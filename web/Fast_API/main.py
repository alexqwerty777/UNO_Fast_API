from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import logging

from web.Fast_API.server.manager import ConnectionManager

logging.basicConfig(level=logging.INFO, filename="log.log", filemode="w")
app = FastAPI()
manager = ConnectionManager()

html = """-"""

@app.get("/")
async def get():
    return HTMLResponse(html)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # await websocket.accept()
    try:
        await manager.connect(websocket)
        while True:
            data = await websocket.receive_text()
            # await websocket.send_text(f"Message text was: {data}")
            if not websocket in manager.players.keys():
                await manager.add_player(name=data, websocket=websocket)
            else:
                # await manager.send_personal_message(f"Player {manager.players.get(websocket).name} wrote: {data}", websocket)
                if data == 'start':
                    await manager.start_game()
                else:
                    await manager.broadcast(f'Player {manager.players.get(websocket).name}: {data}')

    except WebSocketDisconnect:
        player = manager.players[websocket]
        manager.disconnect(websocket)
        await manager.broadcast(f"{player} left the chat")

    except:
        pass
