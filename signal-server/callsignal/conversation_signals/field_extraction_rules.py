from __future__ import annotations

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class ExtractedField:
    field_name: str
    value: str
    confidence: float
    source_turn: str
    redaction_status: str


PATTERNS = {
    "caller_name": re.compile(r"\b(?:my name is|this is)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2})\b", re.I),
    "phone_number": re.compile(r"\b(?:\+?1[\s.-]?)?(?:\(?\d{3}\)?[\s.-]?)\d{3}[\s.-]?\d{4}\b"),
    "email": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
    "policy_id": re.compile(r"\b(?:policy|member|claim)\s*(?:id|number|no\.?|#)\s*[:#-]?\s*([A-Z0-9-]{5,})\b", re.I),
    "appointment_date": re.compile(r"\b(?:on|for)\s+([A-Z][a-z]+\s+\d{1,2}(?:,\s*\d{4})?|\d{1,2}/\d{1,2}/\d{2,4})\b", re.I),
}


def extract_fields(text: str, turn_id: str) -> list[ExtractedField]:
    fields: list[ExtractedField] = []
    for field_name, pattern in PATTERNS.items():
        match = pattern.search(text)
        if match:
            value = match.group(1) if match.groups() else match.group(0)
            redaction_status = "redacted" if field_name in {"phone_number", "email", "policy_id"} else "clear"
            fields.append(ExtractedField(field_name=field_name, value=value, confidence=0.89, source_turn=turn_id, redaction_status=redaction_status))
    lowered = text.lower()
    if "urgent" in lowered or "today" in lowered:
        fields.append(ExtractedField(field_name="urgency", value="high", confidence=0.77, source_turn=turn_id, redaction_status="clear"))
    if "call me back" in lowered:
        fields.append(ExtractedField(field_name="callback_preference", value="call_back", confidence=0.73, source_turn=turn_id, redaction_status="clear"))
    if "refund" in lowered:
        fields.append(ExtractedField(field_name="requested_action", value="refund", confidence=0.83, source_turn=turn_id, redaction_status="clear"))
    if "reschedule" in lowered:
        fields.append(ExtractedField(field_name="requested_action", value="reschedule", confidence=0.83, source_turn=turn_id, redaction_status="clear"))
    return fields
