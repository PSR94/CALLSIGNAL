# Event model

CALLSIGNAL persists call activity as a sequence-ordered event log.

Each event includes an ID, call ID, sequence number, event type, timestamp, and payload. The websocket stream mirrors the same structure so the UI can replay or append events without translating between transport shapes.

Supported event types include transcript updates, speaker turns, intent changes, field extraction, sensitive-value redaction, escalation detection, handoff readiness, QA score changes, and terminal call outcomes.
