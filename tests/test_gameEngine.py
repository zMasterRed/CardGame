from unittest.mock import patch

import pytest

from src.exceptions import PlayerNotFound
from src.gameEngine import GameEngine


class TestGameEngine:

    def test_setup_game_deck_composition(self):
        with patch("src.player.Player.check_pairs"):
            engine = GameEngine()
            # 9 coppie (18) + 1 Joker = 19
            total_cards = len(engine.player.hand) + len(engine.enemy.hand)
            assert total_cards == 19

    def test_distribution_is_correct(self):
        with patch("src.player.Player.check_pairs"):
            engine = GameEngine()
            assert len(engine.player.hand) == 9
            assert len(engine.enemy.hand) == 10

    def test_joker_exists_in_game(self):
        engine = GameEngine()
        all_cards = engine.player.hand + engine.enemy.hand
        jokers = [c for c in all_cards if c.is_joker]
        assert len(jokers) == 1
        assert jokers[0].value == 0

    def test_get_player_hand_raises_exception(self):
        engine = GameEngine()
        engine.player = None
        with pytest.raises(PlayerNotFound):
            engine.get_player_hand()

    def test_get_enemy_hand_raises_exception(self):
        engine = GameEngine()
        engine.enemy = None
        with pytest.raises(PlayerNotFound):
            engine.get_enemy_hand()

    def test_get_enemy_hand_success(self):
        engine = GameEngine()
        hand = engine.get_enemy_hand()
        assert isinstance(hand, list)
        # enemy hand can't be empty at the start
        assert len(hand) > 0

    def test_get_player_hand_success(self):
        engine = GameEngine()
        hand = engine.get_player_hand()
        assert isinstance(hand, list)
        # player hand can't be empty at the start
        assert len(hand) > 0

    @patch("random.shuffle")
    def test_shuffle_is_called(self, mock_shuffle):
        GameEngine()
        mock_shuffle.assert_called_once()

    def test_check_pairs_called_on_setup(self):
        """Check if check_pairs is called 1 time per player"""
        with patch("src.player.Player.check_pairs") as mock_check:
            GameEngine()
            assert mock_check.call_count == 2
