from __future__ import annotations


def inject_interruption(turns: list[dict]) -> list[dict]:
    replay: list[dict] = []
    for turn in turns:
        replay.append(turn)
        if turn.get("speaker") == "caller" and "supervisor" in turn.get("text", "").lower():
            replay.append({"turn_id": f"{turn['turn_id']}-interrupt", "speaker": "agent", "text": "I am routing this for review.", "kind": "final"})
    return replay
