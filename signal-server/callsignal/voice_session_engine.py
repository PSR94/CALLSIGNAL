from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime, timezone

from .api_models import EventEnvelope
from .call_sessions.call_session_store import CallSessionStore
from .call_sessions.call_state_machine import validate_transition
from .conversation_signals.caller_intent_rules import detect_intent
from .conversation_signals.escalation_rules import evaluate_escalation
from .conversation_signals.field_extraction_rules import extract_fields
from .handoff.handoff_packet_builder import build_handoff_packet
from .handoff.supervisor_note_builder import build_supervisor_note
from .privacy.safe_transcript import safe_transcript_line
from .quality_review.qa_rubric_score import score_call
from .reporting.call_report_builder import build_call_report
from .scenario_library import get_scenario, load_scenario_files
from .transcript_stream.transcript_normalizer import normalize_transcript
from .websocket_hub import WebSocketHub


@dataclass
class VoiceSessionEngine:
    store: CallSessionStore
    hub: WebSocketHub

    def create_call(self, scenario_id: str | None = None, caller_name: str | None = None):
        scenarios = load_scenario_files()
        selected = scenario_id or scenarios[0].scenario_id
        call = self.store.create_call(selected, caller_name=caller_name)
        return call

    def get_call(self, call_id: str):
        call = self.store.get_call(call_id)
        if call is None:
            raise KeyError(call_id)
        return call

    def _save_signal_bundle(self, call_id: str) -> dict:
        frames = self.store.list_frames(call_id)
        call = self.get_call(call_id)
        redactions = [redaction.model_dump() for redaction in self.store.list_redactions(call_id)]
        transcript_turns = [frame.normalized_text for frame in frames if not frame.is_partial]
        last_turn = frames[-1] if frames else None
        intent = detect_intent(last_turn.normalized_text if last_turn else "", last_turn.turn_id if last_turn else "turn-0")
        fields = []
        for frame in frames:
            if frame.is_partial:
                continue
            fields.extend(extract_fields(frame.normalized_text, frame.turn_id))
        escalation = evaluate_escalation(transcript_turns, intent.intent, intent.confidence)
        handoff = None
        if escalation["triggered"]:
            handoff = build_handoff_packet(
                call={"call_id": call.call_id, "current_intent": intent.intent},
                summary=self._summarize_call(call.call_id, frames),
                extracted_fields=[field.__dict__ for field in fields],
                escalation=escalation,
                transcript_excerpt=[frame.redacted_text for frame in frames[-4:]],
                next_best_action="Transfer to supervisor and preserve the redacted transcript excerpt.",
            )
        quality = score_call({"call_id": call.call_id, "state": call.state, "current_intent": intent.intent, "resolution_code": call.resolution_code, "summary": self._summarize_call(call.call_id, frames)}, {"fields": [field.__dict__ for field in fields], "escalation": escalation}, [frame.model_dump() for frame in frames])
        return {"intent": intent, "fields": fields, "redactions": redactions, "escalation": escalation, "handoff": handoff, "quality": quality}

    def _summarize_call(self, call_id: str, frames) -> str:
        if not frames:
            return "Call opened but no transcript has been captured yet."
        issue = frames[-1].redacted_text
        return f"{call_id} tracked a live support conversation. Most recent turn: {issue}"

    async def start_call(self, call_id: str) -> dict:
        call = self.get_call(call_id)
        validate_transition(call.state, "connecting")
        call.state = "connecting"
        self.store.save_call(call)
        sequence = len(self.store.list_events(call_id)) + 1
        await self.hub.broadcast(call_id, self.store.append_event(call_id, sequence, "call_started", {"state": call.state}))
        validate_transition(call.state, "active")
        call.state = "active"
        call.started_at = call.started_at or datetime.now(timezone.utc).isoformat()
        self.store.save_call(call)
        scenario = get_scenario(call.scenario_id)
        sequence += 1
        await self.hub.broadcast(call_id, self.store.append_event(call_id, sequence, "call_started", {"state": call.state, "scenario_id": scenario.scenario_id}))
        await self._play_scenario(call_id, scenario.turns, sequence + 1)
        return {"call_id": call_id, "state": self.get_call(call_id).state}

    async def _play_scenario(self, call_id: str, turns: list[dict], sequence: int) -> None:
        call = self.get_call(call_id)
        for turn in turns:
            await asyncio.sleep(0.1)
            normalized = normalize_transcript(turn["text"])
            safe_text, matches = safe_transcript_line(normalized)
            frame = self.store.append_frame(call_id, turn["turn_id"], turn["speaker"], turn["text"], normalized, turn.get("kind", "final") == "partial", sequence, "simulator", safe_text, matches)
            for match_index, match in enumerate(matches, start=1):
                self.store.append_redaction(call_id, turn["turn_id"], sequence + match_index, match["kind"], match["value"], match["placeholder"])
            await self.hub.broadcast(call_id, self.store.append_event(call_id, sequence, "transcript_" + turn.get("kind", "final"), {"turn_id": frame.turn_id, "speaker": frame.speaker, "text": frame.text, "normalized_text": frame.normalized_text, "redacted_text": frame.redacted_text}))
            await self.hub.broadcast(call_id, self.store.append_event(call_id, sequence + 1, "speaker_turn", {"speaker": frame.speaker, "turn_id": frame.turn_id}))
            bundle = self._save_signal_bundle(call_id)
            intent = bundle["intent"]
            call.current_intent = intent.intent
            call.intent_confidence = intent.confidence
            call.summary = self._summarize_call(call_id, self.store.list_frames(call_id))
            self.store.save_call(call)
            await self.hub.broadcast(call_id, self.store.append_event(call_id, sequence + 2, "intent_changed", intent.__dict__))
            for field in bundle["fields"]:
                await self.hub.broadcast(call_id, self.store.append_event(call_id, sequence + 3, "field_extracted", field.__dict__))
            if matches:
                for redaction in self.store.list_redactions(call_id)[-len(matches):]:
                    await self.hub.broadcast(call_id, self.store.append_event(call_id, sequence + 4, "sensitive_value_redacted", redaction.model_dump()))
            if bundle["escalation"]["triggered"] and call.state == "active":
                validate_transition(call.state, "escalation_pending")
                call.state = "escalation_pending"
                self.store.save_call(call)
                await self.hub.broadcast(call_id, self.store.append_event(call_id, sequence + 5, "escalation_detected", bundle["escalation"]))
                validate_transition(call.state, "handoff_ready")
                call.state = "handoff_ready"
                call.handoff_packet_json = json.dumps(bundle["handoff"], sort_keys=True) if bundle["handoff"] else "{}"
                call.escalation_reason_json = json.dumps(bundle["escalation"]["reasons"], sort_keys=True)
                call.quality_json = json.dumps(bundle["quality"], sort_keys=True)
                self.store.save_call(call)
                await self.hub.broadcast(call_id, self.store.append_event(call_id, sequence + 6, "handoff_packet_ready", bundle["handoff"] or {}))
                await self.hub.broadcast(call_id, self.store.append_event(call_id, sequence + 7, "qa_score_changed", bundle["quality"]))
            sequence += 8

    async def resolve_call(self, call_id: str, resolution_code: str, summary: str | None = None) -> dict:
        call = self.get_call(call_id)
        if call.state in {"idle", "failed", "ended"}:
            raise ValueError("call cannot be resolved from its current state")
        validate_transition(call.state, "resolved")
        call.state = "resolved"
        call.resolution_code = resolution_code
        call.summary = summary or call.summary or "Call resolved."
        call.quality_json = json.dumps(self._save_signal_bundle(call_id)["quality"], sort_keys=True)
        self.store.save_call(call)
        payload = {"resolution_code": resolution_code, "summary": call.summary}
        await self.hub.broadcast(call_id, self.store.append_event(call_id, len(self.store.list_events(call_id)) + 1, "call_resolved", payload))
        return payload

    async def escalate_call(self, call_id: str, reason: str) -> dict:
        call = self.get_call(call_id)
        if call.state in {"ended", "failed"}:
            raise ValueError("cannot escalate a closed call")
        validate_transition(call.state, "escalated")
        call.state = "escalated"
        call.escalation_reason_json = json.dumps([reason], sort_keys=True)
        call.quality_json = json.dumps(self._save_signal_bundle(call_id)["quality"], sort_keys=True)
        self.store.save_call(call)
        payload = {"reason": reason}
        await self.hub.broadcast(call_id, self.store.append_event(call_id, len(self.store.list_events(call_id)) + 1, "call_escalated", payload))
        return payload

    async def handoff_call(self, call_id: str) -> dict:
        call = self.get_call(call_id)
        bundle = self._save_signal_bundle(call_id)
        call.handoff_packet_json = json.dumps(bundle["handoff"] or {}, sort_keys=True)
        call.quality_json = json.dumps(bundle["quality"], sort_keys=True)
        self.store.save_call(call)
        payload = bundle["handoff"] or {}
        await self.hub.broadcast(call_id, self.store.append_event(call_id, len(self.store.list_events(call_id)) + 1, "handoff_packet_ready", payload))
        return payload

    async def end_call(self, call_id: str) -> dict:
        call = self.get_call(call_id)
        if call.state not in {"resolved", "escalated", "handoff_ready", "active", "escalation_pending"}:
            raise ValueError("call cannot be ended from its current state")
        validate_transition(call.state, "ended")
        call.state = "ended"
        from datetime import datetime, timezone
        call.ended_at = datetime.now(timezone.utc).isoformat()
        self.store.save_call(call)
        payload = {"state": call.state}
        await self.hub.broadcast(call_id, self.store.append_event(call_id, len(self.store.list_events(call_id)) + 1, "call_ended", payload))
        return payload

    def build_report(self, call_id: str) -> dict:
        call = self.get_call(call_id)
        timeline = [event.model_dump() for event in self.store.list_events(call_id)]
        transcript = [frame.model_dump() for frame in self.store.list_frames(call_id)]
        signals = self._save_signal_bundle(call_id)
        report = build_call_report(call.model_dump(), timeline, transcript, {"intent": signals["intent"].__dict__, "fields": [field.__dict__ for field in signals["fields"]], "redactions": signals["redactions"], "escalation": signals["escalation"]}, signals["quality"], signals["handoff"])
        return report
