from typing import Dict, List
from fastapi import WebSocket
import asyncio
import json
from .database import AsyncSessionLocal
from .services.room_service import set_room_code
from uuid import UUID

class ConnectionManager:
    def __init__(self):
        self.active: Dict[str, List[WebSocket]] = {}
        self.locks: Dict[str, asyncio.Lock] = {}

    async def connect(self, room_id: str, websocket: WebSocket):
        await websocket.accept()
        conns = self.active.setdefault(room_id, [])
        conns.append(websocket)
        self.locks.setdefault(room_id, asyncio.Lock())

    def disconnect(self, room_id: str, websocket: WebSocket):
        conns = self.active.get(room_id, [])
        if websocket in conns:
            conns.remove(websocket)
        if not conns:
            self.active.pop(room_id, None)
            self.locks.pop(room_id, None)

    async def broadcast(self, room_id: str, message: dict, sender: WebSocket | None = None):
        conns = list(self.active.get(room_id, []))
        for ws in conns:
            if ws is sender:
                continue
            try:
                await ws.send_text(json.dumps(message))
            except Exception:
                # ignore broken connections
                pass

manager = ConnectionManager()

async def websocket_endpoint(websocket: WebSocket, room_id: str):
    await manager.connect(room_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                payload = json.loads(data)
            except Exception:
                continue

            # persist latest code to DB (best-effort)
            code = payload.get("code")
            if code is not None:
                try:
                    async with AsyncSessionLocal() as db:
                        try:
                            await set_room_code(db, UUID(room_id), code)
                        except Exception:
                            # ignore DB errors for now
                            pass
                except Exception:
                    pass

            # broadcast to other clients in the room
            await manager.broadcast(room_id, payload, sender=websocket)
    except Exception:
        pass
    finally:
        manager.disconnect(room_id, websocket)
