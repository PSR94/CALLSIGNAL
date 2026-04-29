# Decision 003: redacted transcript boundary

Sensitive values are redacted in the backend before the transcript reaches the safe UI projection. The raw text remains out of the workspace path so the UI never has to guess which spans are safe.
