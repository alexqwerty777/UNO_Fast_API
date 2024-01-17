from fastapi import WebSocket
import logging

# sys.path.append('D:\\PythonProjects\\FastApi\\UNO_game\\game_play')
# sys.path.append('D:\\PythonProjects\\FastApi\\UNO_game\\game_play\\card')
# from player import Player
# from game import Game

from web.Fast_API.game_play.game import game
from web.Fast_API.game_play.player import player

logging.basicConfig(level=logging.INFO, filename="web/Fast_API/log.log", filemode="w")

# adding Folder_2/subfolder to the system path

class WebPlayer(player.Player):

    def __init__(self, name: str, websocket: WebSocket, room_id: int):
        super().__init__(name=name)
        # self.name = name
        self.websocket = websocket
        self.room_id = room_id

    def __repr__(self):
        return self.name

    def send_your_card(self):
      return self.send_message(f'Your_cards: {self.card}')

    def send_message(self, message: str):
        return self.websocket.send_text(message)

class Room:

    def __init__(self, room_id: int):
        self.id = room_id
        self.players = []
        self.game = game.Game()
        self.game_started = False

    async def send_game_state(self):
        for player in self.players:
            await player.send_your_card()
            await player.send_message(f'Stack: {self.game.stack.card}')
            await player.send_message(f'Last card in stack: {self.game.cur_card}')
            if player == self.game.cur_player:
                await player.send_message(f'Your move')
            else:
                await player.send_message(f'Player {self.game.cur_player} move')

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
        self.room[player.room_id].players.remove(player)
        if not self.room[player.room_id]:
            # last player in room left the game
            del self.room[player.room_id]

    async def add_player(self, name: str, websocket: WebSocket):
        if websocket not in self.players.keys():
            player = WebPlayer(name, websocket, self.cur_room_id)
            self.players[websocket] = player
            self.room[self.cur_room_id].players.append(player)
            logging.info(f'Player {name} add to room {self.cur_room_id}. '
                         f'There are {len(self.room.get(self.cur_room_id).players)} players')
            await self.send_personal_message('Registration success', websocket)

            # if players in current room == MAX
            if len(self.room.get(self.cur_room_id).players) >= self.MAX_PLAYER:
                self.cur_room_id += 1
                self.room[self.cur_room_id] = Room(self.cur_room_id)
        else:
            logging.info(f'Websocket {websocket} rty registration but already exist')

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def send_message_to_room(self, message: str, room_id: int):
        for player in self.room[room_id].players:
            await player.websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def start_game(self, room_id: int):
        for player in self.room[room_id].players:
            self.room[room_id].game.add_player(player)
        self.room[room_id].game.start_round()
        self.room[room_id].game_started = True
        await self.send_message_to_room(f"Let's start the UNO game with {self.room[room_id].players}", room_id)
        await self.room[room_id].send_game_state()
        # await self.send_cards(room_id)

    # async def send_cards(self, room_id: int):
    #     for each_player in self.room[room_id].players:
    #         await each_player.websocket.send_text(f'Cards: {each_player.card}, '
    #                                               f'last card in Deck: {self.room[room_id].game.cur_card}')
    #         if each_player == self.room[room_id].game.cur_player:
    #             await each_player.websocket.send_text(f'Your move')
    #         else:
    #             await each_player.websocket.send_text(f'Player {self.room[room_id].game.cur_player} move')

    async def get_move(self, room_id, websocket: WebSocket, card_num: str):
        # player move with card. need to check
        current_player = self.players.get(websocket)
        game = self.room[room_id].game
        try:
            card_num = int(card_num)
            if card_num <= len(current_player.card):
                current_card = current_player.card[card_num - 1]
                logging.info(f'player: {current_player}, try card: {current_card}')
                if game.validate_move(
                    player=current_player,
                    card=current_card,
                ):
                    next_player = game.get_move(card=current_player.make_move(current_card), player=current_player)
                    await next_player.send_message(
                        f'Player {current_player} '
                        f'move with card {current_card}.'
                        f'Now your move')
                    await self.room[room_id].send_game_state()
                else:
                    await current_player.send_message('Incorrect move. Try another card')
        except:
            await current_player.send_message('Incorrect move. Choose your card')

        # await each_player.websocket.send_text(f'Cards: {self.room[room_id].game.player.index(each_player).card}')
