from __future__ import annotations

import asyncio
from pathlib import Path
import json

from ..scenario_library import load_scenario_files
from ..call_sessions.call_session_store import CallSessionStore
from ..voice_session_engine import VoiceSessionEngine
from ..websocket_hub import WebSocketHub


async def seed_demo_state() -> list[dict]:
    store = CallSessionStore()
    engine = VoiceSessionEngine(store=store, hub=WebSocketHub())
    results = []
    for scenario in load_scenario_files():
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
        results.append({"call_id": call.call_id, "scenario_id": scenario.scenario_id, "state": engine.get_call(call.call_id).state, "quality": report["quality"]["score"]})
    return results


def main() -> None:
    results = asyncio.run(seed_demo_state())
    print(json.dumps(results, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
