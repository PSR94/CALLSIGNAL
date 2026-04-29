from __future__ import annotations

from pydantic import BaseModel, Field


class TranscriptFrame(BaseModel):
    turn_id: str
    speaker: str
    text: str
    normalized_text: str
    is_partial: bool = False
    sequence: int = Field(ge=1)
    source: str = "simulator"


class TranscriptSignal(BaseModel):
    kind: str
    value: str
    turn_id: str
    sequence: int
