from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status
from typing import Dict, Set
import json
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.schemas import RideResponse

router = APIRouter()


class ConnectionManager:
    def __init__(self):
        # Map user_id to set of WebSocket connections
        self.active_connections: Dict[str, Set[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = set()
        self.active_connections[user_id].add(websocket)
    
    def disconnect(self, websocket: WebSocket, user_id: str):
        if user_id in self.active_connections:
            self.active_connections[user_id].discard(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        await websocket.send_json(message)
    
    async def send_ride_update(self, user_id: str, ride: RideResponse):
        """Send ride update to all connections for a user"""
        if user_id in self.active_connections:
            message = {
                "type": "ride_update",
                "data": ride.model_dump()
            }
            disconnected = set()
            for connection in self.active_connections[user_id]:
                try:
                    await connection.send_json(message)
                except:
                    disconnected.add(connection)
            
            # Remove disconnected connections
            for connection in disconnected:
                self.disconnect(connection, user_id)
    
    async def broadcast(self, message: dict):
        """Broadcast message to all connected clients"""
        disconnected_users = []
        for user_id, connections in self.active_connections.items():
            disconnected = set()
            for connection in connections:
                try:
                    await connection.send_json(message)
                except:
                    disconnected.add(connection)
            
            # Remove disconnected connections
            for connection in disconnected:
                self.disconnect(connection, user_id)
                if user_id in self.active_connections and not self.active_connections[user_id]:
                    disconnected_users.append(user_id)
        
        # Clean up empty user entries
        for user_id in disconnected_users:
            if user_id in self.active_connections and not self.active_connections[user_id]:
                del self.active_connections[user_id]


manager = ConnectionManager()


async def get_current_user_from_token(token: str, db: AsyncSession):
    """Extract user from token for WebSocket authentication"""
    try:
        from jose import jwt
        import os
        from dotenv import load_dotenv
        
        load_dotenv()
        SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
        
        user = await db.get(User, user_id)
        return user
    except Exception:
        return None


@router.websocket("/ride-updates")
async def websocket_endpoint(websocket: WebSocket, token: str = None):
    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    
    # Get database session
    from app.database import AsyncSessionLocal
    async with AsyncSessionLocal() as db:
        user = await get_current_user_from_token(token, db)
        if not user:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return
        
        await manager.connect(websocket, user.id)
        
        try:
            # Send welcome message
            await manager.send_personal_message({
                "type": "connected",
                "message": f"Connected as {user.username}"
            }, websocket)
            
            # Keep connection alive and handle incoming messages
            while True:
                data = await websocket.receive_text()
                try:
                    message = json.loads(data)
                    # Handle different message types if needed
                    if message.get("type") == "ping":
                        await manager.send_personal_message({"type": "pong"}, websocket)
                except json.JSONDecodeError:
                    await manager.send_personal_message({
                        "type": "error",
                        "message": "Invalid JSON format"
                    }, websocket)
        
        except WebSocketDisconnect:
            manager.disconnect(websocket, user.id)

