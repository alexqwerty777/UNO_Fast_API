import logging
import sys

from fastapi import WebSocket
import logging

sys.path.append('D:\\PythonProjects\\FastApi\\UNO_game\\game_play')
sys.path.append('D:\\PythonProjects\\FastApi\\UNO_game\\game_play\\card')
from player import Player
from game import Game


# adding Folder_2/subfolder to the system path

class WebPlayer(Player):

    def __init__(self, name: str, websocket: WebSocket, room_id: int):
        super().__init__(name=name)
        # self.name = name
        self.websocket = websocket
        self.room_id = room_id

    def __repr__(self):
        return self.name


class Room:

    def __init__(self, room_id: int):
        self.id = room_id
        self.players = []
        self.game = Game()


class ConnectionManager:
    MAX_PLAYER = 3

    def __init__(self):
        self.active_connections: list[WebSocket] = []
        self.players: dict = {}
        self.room: dict = {}
        self.cur_room_id = 1
        self.room[self.cur_room_id] = Room(self.cur_room_id)

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        player = self.players.get(websocket)
        self.active_connections.remove(websocket)
        del self.players[websocket]
        self.room[player.room_id].remove(player)
        if not self.room[player.room_id]:
            # last player in room left the game
            del self.room[player.room_id]

    async def add_player(self, name: str, websocket: WebSocket):
        if websocket not in self.players.keys():
            player = WebPlayer(name, websocket, self.cur_room_id)
            self.players[websocket] = player
            self.room[self.cur_room_id].players.append(player)
            logging.info(f'Player {name} add to room {self.cur_room_id}. '
                         f'There are {len(self.room.get(self.cur_room_id))} players')
            await self.send_personal_message('Registration success', websocket)

            # if players in current room == MAX
            if len(self.room.get(self.cur_room_id)) >= self.MAX_PLAYER:
                self.cur_room_id += 1
                self.room[self.cur_room_id] = Room(self.cur_room_id)
        else:
            logging.info(f'Websocket {websocket} rty registration but already exist')

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def send_message_to_room(self, message: str, room_id: int):
        for player in self.room[room_id]:
            await player.websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def start_game(self, room_id: int):
        for player in self.room[room_id].players:
            self.room[room_id].game.add_player(player)
        self.room[room_id].game.start_round()
        await self.send_message_to_room(f"Let's start the UNO game with {self.room[room_id].players}", room_id)

    async def send_cards(self, room_id: int):
        for player in self.room[room_id].players:
            await player.websocket.send_text(f'Cards: {self.room[room_id].game.player.card}')
