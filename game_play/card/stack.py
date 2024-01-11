from game_play.card.card import Card


class Stack:

    def __init__(self):
        # self.flip = False
        self.card = []
        self.last_card = None

    def __repr__(self):
        return self.card

    def get_droped_card(self, card) -> Card:
        self.card.append(card)
        self.last_card = card
        return card

    def shuffle_to_deck(self) -> list:
        cards_to_deck = self.card
        cards_to_deck.remove(self.last_card)
        self.card = [self.last_card]
        return cards_to_deck

    # def flip(self) -> None:
    #     self.shuffle_to_deck()
    #     self.flip = not self.flip
