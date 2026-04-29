from __future__ import annotations


def build_handoff_packet(call: dict, summary: str, extracted_fields: list[dict], escalation: dict, transcript_excerpt: list[str], next_best_action: str) -> dict:
    return {
        "call_id": call["call_id"],
        "call_summary": summary,
        "detected_intent": call.get("current_intent", "unknown"),
        "extracted_fields": extracted_fields,
        "escalation_reason": escalation.get("reasons", []),
        "priority": escalation.get("priority", "normal"),
        "recommended_queue": escalation.get("recommended_queue", "frontline_queue"),
        "redacted_transcript_excerpt": transcript_excerpt,
        "next_best_action": next_best_action,
    }
