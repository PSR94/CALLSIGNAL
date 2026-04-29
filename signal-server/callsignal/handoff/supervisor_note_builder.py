from __future__ import annotations


def build_supervisor_note(call: dict) -> str:
    return f"{call['call_id']} :: {call.get('current_intent', 'unknown')} :: {call.get('resolution_code', 'unresolved')}"
