from __future__ import annotations

import asyncio
from collections import defaultdict
from typing import DefaultDict

from fastapi import WebSocket


class WebSocketHub:
    def __init__(self) -> None:
        self._channels: DefaultDict[str, set[WebSocket]] = defaultdict(set)
        self._lock = asyncio.Lock()

    async def connect(self, call_id: str, websocket: WebSocket) -> None:
        await websocket.accept()
        async with self._lock:
            self._channels[call_id].add(websocket)

    async def disconnect(self, call_id: str, websocket: WebSocket) -> None:
        async with self._lock:
            self._channels[call_id].discard(websocket)

    async def broadcast(self, call_id: str, payload: dict) -> None:
        async with self._lock:
            sockets = list(self._channels.get(call_id, set()))
        for websocket in sockets:
            try:
                await websocket.send_json(payload)
            except Exception:
                await self.disconnect(call_id, websocket)
