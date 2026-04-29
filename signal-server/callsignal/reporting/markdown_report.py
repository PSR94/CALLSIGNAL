from __future__ import annotations


def render_markdown_report(report: dict) -> str:
    lines = [
        f"# Call Review: {report['call_id']}",
        "",
        f"- State: {report['state']}",
        f"- Intent: {report['current_intent']}",
        f"- Resolution code: {report.get('resolution_code', 'unresolved')}",
        f"- QA score: {report['quality']['score']}",
        f"- Escalation: {', '.join(report['signals']['escalation']['reasons']) or 'none'}",
        "",
        "## Extracted fields",
    ]
    for field in report['signals']['fields']:
        lines.append(f"- {field['field_name']}: {field['value']} ({field['redaction_status']})")
    lines.extend(["", "## Redacted transcript"])
    for turn in report['transcript']:
        lines.append(f"- {turn['speaker']}: {turn['redacted_text']}")
    return "\n".join(lines) + "\n"
