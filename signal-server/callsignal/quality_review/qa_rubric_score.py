from __future__ import annotations


RUBRIC_ITEMS = [
    "greeting_completed",
    "identity_verification_requested",
    "issue_captured",
    "sensitive_data_handled_safely",
    "escalation_handled_correctly",
    "resolution_code_assigned",
    "summary_completeness",
    "customer_sentiment_risk",
]


def score_call(call: dict, signals: dict, transcript_turns: list[dict]) -> dict:
    positive = {
        "greeting_completed": any("hello" in turn["normalized_text"].lower() for turn in transcript_turns),
        "identity_verification_requested": any("verify" in turn["normalized_text"].lower() for turn in transcript_turns),
        "issue_captured": bool(call.get("current_intent") not in {None, "unknown"}),
        "sensitive_data_handled_safely": not any(item.get("redaction_status") == "leaked" for item in signals.get("fields", [])),
        "escalation_handled_correctly": not signals.get("escalation", {}).get("triggered") or call.get("state") in {"handoff_ready", "escalated", "resolved", "ended"},
        "resolution_code_assigned": bool(call.get("resolution_code")),
        "summary_completeness": bool(call.get("summary")),
        "customer_sentiment_risk": signals.get("escalation", {}).get("priority") in {"high", "critical"},
    }
    score = round(sum(1 for value in positive.values() if value) / len(RUBRIC_ITEMS) * 100)
    missed = [item for item, passed in positive.items() if not passed]
    coaching = []
    if not positive["greeting_completed"]:
        coaching.append("Open the call with a greeting before the issue path starts.")
    if not positive["identity_verification_requested"]:
        coaching.append("Ask for identity verification early when the scenario requires it.")
    if positive["customer_sentiment_risk"]:
        coaching.append("Treat the call as elevated risk and keep the handoff packet concise.")
    return {"score": score, "passed": score >= 75, "missed_rubric_items": missed, "coaching_notes": coaching, "evidence_turns": [turn["turn_id"] for turn in transcript_turns[:4]]}
