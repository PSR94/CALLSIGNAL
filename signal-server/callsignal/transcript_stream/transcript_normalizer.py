from __future__ import annotations

import re


def normalize_transcript(text: str) -> str:
    normalized = text.strip()
    normalized = re.sub(r"\s+", " ", normalized)
    normalized = normalized.replace(" ,", ",").replace(" .", ".").replace(" ?", "?").replace(" !", "!")
    return normalized
