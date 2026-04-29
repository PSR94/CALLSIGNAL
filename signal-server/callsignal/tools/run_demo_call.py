from __future__ import annotations

import asyncio
import json

from ..scenario_library import load_scenario_files
from ..call_sessions.call_session_store import CallSessionStore
from ..voice_session_engine import VoiceSessionEngine
from ..websocket_hub import WebSocketHub


async def run_demo_call() -> dict:
    store = CallSessionStore()
    engine = VoiceSessionEngine(store=store, hub=WebSocketHub())
    scenario = load_scenario_files()[0]
    call = engine.create_call(scenario_id=scenario.scenario_id)
    await engine.start_call(call.call_id)
    if scenario.scenario_id in {"billing_dispute", "technical_support", "cancellation_risk"}:
        if engine.get_call(call.call_id).state != "escalated":
            await engine.escalate_call(call.call_id, "supervisor_requested")
        await engine.end_call(call.call_id)
    else:
        await engine.resolve_call(call.call_id, "resolved", f"{scenario.title} completed in the demo session.")
        await engine.end_call(call.call_id)
    report = engine.build_report(call.call_id)
    return report


def main() -> None:
    report = asyncio.run(run_demo_call())
    print(json.dumps({"call_id": report["call_id"], "state": report["state"], "quality": report["quality"], "signals": report["signals"]}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
