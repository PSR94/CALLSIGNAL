from __future__ import annotations

import json


def timeline_from_events(events: list) -> list[dict]:
    return [
        {
            "event_id": event.event_id,
            "sequence": event.sequence,
            "event_type": event.event_type,
            "timestamp": event.timestamp,
            "payload": json.loads(event.payload_json),
        }
        for event in events
    ]
