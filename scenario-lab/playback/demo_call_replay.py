from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import yaml


@dataclass(frozen=True)
class DemoCallReplay:
    scenario_id: str
    turns: list[dict]


def load_replay(path: Path) -> DemoCallReplay:
    payload = yaml.safe_load(path.read_text())
    return DemoCallReplay(scenario_id=payload["scenario_id"], turns=payload["turns"])
