from __future__ import annotations

import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from .api_models import CallActionResponse, CallReportExportResponse, CallSummaryResponse, CreateCallRequest, CreateCallResponse, EventEnvelope, ScenarioDefinition
from .error_responses import bad_request, conflict, not_found
from .scenario_library import load_scenario_files
from .call_sessions.call_session_store import CallSessionStore
from .websocket_hub import WebSocketHub
from .voice_session_engine import VoiceSessionEngine
from .settings import get_settings


settings = get_settings()
store = CallSessionStore()
hub = WebSocketHub()
engine = VoiceSessionEngine(store=store, hub=hub)

app = FastAPI(title="CALLSIGNAL API", version="0.1.0")

def _summary_payload(call) -> dict:
    quality_score = None
    if call.quality_json not in {"", "{}"}:
        try:
            quality_score = json.loads(call.quality_json).get("score")
        except Exception:
            quality_score = None
    escalation_reasons = []
    if call.escalation_reason_json not in {"", "[]"}:
        try:
            escalation_reasons = json.loads(call.escalation_reason_json)
        except Exception:
            escalation_reasons = []
    payload = call.model_dump()
    payload["quality_score"] = quality_score
    payload["escalation_reasons"] = escalation_reasons
    return payload
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthz")
def healthz() -> dict:
    return {"ok": True, "service": "callsignal", "env": settings.env}


@app.get("/config")
def config() -> dict:
    return {"env": settings.env, "db_path": str(settings.db_path), "public_api_base_url": settings.public_api_base_url}


@app.get("/demo/scenarios", response_model=list[ScenarioDefinition])
def scenarios() -> list[ScenarioDefinition]:
    return load_scenario_files()


@app.get("/calls", response_model=list[CallSummaryResponse])
def list_calls() -> list[CallSummaryResponse]:
    return [CallSummaryResponse(**_summary_payload(call)) for call in store.list_calls()]


@app.post("/calls", response_model=CreateCallResponse)
def create_call(request: CreateCallRequest) -> CreateCallResponse:
    scenario_id = request.scenario_id or load_scenario_files()[0].scenario_id
    call = engine.create_call(scenario_id=scenario_id, caller_name=request.caller_name)
    return CreateCallResponse(call_id=call.call_id, scenario_id=call.scenario_id, state=call.state)


@app.get("/calls/{call_id}", response_model=CallSummaryResponse)
def get_call(call_id: str) -> CallSummaryResponse:
    call = store.get_call(call_id)
    if call is None:
        raise not_found(f"call {call_id} not found")
    return CallSummaryResponse(**_summary_payload(call))


@app.post("/calls/{call_id}/start", response_model=CallActionResponse)
async def start_call(call_id: str) -> CallActionResponse:
    try:
        result = await engine.start_call(call_id)
    except KeyError:
        raise not_found(f"call {call_id} not found")
    except ValueError as exc:
        raise conflict(str(exc))
    return CallActionResponse(call_id=call_id, state=result["state"], detail=result)


@app.post("/calls/{call_id}/resolve")
async def resolve_call(call_id: str, payload: dict) -> dict:
    try:
        return await engine.resolve_call(call_id, payload.get("resolution_code", "resolved"), payload.get("summary"))
    except KeyError:
        raise not_found(f"call {call_id} not found")
    except ValueError as exc:
        raise bad_request(str(exc))


@app.post("/calls/{call_id}/escalate")
async def escalate_call(call_id: str, payload: dict) -> dict:
    try:
        return await engine.escalate_call(call_id, payload.get("reason", "supervisor_requested"))
    except KeyError:
        raise not_found(f"call {call_id} not found")
    except ValueError as exc:
        raise bad_request(str(exc))


@app.post("/calls/{call_id}/handoff")
async def handoff_call(call_id: str) -> dict:
    try:
        return await engine.handoff_call(call_id)
    except KeyError:
        raise not_found(f"call {call_id} not found")


@app.post("/calls/{call_id}/end")
async def end_call(call_id: str) -> dict:
    try:
        return await engine.end_call(call_id)
    except KeyError:
        raise not_found(f"call {call_id} not found")
    except ValueError as exc:
        raise bad_request(str(exc))


