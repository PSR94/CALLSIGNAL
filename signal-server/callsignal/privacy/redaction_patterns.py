from __future__ import annotations

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class RedactionMatch:
    kind: str
    value: str
    placeholder: str


PATTERNS = [
    ("email", re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I), "[redacted-email]"),
    ("phone", re.compile(r"\b(?:\+?1[\s.-]?)?(?:\(?\d{3}\)?[\s.-]?)\d{3}[\s.-]?\d{4}\b"), "[redacted-phone]"),
    ("member_id", re.compile(r"\b(?:member|policy|claim|account)[\s-]?(?:id|number|no\.?|#)?:?\s*[A-Z0-9-]{5,}\b", re.I), "[redacted-id]"),
    ("policy_id", re.compile(r"\b(?:POL|P)-\d{4,}[A-Z0-9-]*\b", re.I), "[redacted-policy-id]"),
    ("payment_like", re.compile(r"\b\d{4}([\s-]?\d{4}){2,3}\b"), "[redacted-payment]"),
    ("secret_token", re.compile(r"\b(?:sk|tok|secret)_[A-Za-z0-9_-]{8,}\b"), "[redacted-token]"),
]


def redact_sensitive_text(text: str) -> tuple[str, list[RedactionMatch]]:
    redacted = text
    matches: list[RedactionMatch] = []
    for kind, pattern, placeholder in PATTERNS:
        for match in pattern.finditer(redacted):
            value = match.group(0)
            redacted = redacted.replace(value, placeholder)
            matches.append(RedactionMatch(kind=kind, value=value, placeholder=placeholder))
    return redacted, matches
