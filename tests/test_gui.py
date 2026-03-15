from unittest.mock import MagicMock, patch

import pytest

from src.gui import MenuView, runMenu


class TestMenuView:

    # FIXTURES
    @pytest.fixture(autouse=True)
    def mock_window(self):
        with patch("src.gui.arcade.get_window") as mock_get_window:
            mock_get_window.return_value = MagicMock()
            yield mock_get_window

    @pytest.fixture(autouse=True)
    def mock_settings(self):
        with patch("src.gui.settings") as mock_sett:
            mock_sett.fX = 800
            mock_sett.fY = 600
            mock_sett.bX = 200
            mock_sett.bY = 50
            yield mock_sett

    # TESTS FOR DISPLAY
    def test_on_show_view_sets_background(self):
        with patch("src.gui.arcade.set_background_color") as mock_set_bg:
            view = MenuView()
            view.on_show_view()
            mock_set_bg.assert_called_once_with((6, 56, 138))

    def test_on_draw_calls_arcade_drawing_functions(self):
        with patch("src.gui.arcade.draw_text") as mock_draw_text, patch(
            "src.gui.arcade.draw_rect_filled"
        ) as mock_draw_rect:

            view = MenuView()
            view.on_draw()

            assert mock_draw_text.call_count == 3
            assert mock_draw_rect.call_count == 2

    # TESTS FOR MOUSE CLICKS
    @pytest.mark.parametrize(
        "click_x, click_y, expected_view_class",
        [
            (400, 400, "TableView"),
            (400, 320, "RuleView"),
        ],
    )
    def test_mouse_press_inside_buttons_changes_view(
        self, click_x, click_y, expected_view_class
    ):
        view = MenuView()
        view.window = MagicMock()

        with patch(f"src.gui.{expected_view_class}") as mock_target_view:
            mock_target_instance = mock_target_view.return_value

            view.on_mouse_press(click_x, click_y, 1, 0)

            mock_target_view.assert_called_once_with(view)
            view.window.show_view.assert_called_once_with(mock_target_instance)

    @pytest.mark.parametrize(
        "click_x, click_y",
        [
            (100, 400),
            (700, 400),
            (400, 500),
            (400, 100),
            (400, 360),
        ],
    )
    def test_mouse_press_outside_buttons_does_nothing(self, click_x, click_y):
        view = MenuView()
        view.window = MagicMock()

        view.on_mouse_press(click_x, click_y, 1, 0)

        view.window.show_view.assert_not_called()


# TEST FOR MAIN ENTRY POINT
def test_run_menu_initializes_and_runs_arcade():
    with patch("src.gui.arcade.Window") as mock_window_class, patch(
        "src.gui.MenuView"
    ) as mock_menu_class, patch("src.gui.arcade.run") as mock_run:

        mock_window_instance = mock_window_class.return_value
        mock_menu_instance = mock_menu_class.return_value

        runMenu()

        mock_window_class.assert_called_once()
        mock_menu_class.assert_called_once()
        mock_window_instance.show_view.assert_called_once_with(mock_menu_instance)
        mock_run.assert_called_once()
