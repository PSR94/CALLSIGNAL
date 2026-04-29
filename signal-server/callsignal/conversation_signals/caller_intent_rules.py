from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class IntentSignal:
    intent: str
    confidence: float
    evidence_phrase: str
    turn_id: str


INTENT_RULES = [
    ("billing_question", ["bill", "charge", "payment", "invoice", "refund"]),
    ("appointment_request", ["appointment", "reschedule", "book", "availability"]),
    ("insurance_intake", ["member id", "policy", "coverage", "benefits", "claims"]),
    ("claim_status", ["claim status", "claim number", "claim update"]),
    ("technical_issue", ["not working", "broken", "error", "technical"]),
    ("cancellation_request", ["cancel", "cancel my", "terminate", "close my account"]),
    ("escalation_request", ["supervisor", "manager", "escalate", "complaint"]),
    ("complaint", ["frustrated", "angry", "unacceptable", "worst"]),
]


def detect_intent(text: str, turn_id: str) -> IntentSignal:
    lowered = text.lower()
    for intent, phrases in INTENT_RULES:
        for phrase in phrases:
            if phrase in lowered:
                confidence = 0.95 if len(phrase.split()) > 1 else 0.84
                return IntentSignal(intent=intent, confidence=confidence, evidence_phrase=phrase, turn_id=turn_id)
    return IntentSignal(intent="unknown", confidence=0.42, evidence_phrase=text[:40], turn_id=turn_id)
