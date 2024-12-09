from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
import asyncio

# WebSocket Connection Manager
class ConnectionManager:
    def __init__(self):
        self.active_connections = {}

    async def connect(self, websocket: WebSocket, room_key: int):
        if str(room_key) not in self.active_connections:
            self.active_connections[str(room_key)] = []
        await websocket.accept()
        self.active_connections[str(room_key)].append(websocket)

    def disconnect(self, websocket: WebSocket, room_key: int):
        if str(room_key) in self.active_connections:
            self.active_connections[str(room_key)].remove(websocket)
            if not self.active_connections[str(room_key)]:
                del self.active_connections[str(room_key)]

    async def broadcast(self, room_key: int, message: str):
        if str(room_key) in self.active_connections:
            for connection in self.active_connections[str(room_key)]:
                await connection.send_text(message)

manager = ConnectionManager()

# Router for WebSocket
router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # Keep the connection alive
    except WebSocketDisconnect:
        manager.disconnect(websocket)
