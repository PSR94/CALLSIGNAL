from __future__ import annotations

from pathlib import Path
import json


def write_stream_fixture(path: Path, events: list[dict]) -> None:
    path.write_text(json.dumps(events, indent=2, sort_keys=True) + "\n")
