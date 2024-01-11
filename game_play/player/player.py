from game_play.card.card import Card


class Player:

    def __init__(self, name):
        self.name = name
        self.card = []
        # self.flip = False
        self.current_point = 0
        self.game_point = 0

    def __repr__(self):
        return self.name

    def get_card(self, card: Card):
        self.card.append(card)

    def make_move(self, card: Card):
        if card in self.card:
            self.card.remove(card)
            return card

    def add_card_point(self, flip: bool = False) -> int:
        """
        Finish this round, count points and return cards to deck
        """
        print([str(card) + str(card.get_value(flip=flip)) for card in self.card])
        points = sum([card.get_value(flip=flip) for card in self.card])
        self.game_point += points
        return points

    def drop_card_to_deck(self):
        card = self.card.copy()
        self.card.clear()
        return card

