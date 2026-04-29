from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import json
import sqlite3

from sqlmodel import SQLModel, Field, Session, create_engine, select

from ..settings import get_settings


class CallSessionRecord(SQLModel, table=True):
    call_id: str = Field(primary_key=True)
    scenario_id: str
    caller_name: str | None = None
    state: str = "idle"
    current_intent: str | None = None
    intent_confidence: float | None = None
    summary: str | None = None
    resolution_code: str | None = None
    started_at: str | None = None
    ended_at: str | None = None
    escalation_reason_json: str = "[]"
    handoff_packet_json: str = "{}"
    quality_json: str = "{}"
    created_at: str
    updated_at: str


class CallEventRecord(SQLModel, table=True):
    event_id: str = Field(primary_key=True)
    call_id: str = Field(index=True)
    sequence: int = Field(index=True)
    event_type: str
    timestamp: str
    payload_json: str


class RedactionEventRecord(SQLModel, table=True):
    id: str = Field(primary_key=True)
    call_id: str = Field(index=True)
    turn_id: str
    sequence: int = Field(index=True)
    redaction_kind: str
    original_value: str
    placeholder: str
    created_at: str


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
    redacted_text: str
    redaction_matches_json: str
    created_at: str


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


class SQLiteStore:
    def __init__(self, db_path: Path):
        db_path.parent.mkdir(parents=True, exist_ok=True)
        self.engine = create_engine(f"sqlite:///{db_path}")
        SQLModel.metadata.create_all(self.engine)

    def session(self) -> Session:
        return Session(self.engine, expire_on_commit=False)

    def list_calls(self) -> list[CallSessionRecord]:
        with self.session() as session:
            return list(session.exec(select(CallSessionRecord).order_by(CallSessionRecord.created_at.desc())).all())

    def get_call(self, call_id: str) -> CallSessionRecord | None:
        with self.session() as session:
            return session.get(CallSessionRecord, call_id)

    def upsert_call(self, record: CallSessionRecord) -> CallSessionRecord:
        with self.session() as session:
            existing = session.get(CallSessionRecord, record.call_id)
            if existing is None:
                session.add(record)
            else:
                for key, value in record.model_dump().items():
                    setattr(existing, key, value)
            session.commit()
            return session.get(CallSessionRecord, record.call_id) or record

    def append_event(self, record: CallEventRecord) -> CallEventRecord:
        with self.session() as session:
            session.add(record)
            session.commit()
            return record

    def list_events(self, call_id: str) -> list[CallEventRecord]:
        with self.session() as session:
            statement = select(CallEventRecord).where(CallEventRecord.call_id == call_id).order_by(CallEventRecord.sequence.asc())
            return list(session.exec(statement).all())

    def append_transcript(self, record: TranscriptFrameRecord) -> TranscriptFrameRecord:
        with self.session() as session:
            session.add(record)
            session.commit()
            return record

    def list_transcript(self, call_id: str) -> list[TranscriptFrameRecord]:
        with self.session() as session:
            statement = select(TranscriptFrameRecord).where(TranscriptFrameRecord.call_id == call_id).order_by(TranscriptFrameRecord.sequence.asc())
            return list(session.exec(statement).all())

    def append_redaction(self, record: RedactionEventRecord) -> RedactionEventRecord:
        with self.session() as session:
            session.add(record)
            session.commit()
            return record

    def list_redactions(self, call_id: str) -> list[RedactionEventRecord]:
        with self.session() as session:
            statement = select(RedactionEventRecord).where(RedactionEventRecord.call_id == call_id).order_by(RedactionEventRecord.sequence.asc())
            return list(session.exec(statement).all())


def json_load(value: str) -> Any:
    return json.loads(value)


def json_dump(value: Any) -> str:
    return json.dumps(value, sort_keys=True)


def get_store() -> SQLiteStore:
    return SQLiteStore(get_settings().db_path)
