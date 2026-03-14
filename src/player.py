from src.card import Card
from src.exceptions import InsufficientHealth


class Player:
    def __init__(self, hand: list[Card], health: int = 3) -> None:
        self.hand = hand
        self.health = health

    def check_pairs(self) -> None:
        new_hand: list[Card] = []
        for card in self.hand:
            if card in new_hand:
                new_hand.remove(card)
            else:
                new_hand.append(card)
        self.hand = new_hand

    def decrease_health(self) -> None:
        if self.health <= 0:
            raise InsufficientHealth()
        self.health -= 1

    def is_dead(self) -> bool:
        return self.health <= 0
