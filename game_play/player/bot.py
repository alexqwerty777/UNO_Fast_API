import random

from game_play.card.card import Card
from game_play.player.player import Player


class Bot:

    def __init__(self, player: Player):
        self.player = player

    def __repr__(self):
        return self.player.name

    def choose_random_color(self, last_card: Card, flip: bool = False):
        color = last_card.usual_colors
        if flip:
            color = last_card.flip_colors
        random.shuffle(color)
        return color[0]

    def make_best_move(self, last_card: Card, flip: bool = False):
        """
        Choose best move
        """

    def make_random_move(self, last_value: str, last_color: str, flip: bool = False, choosed_color = None):
        """
        """
        print(f'Cards: {self.player.card}')

        for card in self.player.card:
            print(f'Last card: {last_value}.{last_color}, current: {card}')

            cur_value = card.flip_value if flip else card.value
            cur_color = card.flip_color if flip else card.color

            if cur_value == last_value:
                self.player.card.remove(card)
                return card
            if cur_color == last_color:
                self.player.card.remove(card)
                return card
            if cur_color == 'w':
                self.player.card.remove(card)
                return card

        return None

