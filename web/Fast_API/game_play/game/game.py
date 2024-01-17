from web.Fast_API.game_play.card import card as cr
from web.Fast_API.game_play.card import stack
from web.Fast_API.game_play.card import deck
from web.Fast_API.game_play.player import player as pl
import logging

logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w")


class Game:

    def __init__(self):
        self.player = []
        self.deck = deck.Deck()
        self.stack = stack.Stack()
        self.flip = False
        self.game_num = 1
        self.round_num = 1
        self.cur_color = ''
        self.cur_value = ''
        self.cur_player = None
        self.cur_card = None
        self.no_card_flag = 1

    def add_player(self, player: pl.Player):
        self.player.append(player)
        logging.info(f'Player {player} join the game')

    def start_round(self) -> pl.Player:
        # give cards to hand
        logging.info(f'Start game {self.game_num}, round {self.round_num}, with players: {self.player}')
        for player in self.player:
            for i in range(7):
                player.get_card(self.deck.give_card())
            logging.info(f'{player.name} cards: {player.card}')

        # first move
        if not self.cur_player:
            self.cur_player = self.player[0]
        self.cur_card = self.deck.give_card()
        logging.info(f'First card dropped: {self.cur_card}')
        return self.get_move(self.cur_card, player=self.cur_player)

    def get_next_player(self) -> pl.Player:
        self.cur_player = self.player[(self.player.index(self.cur_player) + 1) % len(self.player)]
        return self.cur_player

    def get_move(
            self,
            card: cr.Card,
            player: pl.Player,
            selected_color: str = None
    ) -> pl.Player:
        """
        Card was dropped to stack. Perform move.
        Return next player, (who move next)
        """
        if not self.deck.card:
            self.deck.add_dropped_card(self.stack.shuffle_to_deck())
            logging.info('Deck is over. Shuffling cards from stack')

        if not card:
            # player have no suitable card
            if self.no_card_flag:
                # first time getting card from deck
                if not self.cur_value == 'find_color':
                    # second time pass the move (if not 'find color' card)
                    self.no_card_flag = 0
                self.cur_player = player
                getting_card = self.deck.give_card()
                player.get_card(getting_card)
                logging.info(f'Player {player} have no suitable card. Take card: {getting_card} from deck')
                return self.cur_player
            else:
                # player get one card and have no suitable again
                self.no_card_flag = 1
                logging.info(f'Player {player} have no suitable card again and pass the move.')
                return self.get_next_player()

        self.no_card_flag = 1

        self.cur_player = player
        self.cur_card = card
        self.stack.get_droped_card(card)
        # [1-9], '+1', 'flip', 'passed', 'revert', '+2, 'choose_color'
        self.cur_value = card.flip_value if self.flip else card.value
        # ['r','g','b','y'],['o','c','m','p'], 'w'
        self.cur_color = card.flip_color if self.flip else card.color

        if selected_color:
            self.cur_color = selected_color

        logging.info(f'Last card on stack: {self.cur_value}"{self.cur_color}"')
        # need choose color
        if self.cur_color == 'w':
            logging.info(f'Player {self.cur_player.name} select the color')
            return self.cur_player

        # taking_values
        if self.cur_value in card.taking_values:
            self.get_next_player()
            for i in range(int(self.cur_value[1])):
                self.cur_player.get_card(self.deck.give_card())
                logging.info(f'Player {self.cur_player.name} take card: {self.cur_player.card[-1]}')
            logging.info(f'Player {self.cur_player.name} pass the move')

        if self.cur_value == 'repeat':
            return self.cur_player

        # num card, next player move
        if self.cur_value in card.num_values:
            ...

        # next player pass move
        if self.cur_value == 'passed':
            self.get_next_player()
            logging.info(f'Player {self.cur_player.name} pass the move')

        if self.cur_value == 'revert':
            self.player.reverse()
            logging.info(f'Reversing the game')

        if self.cur_value == 'flip':
            self.flip = not self.flip
            # self.deck.add_dropped_card(self.stack.shuffle_to_deck())
            self.deck.card.reverse()
            last_card = self.stack.card.pop()
            self.stack.card.reverse()
            self.stack.card.append(last_card)
            logging.info(f'Flip the cards. Now flipping mode: {self.flip}')

        return self.get_next_player()

    def get_choose_color(self, color: str):
        # color validation
        if self.flip:
            if color in cr.Card.flip_colors:
                self.cur_color = color
        else:
            if color in cr.Card.usual_colors:
                self.cur_color = color

        self.get_next_player()

        if self.cur_value == '+2':
            # need to take two cards from deck and pass a move
            for i in range(2):
                self.cur_player.get_card(self.deck.give_card())
                logging.info(f'Player {self.cur_player.name} take card: {self.cur_player.card[-1]}')
            logging.info(f'Player {self.cur_player.name} pass the move')
            self.get_next_player()

        logging.info(f'Color {self.cur_color} choosed. Now player {self.cur_player} move.')
        # return self.get_move(card=self.cur_card, player=self.cur_player)

    def end_round(self) -> bool:
        for player in self.player:
            points = player.add_card_point(flip=self.flip)
            logging.info(f'Player {player} have {points} points. Total: {player.game_point}')
            self.deck.add_dropped_card(player.drop_card_to_deck())
        for player in self.player:
            if player.game_point > 500:
                logging.info(f'Player loose the game {player} have {player.game_point} points')
                # без учета если проиграли сразу двое
                return True
        self.deck.add_dropped_card(self.stack.shuffle_to_deck())
        self.round_num += 1
        return False

    def get_player_move(self, player: pl.Player, card: cr.Card):
        if self.validate_move(player, card):
            return self.get_move(card, player)
        return False

    def validate_move(self, player: pl.Player, card: cr.Card):
        card_value = card.flip_value if self.flip else card.value
        card_color = card.flip_color if self.flip else card.color
        # player moves in his turn
        if player == self.cur_player:
            # if player have no card
            if not card:
                return True
            if card_value == self.cur_value or card_color == self.cur_color:
                return True

        # try to move not in his turn
        else:
            # the same card
            if card_value == self.cur_value and card_color == self.cur_value:
                return True
        return False
