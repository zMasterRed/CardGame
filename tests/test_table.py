from unittest.mock import MagicMock, patch

import arcade
import pytest

from src.table import TableView


class TestTableView:

    # FIXTURES
    @pytest.fixture(autouse=True)
    def mock_window(self):
        with patch("src.table.arcade.get_window") as mock_get_window:
            mock_get_window.return_value = MagicMock()
            yield mock_get_window

    @pytest.fixture(autouse=True)
    def mock_settings(self):
        with patch("src.table.settings") as mock_sett:
            mock_sett.fX = 1000
            mock_sett.fY = 700
            mock_sett.bX = 200
            mock_sett.bY = 50
            yield mock_sett

    @pytest.fixture(autouse=True)
    def mock_arcade_text(self):
        with patch(
            "src.table.arcade.Text", side_effect=lambda *args, **kwargs: MagicMock()
        ) as mock_text:
            yield mock_text

    @pytest.fixture
    def mock_engine(self):
        with patch("src.table.GameEngine") as mock_eng_class:
            mock_eng = mock_eng_class.return_value
            mock_eng.get_player_hand.return_value = []
            mock_eng.get_enemy_hand.return_value = []
            mock_eng.game_status = "PLAYING"
            mock_eng.turn = "PLAYER_TURN"
            yield mock_eng

    # TESTS FOR DISPLAY e SETUP
    @pytest.mark.usefixtures("mock_engine")
    def test_on_show_view_sets_background(self):
        with patch("src.table.arcade.set_background_color") as mock_set_bg:
            view = TableView(MagicMock())
            view.on_show_view()
            mock_set_bg.assert_called_once_with((5, 105, 25))

    def test_update_cards_position(self, mock_engine):
        mock_card1 = MagicMock()
        mock_card2 = MagicMock()
        mock_engine.get_player_hand.return_value = [mock_card1]
        mock_engine.get_enemy_hand.return_value = [mock_card2]

        view = TableView(MagicMock())

        assert len(view.player_sprites) == 1
        assert len(view.enemy_sprites) == 1

        assert mock_card1.center_x == 200
        assert mock_card1.center_y == 150
        mock_card1.flip.assert_called_once_with(face_up=True)

        assert mock_card2.center_x == 200
        assert mock_card2.center_y == 550
        mock_card2.flip.assert_called_once_with(face_up=False)

    def test_on_draw_playing_status(self, mock_engine):
        view = TableView(MagicMock())
        mock_engine.game_status = "PLAYING"

        with patch("src.table.arcade.draw_line") as mock_draw_line, patch(
            "src.table.arcade.draw_rect_outline"
        ) as mock_draw_rect:

            view.player_sprites = MagicMock()
            view.enemy_sprites = MagicMock()

            view.on_draw()

            mock_draw_line.assert_called_once()
            assert mock_draw_rect.call_count == 2
            view.player_sprites.draw.assert_called_once()

    @pytest.mark.parametrize(
        "status, expected_text",
        [
            ("WIN", "YOU WIN THE GAME !!"),
            ("LOSE", "Oh noo\nGame Over\nTry again !!"),
            ("HEART_WIN", "YOU WIN !!\nOpponent has no lives left"),
            ("HEART_LOSE", "Game Over\nNo lives remaining\ntry again !!"),
        ],
    )
    def test_on_draw_game_over_statuses(self, mock_engine, status, expected_text):
        view = TableView(MagicMock())
        mock_engine.game_status = status

        with patch("src.table.settings.draw_exit_button") as mock_exit_btn:

            view.on_draw()

            assert view.msg.text == expected_text
            mock_exit_btn.assert_called_once()

    # TESTS FOR GAME LOGIC
    def test_lose_heart_changes_color(self, mock_engine):
        view = TableView(MagicMock())
        mock_engine.player.health = 2

        view.lose_heart(is_player=True)

        assert view.player_heart[2].color == arcade.color.BLACK

    # TESTS FOR MOUSE CLICKS
    def test_on_mouse_press_draws_card(self, mock_engine):
        view = TableView(MagicMock())
        mock_engine.game_status = "PLAYING"
        mock_engine.turn = "PLAYER_TURN"

        view.can_draw = True

        mock_card = MagicMock()
        view.enemy_sprites.append(mock_card)

        with patch(
            "src.table.arcade.get_sprites_at_point"
        ) as mock_get_sprites, patch.object(view, "animated_to_draw") as mock_animated:

            mock_get_sprites.return_value = [mock_card]

            view.on_mouse_press(100, 100, 1, 0)

            assert view.can_draw is False
            assert mock_card not in view.enemy_sprites
            assert mock_card in view.player_sprites
            mock_animated.assert_called_once_with(mock_card, is_player=True)

    def test_on_mouse_press_exit_button(self, mock_engine):
        mock_menu = MagicMock()
        view = TableView(mock_menu)
        view.window = MagicMock()

        mock_engine.game_status = "LOSE"

        view.on_mouse_press(500, 100, 1, 0)

        view.window.show_view.assert_called_once_with(mock_menu)
