# Call state model

The session engine uses a strict state machine:

- `idle`
- `connecting`
- `active`
- `extracting`
- `escalation_pending`
- `handoff_ready`
- `resolved`
- `escalated`
- `ended`
- `failed`

State transitions are validated before mutation. Invalid transitions fail fast so the UI can show a real error instead of silently drifting out of sync with the backend.
