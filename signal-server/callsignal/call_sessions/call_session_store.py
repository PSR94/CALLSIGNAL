from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from ..storage.sqlite_store import (
    CallEventRecord,
    CallSessionRecord,
    RedactionEventRecord,
    TranscriptFrameRecord,
    get_store,
    json_dump,
    json_load,
    utcnow,
)


class CallSessionStore:
    def __init__(self) -> None:
        self.store = get_store()

    def create_call(self, scenario_id: str, caller_name: str | None = None) -> CallSessionRecord:
        now = utcnow()
        record = CallSessionRecord(
            call_id=str(uuid4()),
            scenario_id=scenario_id,
            caller_name=caller_name,
            state="idle",
            created_at=now,
            updated_at=now,
        )
        return self.store.upsert_call(record)

    def get_call(self, call_id: str) -> CallSessionRecord | None:
        return self.store.get_call(call_id)

    def save_call(self, call: CallSessionRecord) -> CallSessionRecord:
        call.updated_at = utcnow()
        return self.store.upsert_call(call)

    def list_calls(self) -> list[CallSessionRecord]:
        return self.store.list_calls()

    def list_events(self, call_id: str) -> list[CallEventRecord]:
        return self.store.list_events(call_id)

    def append_event(self, call_id: str, sequence: int, event_type: str, payload: dict) -> dict:
        event_id = str(uuid4())
        timestamp = datetime.now(timezone.utc).isoformat()
        self.store.append_event(CallEventRecord(
            event_id=event_id,
            call_id=call_id,
            sequence=sequence,
            event_type=event_type,
            timestamp=timestamp,
            payload_json=json_dump(payload),
        ))
        return {"event_id": event_id, "call_id": call_id, "sequence": sequence, "event_type": event_type, "timestamp": timestamp, "payload": payload}

    def append_frame(self, call_id: str, turn_id: str, speaker: str, text: str, normalized_text: str, is_partial: bool, sequence: int, source: str, redacted_text: str, redaction_matches: list[dict]) -> TranscriptFrameRecord:
        now = utcnow()
        record = TranscriptFrameRecord(
            id=str(uuid4()),
            call_id=call_id,
            turn_id=turn_id,
            speaker=speaker,
            text=text,
            normalized_text=normalized_text,
            is_partial=is_partial,
            sequence=sequence,
            source=source,
            redacted_text=redacted_text,
            redaction_matches_json=json_dump(redaction_matches),
            created_at=now,
        )
        return self.store.append_transcript(record)

    def list_frames(self, call_id: str) -> list[TranscriptFrameRecord]:
        return self.store.list_transcript(call_id)

    def append_redaction(self, call_id: str, turn_id: str, sequence: int, kind: str, original_value: str, placeholder: str) -> RedactionEventRecord:
        now = utcnow()
        record = RedactionEventRecord(
            id=str(uuid4()),
            call_id=call_id,
            turn_id=turn_id,
            sequence=sequence,
            redaction_kind=kind,
            original_value=original_value,
            placeholder=placeholder,
            created_at=now,
        )
        return self.store.append_redaction(record)

    def list_redactions(self, call_id: str) -> list[RedactionEventRecord]:
        return self.store.list_redactions(call_id)
