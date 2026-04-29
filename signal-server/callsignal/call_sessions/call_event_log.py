from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4
import json

from ..storage.sqlite_store import CallEventRecord, get_store


def append_call_event(call_id: str, sequence: int, event_type: str, payload: dict) -> dict:
    event = {
        "event_id": str(uuid4()),
        "call_id": call_id,
        "sequence": sequence,
        "event_type": event_type,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "payload": payload,
    }
    get_store().append_event(CallEventRecord(
        event_id=event["event_id"],
        call_id=call_id,
        sequence=sequence,
        event_type=event_type,
        timestamp=event["timestamp"],
        payload_json=json.dumps(payload, sort_keys=True),
    ))
    return event
