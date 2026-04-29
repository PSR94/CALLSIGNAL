from __future__ import annotations

from .transcript_normalizer import normalize_transcript
from ..privacy.redaction_patterns import redact_sensitive_text


def build_safe_frame(text: str) -> dict:
    normalized = normalize_transcript(text)
    redacted, matches = redact_sensitive_text(normalized)
    return {"normalized": normalized, "redacted": redacted, "matches": [m.__dict__ for m in matches]}
