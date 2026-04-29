from __future__ import annotations

import json


def render_json_report(report: dict) -> str:
    return json.dumps(report, indent=2, sort_keys=True)
