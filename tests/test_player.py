from unittest.mock import MagicMock

import pytest

from src.card import Card
from src.exceptions import InsufficientHealth
from src.player import Player


class TestPlayer:

    def test_player_initialization(self):
        mock_card = MagicMock(spec=Card)
        hand = [mock_card]
        player = Player(hand=hand)

        assert player.hand == hand
        assert player.health == 3

    def test_check_pairs_removes_duplicates(self):
        card1 = MagicMock(spec=Card)
        card2 = MagicMock(spec=Card)

        player = Player(hand=[card1, card2, card1])
        player.check_pairs()

        assert len(player.hand) == 1
        assert card2 in player.hand
        assert card1 not in player.hand

    def test_check_pairs_empty_hand(self):
        player = Player(hand=[])
        player.check_pairs()
        assert player.hand == []

    def test_decrease_health_success(self):
        player = Player(hand=[], health=3)
        player.decrease_health()
        assert player.health == 2

    def test_decrease_health_to_zero(self):
        player = Player(hand=[], health=1)
        player.decrease_health()
        assert player.health == 0

    def test_decrease_health_raises_exception(self):
        player = Player(hand=[], health=0)

        with pytest.raises(InsufficientHealth):
            player.decrease_health()
