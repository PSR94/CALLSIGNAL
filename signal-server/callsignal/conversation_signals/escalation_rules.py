from __future__ import annotations


ESCALATION_PATTERNS = {
    "angry_language": ["angry", "frustrated", "unacceptable", "this is ridiculous", "worst"],
    "supervisor_requested": ["supervisor", "manager", "escalate"],
    "payment_dispute": ["charge", "billing", "refund", "payment dispute"],
    "urgent_medical": ["urgent", "medical", "can not wait", "can't wait", "today"],
    "cancellation_risk": ["cancel my", "canceling", "close my account", "leave"],
    "compliance_sensitive": ["ssn", "social security", "credit card", "bank account"],
}


def evaluate_escalation(transcript: list[str], intent: str, confidence: float) -> dict:
    joined = " ".join(transcript).lower()
    reasons = [name for name, phrases in ESCALATION_PATTERNS.items() if any(phrase in joined for phrase in phrases)]
    if confidence < 0.55 and len(transcript) >= 3:
        reasons.append("low_confidence_after_multiple_turns")
    if intent == "cancellation_request":
        reasons.append("cancellation_risk")
    priority = "normal"
    if any(reason in reasons for reason in ["urgent_medical", "compliance_sensitive"]):
        priority = "critical"
    elif reasons:
        priority = "high"
    return {"triggered": bool(reasons), "reasons": sorted(set(reasons)), "priority": priority, "recommended_queue": "supervisor_queue" if reasons else "frontline_queue"}
