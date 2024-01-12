import logging

from fastapi import WebSocket
import logging


class Player:

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return self.name


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
        self.players: dict = {}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        del self.players[websocket]

    async def add_player(self, name: str, websocket: WebSocket):
        if not websocket in self.players.keys():
            self.players[websocket] = Player(name)
            logging.info(f'Player {name} add to list')
            await self.send_personal_message('Registration success', websocket)
        else:
            logging.info(f'Websocket {websocket} rty registration but already exist')

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def start_game(self):
        await self.broadcast("Let's start the UNO game")
