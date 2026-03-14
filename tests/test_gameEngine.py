from unittest.mock import patch

import pytest

from src.card import Card
from src.exceptions import PlayerNotFound
from src.gameEngine import GameEngine


class TestGameEngine:

    # TEST FOR GAME INIT
    def test_setup_game_deck_composition(self):
        with patch("src.player.Player.check_pairs"):
            engine = GameEngine()
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

    # TEST FOR GET HAND
    @pytest.mark.parametrize(
        "target_attribute, method_name",
        [
            ("player", "get_player_hand"),
            ("enemy", "get_enemy_hand"),
        ],
    )
    def test_get_hand_raises_exception(self, target_attribute, method_name):
        engine = GameEngine()

        setattr(engine, target_attribute, None)

        get_hand_method = getattr(engine, method_name)

        with pytest.raises(PlayerNotFound):
            get_hand_method()

    @pytest.mark.parametrize(
        "method_name",
        [
            "get_player_hand",
            "get_enemy_hand",
        ],
    )
    def test_get_hand_success(self, method_name):
        engine = GameEngine()

        get_hand_method = getattr(engine, method_name)
        hand = get_hand_method()

        assert isinstance(hand, list)
        assert len(hand) > 0

    def test_shuffle_is_called(self):
        with patch("random.shuffle") as mock_shuffle:
            GameEngine()
            mock_shuffle.assert_called_once()

    def test_check_pairs_called_on_setup(self):
        """Check if check_pairs is called 1 time per player"""
        with patch("src.player.Player.check_pairs") as mock_check:
            GameEngine()
            assert mock_check.call_count == 2

    # TESTS FOR game_status UPDATES
    @pytest.mark.parametrize(
        "player_cards, enemy_cards, expected_status",
        [
            (0, 5, "WIN"),  # Player hand empty -> WIN
            (5, 0, "LOSE"),  # Enemy hand empty -> LOSE
            (5, 5, "PLAYING"),  # Both have cards -> PLAYING
        ],
    )
    def test_update_game_status(self, player_cards, enemy_cards, expected_status):
        engine = GameEngine()

        engine.player.hand = [Card(1)] * player_cards
        engine.enemy.hand = [Card(1)] * enemy_cards

        engine.update_game_status()
        assert engine.game_status == expected_status

    # TESTS FOR apply_damage
    @pytest.mark.parametrize(
        "is_player, expected_status", [(True, "HEART_LOSE"), (False, "HEART_WIN")]
    )
    def test_apply_damage_lethal(self, is_player, expected_status):
        """Test applying damage when health is 1, causing death and game over."""
        engine = GameEngine()
        target = engine.player if is_player else engine.enemy
        target.health = 1  # Set to lethal range

        is_dead = engine.apply_damage(is_player)

        assert is_dead is True
        assert target.health == 0
        assert engine.game_status == expected_status

    @pytest.mark.parametrize("is_player", [True, False])
    def test_apply_damage_non_lethal(self, is_player):
        """Test applying damage that does not reduce health to 0."""
        engine = GameEngine()
        target = engine.player if is_player else engine.enemy
        target.health = 3

        is_dead = engine.apply_damage(is_player)

        assert is_dead is False
        assert target.health == 2
        assert engine.game_status == "PLAYING"

    # TESTS FOR player_draws_card
    def test_player_draws_normal_card(self):
        engine = GameEngine()
        normal_card = Card(5)
        engine.enemy.hand = [normal_card]
        engine.player.hand = []

        with patch("random.shuffle") as mock_shuffle:
            engine.player_draws_card(normal_card)

        assert normal_card not in engine.enemy.hand
        assert normal_card in engine.player.hand
        assert engine.player.health == 3  # Normal card doesn't deal damage
        mock_shuffle.assert_called_once_with(engine.enemy.hand)

    def test_player_draws_joker_applies_damage(self):
        engine = GameEngine()
        joker = Card(0, is_joker=True)
        engine.enemy.hand = [joker]
        engine.player.hand = []
        engine.player.health = 3

        engine.player_draws_card(joker)

        assert engine.player.health == 2

    def test_player_draws_card_raises_exception_if_none(self):
        engine = GameEngine()
        engine.enemy = None
        with pytest.raises(PlayerNotFound):
            engine.player_draws_card(Card(1))

    # TESTS FOR enemy_draws_card
    def test_enemy_draws_normal_card(self):
        engine = GameEngine()
        normal_card = Card(5)
        engine.player.hand = [normal_card]
        engine.enemy.hand = []

        drawn_card = engine.enemy_draws_card()

        assert drawn_card == normal_card
        assert normal_card not in engine.player.hand
        assert normal_card in engine.enemy.hand
        assert engine.enemy.health == 3

    def test_enemy_draws_joker_applies_damage(self):
        engine = GameEngine()
        joker = Card(0, is_joker=True)
        engine.player.hand = [joker]
        engine.enemy.hand = []
        engine.enemy.health = 3

        drawn_card = engine.enemy_draws_card()

        assert drawn_card == joker
        assert engine.enemy.health == 2

    def test_enemy_draws_card_returns_none_when_player_empty(self):
        engine = GameEngine()
        engine.player.hand = []

        assert engine.enemy_draws_card() is None
