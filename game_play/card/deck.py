import random

from game_play.card.card import Card


class Deck:
    """
    color: 'r' - red, 'g' - green, 'b' - blue, 'y' - yellow, 'w' - wild card (black)
    value: [1-9], '+1', 'flip', 'passed', 'revert', '+2, 'choose_color'
    -----------------------------
    flip_color: 'o' - orange, 'c' - cian (бирюзовый), 'm' - magenta (розовый), 'p' - purple (фиолетовый), 'w' - wild
    flip_value: [1-9], '+5', 'flip', 'repeat', 'revert', 'choose_color', 'find_color'
    """

    def __init__(self):
        # self.flip = False
        self.card = []
        face_card = []
        flip_card = []
        for color in ['r', 'g', 'b', 'y']:
            for value in range(1, 10):
                face_card.extend([(color, str(value))] * 2)
            for value in ['+1', 'flip', 'passed', 'revert']:
                face_card.extend([(color, value)] * 2)
        face_card.extend([('w', '+2')] * 4)
        face_card.extend([('w', 'choose_color')] * 4)

        for color in ['o', 'c', 'm', 'p']:
            for value in range(1, 10):
                flip_card.extend([(color, str(value))] * 2)
            for value in ['+5', 'flip', 'repeat', 'revert']:
                flip_card.extend([(color, value)] * 2)
        flip_card.extend([('w', 'find_color')] * 4)
        flip_card.extend([('w', 'choose_color')] * 4)
        
        random.shuffle(face_card)
        random.shuffle(flip_card)
        self.card = [
            Card(
                color=face_card[0],
                value=face_card[1],
                flip_color=flip_card[0],
                flip_value=flip_card[1],
            ) for face_card, flip_card in zip(face_card, flip_card)
        ]

    def __repr__(self):
        return '\n'.join([f'[{str(card)}]' for card in self.card])

    def give_card(self) -> Card:
        return self.card.pop()

    def shuffle(self) -> None:
        random.shuffle(self.card)

    def add_dropped_card(self, deck_cards: list) -> None:
        self.card.extend(deck_cards)
        self.shuffle()

    # def flip(self, deck_cards: list) -> None:
    #     self.add_dropped_card(deck_cards)
    #     self.flip = not self.flip
