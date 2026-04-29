from __future__ import annotations

from sqlmodel import Field, SQLModel


class TranscriptFrameRecord(SQLModel, table=True):
    id: str = Field(primary_key=True)
    call_id: str = Field(index=True)
    turn_id: str
    speaker: str
    text: str
    normalized_text: str
    is_partial: bool = False
    sequence: int = Field(index=True)
    source: str = "simulator"
