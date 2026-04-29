#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "$0")/.." && pwd)"

if [[ ! -x "$root_dir/signal-server/.venv/bin/uvicorn" ]]; then
  echo "Backend environment is missing. Run make bootstrap first."
  exit 1
fi

(
  cd "$root_dir/signal-server"
  . .venv/bin/activate
  uvicorn callsignal.app:app --host 127.0.0.1 --port 8088
) &
api_pid=$!

(
  cd "$root_dir/call-room"
  npm run dev -- --host 127.0.0.1
) &
ui_pid=$!

cleanup() {
  kill "$api_pid" "$ui_pid" 2>/dev/null || true
}

trap cleanup EXIT INT TERM
wait "$api_pid" "$ui_pid"
