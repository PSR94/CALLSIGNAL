from __future__ import annotations


def route_queue(priority: str, reasons: list[str]) -> str:
    if priority == "critical":
        return "critical_escalation"
    if "cancellation_risk" in reasons:
        return "retention_queue"
    return "supervisor_queue"
