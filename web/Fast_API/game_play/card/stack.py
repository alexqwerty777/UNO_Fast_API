from web.Fast_API.game_play.card import card as cr


class Stack:

    def __init__(self):
        # self.flip = False
        self.card = []
        self.last_card = None

    def __repr__(self):
        return self.card

    def get_droped_card(self, card) -> cr.Card:
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
