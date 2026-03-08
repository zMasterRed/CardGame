from src.card import Card


class CardGameError(Exception):
    pass


class InsufficientHealth(CardGameError):
    def __init__(self):
        self.message("")


class Player:
    def __init__(self, hand: list[Card], health: int = 3):
        self.hand = hand
        self.health = health

    def check_pairs(self):
        new_hand = []
        for card in self.hand:
            if card in new_hand:
                new_hand.remove(card)
            else:
                new_hand.append(card)
        self.hand = new_hand

    def decrease_health(self):
        if self.health is not 0:
            self.health = self.health - 1
        else:
            raise InsufficientHealth()
