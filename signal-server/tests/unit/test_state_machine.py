from __future__ import annotations

import pytest

from callsignal.call_sessions.call_state_machine import validate_transition


def test_valid_transition():
    validate_transition("idle", "connecting")


def test_invalid_transition():
    with pytest.raises(ValueError):
        validate_transition("ended", "active")
