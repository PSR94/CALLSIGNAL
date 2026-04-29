from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, Field


class CreateCallRequest(BaseModel):
    scenario_id: str | None = None
    caller_name: str | None = None


class CreateCallResponse(BaseModel):
    call_id: str
    scenario_id: str
    state: str


class CallActionResponse(BaseModel):
    call_id: str
    state: str
    detail: dict


class CallSummaryResponse(BaseModel):
    call_id: str
    scenario_id: str
    state: str
    caller_name: str | None = None
    current_intent: str | None = None
    intent_confidence: float | None = None
    summary: str | None = None
    resolution_code: str | None = None
    quality_score: int | None = None
    escalation_reasons: list[str] = Field(default_factory=list)
    started_at: str | None = None
    ended_at: str | None = None
    created_at: str
    updated_at: str


class ScenarioDefinition(BaseModel):
    scenario_id: str
    title: str
    caller_persona: str
    problem_type: str
    turns: list[dict]
    expected_intents: list[str]
    expected_redactions: list[str]
    expected_escalation: list[str]
    expected_quality: str


class EventEnvelope(BaseModel):
    event_id: str
    call_id: str
    sequence: int
    event_type: str
    timestamp: str
    payload: dict


class CallReportExportResponse(BaseModel):
    call_id: str
    markdown: str
    json_report: dict = Field(alias="json")

    model_config = {"populate_by_name": True}