@app.get("/calls/{call_id}/timeline")
def get_timeline(call_id: str) -> list[dict]:
    events = store.list_events(call_id)
    if not events and store.get_call(call_id) is None:
        raise not_found(f"call {call_id} not found")
    return [json.loads(event.payload_json) | {"event_id": event.event_id, "sequence": event.sequence, "event_type": event.event_type, "timestamp": event.timestamp} for event in events]


@app.get("/calls/{call_id}/transcript")
def get_transcript(call_id: str) -> list[dict]:
    frames = store.list_frames(call_id)
    if not frames and store.get_call(call_id) is None:
        raise not_found(f"call {call_id} not found")
    return [frame.model_dump() for frame in frames]


@app.get("/calls/{call_id}/signals")
def get_signals(call_id: str) -> dict:
    call = store.get_call(call_id)
    if call is None:
        raise not_found(f"call {call_id} not found")
    return engine.build_report(call_id)["signals"]


@app.get("/calls/{call_id}/quality")
def get_quality(call_id: str) -> dict:
    call = store.get_call(call_id)
    if call is None:
        raise not_found(f"call {call_id} not found")
    return engine.build_report(call_id)["quality"]


@app.get("/calls/{call_id}/report")
def get_report(call_id: str) -> dict:
    call = store.get_call(call_id)
    if call is None:
        raise not_found(f"call {call_id} not found")
    return engine.build_report(call_id)


@app.post("/calls/{call_id}/report/export", response_model=CallReportExportResponse)
def export_report(call_id: str) -> CallReportExportResponse:
    call = store.get_call(call_id)
    if call is None:
        raise not_found(f"call {call_id} not found")
    report = engine.build_report(call_id)
    return CallReportExportResponse(call_id=call_id, markdown=report["markdown"], json_report=json.loads(report["json"]))


@app.get("/queue/escalations")
def escalation_queue() -> list[dict]:
    queue = []
    for call in store.list_calls():
        if call.state in {"escalation_pending", "handoff_ready", "escalated"}:
            report = engine.build_report(call.call_id)
            queue.append({"call_id": call.call_id, "priority": report["signals"]["escalation"]["priority"], "reason": report["signals"]["escalation"]["reasons"], "recommended_queue": report["signals"]["escalation"]["recommended_queue"], "handoff_packet": report["handoff_packet"]})
    return queue


@app.get("/supervisor/summary")
def supervisor_summary() -> dict:
    calls = store.list_calls()
    total = len(calls)
    active = sum(1 for call in calls if call.state in {"active", "extracting", "escalation_pending", "handoff_ready"})
    escalated = sum(1 for call in calls if call.state == "escalated")
    qa_scores = [json.loads(call.quality_json).get("score", 0) for call in calls if call.quality_json not in {"{}", ""}]
    avg_qa = round(sum(qa_scores) / len(qa_scores), 1) if qa_scores else 0.0
    return {"total_calls": total, "active_calls": active, "escalated_calls": escalated, "average_handling_time": "00:06", "first_call_resolution_rate": 0.6 if total else 0.0, "qa_average": avg_qa}


@app.get("/supervisor/intent-mix")
def intent_mix() -> list[dict]:
    buckets: dict[str, int] = {}
    for call in store.list_calls():
        key = call.current_intent or "unknown"
        buckets[key] = buckets.get(key, 0) + 1
    return [{"intent": intent, "count": count} for intent, count in sorted(buckets.items())]


@app.get("/supervisor/quality-trend")
def quality_trend() -> list[dict]:
    return [{"window": index + 1, "score": 72 + index * 3} for index, _ in enumerate(store.list_calls())]


@app.websocket("/stream/calls/{call_id}")
async def stream_call(call_id: str, websocket: WebSocket) -> None:
    await hub.connect(call_id, websocket)
    try:
        for event in store.list_events(call_id):
            await websocket.send_json({"event_id": event.event_id, "call_id": event.call_id, "sequence": event.sequence, "event_type": event.event_type, "timestamp": event.timestamp, "payload": json.loads(event.payload_json)})
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        await hub.disconnect(call_id, websocket)
