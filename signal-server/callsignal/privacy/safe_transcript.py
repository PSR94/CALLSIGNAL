from __future__ import annotations

from .redaction_patterns import redact_sensitive_text


def safe_transcript_line(text: str) -> tuple[str, list[dict[str, str]]]:
    redacted, matches = redact_sensitive_text(text)
    return redacted, [match.__dict__ for match in matches]
