from __future__ import annotations

import time


def play_turns(turns: list[dict], delay_seconds: float = 0.1):
    for turn in turns:
        time.sleep(delay_seconds)
        yield turn
