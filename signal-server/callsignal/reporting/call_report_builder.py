from __future__ import annotations

from .markdown_report import render_markdown_report
from .json_report import render_json_report


def build_call_report(call: dict, timeline: list[dict], transcript: list[dict], signals: dict, quality: dict, handoff: dict | None) -> dict:
    report = {
        "call_id": call["call_id"],
        "scenario_id": call.get("scenario_id"),
        "state": call["state"],
        "current_intent": call.get("current_intent", "unknown"),
        "resolution_code": call.get("resolution_code"),
        "summary": call.get("summary", ""),
        "timeline": timeline,
        "transcript": transcript,
        "signals": signals,
        "quality": quality,
        "handoff_packet": handoff,
    }
    report["markdown"] = render_markdown_report(report)
    report["json"] = render_json_report(report)
    return report
