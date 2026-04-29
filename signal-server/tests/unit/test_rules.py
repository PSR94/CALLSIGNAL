from __future__ import annotations

from callsignal.conversation_signals.caller_intent_rules import detect_intent
from callsignal.conversation_signals.field_extraction_rules import extract_fields
from callsignal.conversation_signals.escalation_rules import evaluate_escalation
from callsignal.privacy.redaction_patterns import redact_sensitive_text
from callsignal.transcript_stream.transcript_normalizer import normalize_transcript


def test_normalizer_collapses_space():
    assert normalize_transcript("  hello   there  ") == "hello there"


def test_intent_detection_prefers_billing():
    result = detect_intent("I was charged twice and need a refund", "t1")
    assert result.intent == "billing_question"


def test_field_extraction_and_redaction():
    text = "My name is Jordan Lee and my email is jordan.lee@example.com and my phone is 555-214-9876"
    fields = extract_fields(text, "t2")
    assert any(field.field_name == "caller_name" for field in fields)
    redacted, matches = redact_sensitive_text(text)
    assert "[redacted-email]" in redacted
    assert any(match.kind == "phone" for match in matches)


def test_escalation_rules_trigger_on_supervisor_request():
    escalation = evaluate_escalation(["This is unacceptable", "Please escalate me to a supervisor"], "billing_question", 0.92)
    assert escalation["triggered"]
    assert "supervisor_requested" in escalation["reasons"]


def test_policy_redaction_does_not_match_regular_words():
    redacted, _matches = redact_sensitive_text("Please keep my appointment for next week")
    assert "[redacted-policy-id]" not in redacted
