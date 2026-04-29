# Decision 002: websocket event stream

CALLSIGNAL uses a websocket instead of polling because the live workspace is defined by the stream of turn updates. The backend event log and websocket payload share the same envelope shape so the UI can render and review the same data.
