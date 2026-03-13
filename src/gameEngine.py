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
        self.game_status = "PLAYING"
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

    def apply_damage(self, is_player: bool) -> bool:
        # True = Player
        # False = Enemy

        target = self.player if is_player else self.enemy

        if target:
            target.decrease_health()
            if target.is_dead():
                if is_player:
                    self.game_status = "HEART_LOSE"
                else:
                    self.game_status = "HEART_WIN"
                return True
        return False

    def player_draws_card(self, card: Card) -> None:
        """
        Move the card the player draw from enemy hand to player hand
        """
        if self.player is None or self.enemy is None:
            raise PlayerNotFound()

        if card in self.enemy.hand:
            self.enemy.hand.remove(card)
            self.player.hand.append(card)

            if card.is_joker:
                self.apply_damage(is_player=True)

            self.player.check_pairs()
            random.shuffle(self.enemy.hand)
            self.update_game_status()

    def update_game_status(self) -> None:
        """Check if someone won after this move"""
        if len(self.player.hand) == 0:
            self.game_status = "WIN"
        elif len(self.enemy.hand) == 0:
            self.game_status = "LOSE"

    def enemy_draws_card(self) -> Optional[Card]:
        """
        Enemy draws a random card from player hand,
        return it to display in the updated deck
        """
        if self.player is None or self.enemy is None:
            raise PlayerNotFound()

        if len(self.player.hand) == 0:
            return None

        random_card = random.choice(self.player.hand)
        self.player.hand.remove(random_card)
        self.enemy.hand.append(random_card)

        if random_card.is_joker:
            self.apply_damage(is_player=False)

        self.enemy.check_pairs()
        self.update_game_status()

        return random_card
