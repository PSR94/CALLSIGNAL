#!/usr/bin/env bash
set -euo pipefail

empty_dirs=$(find . -type d -empty -not -path './.git/*' -not -path './node_modules/*' -not -path './signal-server/.venv/*' -not -path './call-room/node_modules/*')
if [[ -n "$empty_dirs" ]]; then
  printf '%s\n' "$empty_dirs"
  exit 1
fi
