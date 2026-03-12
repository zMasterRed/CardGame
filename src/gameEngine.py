import random
from typing import List, Optional

from src.card import Card
from src.exceptions import PlayerNotFound
from src.player import Player


class GameEngine:
    def __init__(self) -> None:
        self.deck: List[Card] = []
        self.player: Optional[Player] = None
        self.enemy: Optional[Player] = None
        self.setup_game()

    def setup_game(self) -> None:

        self.deck = [Card(value=v) for v in range(1, 10)] + [
            Card(value=v) for v in range(1, 10)
        ]
        self.deck.append(Card(value=0, is_joker=True))

        random.shuffle(self.deck)

        mid: int = len(self.deck) // 2
        self.player = Player(hand=self.deck[:mid])
        self.enemy = Player(hand=self.deck[mid:])

        self.player.check_pairs()
        self.enemy.check_pairs()

    def get_player_hand(self) -> List[Card]:

        if self.player:
            return self.player.hand
        raise PlayerNotFound()

    def get_enemy_hand(self) -> List[Card]:

        if self.enemy:
            return self.enemy.hand
        raise PlayerNotFound()

    def lose_heart(self, is_player: bool) -> bool:
        # True = Player
        # False = Enemy

        target = self.player if is_player else self.enemy

        if target:
            target.decrease_health()
            return target.is_dead()
        return False
