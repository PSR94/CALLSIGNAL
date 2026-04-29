from __future__ import annotations

from callsignal.reporting.call_report_builder import build_call_report


def test_report_contains_markdown_and_json():
    report = build_call_report(
        {"call_id": "c1", "state": "ended", "current_intent": "billing_question", "resolution_code": "resolved", "summary": "done"},
        [{"event_id": "e1", "sequence": 1, "event_type": "call_started", "timestamp": "2026-04-27T00:00:00Z", "payload": {}}],
        [{"speaker": "caller", "redacted_text": "hello"}],
        {"intent": {"intent": "billing_question"}, "fields": [], "escalation": {"reasons": [], "priority": "normal", "recommended_queue": "frontline_queue"}},
        {"score": 88, "passed": True, "missed_rubric_items": [], "coaching_notes": [], "evidence_turns": ["t1"]},
        None,
    )
    assert report["markdown"].startswith("# Call Review")
    assert '"call_id": "c1"' in report["json"]
