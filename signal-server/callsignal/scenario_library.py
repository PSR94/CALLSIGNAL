from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import yaml

from .api_models import ScenarioDefinition


ROOT = Path(__file__).resolve().parents[2]
SCENARIO_DIR = ROOT / "scenario-lab" / "call_scripts"


@dataclass(frozen=True)
class ScenarioTurn:
    speaker: str
    text: str
    kind: str = "final"


def load_scenario_files() -> list[ScenarioDefinition]:
    scenarios: list[ScenarioDefinition] = []
    for path in sorted(SCENARIO_DIR.glob("*.yaml")):
        data = yaml.safe_load(path.read_text())
        scenarios.append(ScenarioDefinition(**data))
    return scenarios


def get_scenario(scenario_id: str) -> ScenarioDefinition:
    for scenario in load_scenario_files():
        if scenario.scenario_id == scenario_id:
            return scenario
    raise KeyError(scenario_id)
