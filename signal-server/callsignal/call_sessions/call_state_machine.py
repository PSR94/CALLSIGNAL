from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
import yaml


STATE_FILE = Path(__file__).with_name("call_state_machine.yaml")


@dataclass(frozen=True)
class StateMachine:
    states: tuple[str, ...]
    transitions: dict[str, tuple[str, ...]]

    def can_transition(self, current: str, next_state: str) -> bool:
        return next_state in self.transitions.get(current, ())


def load_state_machine() -> StateMachine:
    payload = yaml.safe_load(STATE_FILE.read_text())
    transitions = {key: tuple(value) for key, value in payload["transitions"].items()}
    return StateMachine(states=tuple(payload["states"]), transitions=transitions)


def validate_transition(current: str, next_state: str) -> None:
    machine = load_state_machine()
    if not machine.can_transition(current, next_state):
        raise ValueError(f"invalid call state transition: {current} -> {next_state}")
