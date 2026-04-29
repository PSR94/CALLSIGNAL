from __future__ import annotations

from pathlib import Path

import pytest

from callsignal.settings import Settings


@pytest.fixture()
def tmp_db_path(tmp_path: Path) -> Path:
    return tmp_path / "callsignal.db"
