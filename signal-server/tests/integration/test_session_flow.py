from __future__ import annotations

import asyncio

from callsignal.call_sessions.call_session_store import CallSessionStore
from callsignal.voice_session_engine import VoiceSessionEngine
from callsignal.websocket_hub import WebSocketHub


def test_demo_call_flow_produces_ordered_events():
    store = CallSessionStore()
    engine = VoiceSessionEngine(store=store, hub=WebSocketHub())
    call = engine.create_call("insurance_intake")
    asyncio.run(engine.start_call(call.call_id))
    events = store.list_events(call.call_id)
    assert events
    assert [event.sequence for event in events] == sorted(event.sequence for event in events)
