from src.card import Card
from src.exceptions import InsufficientHealth


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
        if self.health <= 0:
            raise InsufficientHealth()
        self.health -= 1

    def is_dead(self):
        return self.health <= 0
