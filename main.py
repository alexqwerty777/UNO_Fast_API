from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import logging

from web.Fast_API.server.manager.connection_manager import ConnectionManager

logging.basicConfig(level=logging.INFO, filename="web/Fast_API/log.log", filemode="w")
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
        print('Websocket')
        while True:
            data = await websocket.receive_text()
            # await websocket.send_text(f"Message text was: {data}")
            if websocket not in manager.players.keys():
                await manager.add_player(name=data, websocket=websocket)

            else:
                if data == 'start':
                    await manager.start_game(room_id=manager.players.get(websocket).room_id)
                else:
                    if manager.room[manager.players.get(websocket).room_id].game_started:
                        await manager.get_move(
                            room_id=manager.players.get(websocket).room_id,
                            websocket=websocket,
                            card_num=data,
                        )

                    # await manager.send_message_to_room(
                    #     message=f"Player {manager.players.get(websocket).name} wrote: {data}",
                    #     room_id=manager.players.get(websocket).room_id)

    except WebSocketDisconnect:
        player = manager.players.get(websocket)
        manager.disconnect(websocket)
        await manager.broadcast(f"{player} left the chat")

    #
    # except:
    #     pass
