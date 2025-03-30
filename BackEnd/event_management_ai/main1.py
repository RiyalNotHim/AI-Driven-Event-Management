from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections = {}

    async def connect(self, websocket: WebSocket, email: str):
        await websocket.accept()
        self.active_connections[email] = websocket
        print(f"🔗 {email} connected!")

    def disconnect(self, email: str):
        if email in self.active_connections:
            del self.active_connections[email]
            print(f"❌ {email} disconnected!")

    async def send_notification(self, email: str, message: dict):
        if email in self.active_connections:
            await self.active_connections[email].send_text(json.dumps(message))

manager = ConnectionManager()

@app.websocket("/ws/{email}")
async def websocket_endpoint(websocket: WebSocket, email: str):
    await manager.connect(websocket, email)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"📩 Received from {email}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(email)

@app.get("/send-notification/")
async def send_notification(email: str, message: str):
    await manager.send_notification(email, {"notification": message})
    return {"status": "Notification sent"}
