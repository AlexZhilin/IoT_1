
from typing import List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
temps = []

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            print('Sended', message, 'to', connection)
            await connection.send_text(message)

templates = Jinja2Templates(directory='templates')

manager = ConnectionManager()

@app.get("/")
async def get(request: Request, response_class=HTMLResponse):
    return templates.TemplateResponse('index.html', context={"request": request, "temps": temps})


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.post("/webhook")
async def webhook(item: dict):
    print(item)
    temps.append(item["uplink_message"]["decoded_payload"])
    await manager.broadcast(str(item["uplink_message"]["decoded_payload"]))
    return {"success": True}
