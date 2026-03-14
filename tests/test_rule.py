import pytest
from unittest.mock import MagicMock, patch
from src.rule import RuleView

@pytest.fixture
def mock_settings():
    with patch('src.rule.settings') as mock_sett:
        mock_sett.fX = 800  
        mock_sett.bX = 200  
        mock_sett.bY = 50   
        yield mock_sett

def test_initialization():
    mock_menu = MagicMock()
    view = RuleView(mock_menu)
    assert view.menu_view == mock_menu

@patch('src.rule.arcade')
def test_on_show_view(mock_arcade):
    view = RuleView(MagicMock())
    view.on_show_view()

    mock_arcade.set_background_color.asser_called_once_with((6,56,138))

def test_click_on_button_exits(mock_settings):
    mock_menu = MagicMock()
    view = RuleView(mock_menu)

    view.window = MagicMock()

    center_x = 400
    center_y = 100

    view.on_mouse_press(center_x, center_y, 1, 0)

    view.window.show_view.assert_called_once_with(mock_menu)

def test_click_outside_button_does_nothing(mock_settings):
    mock_menu = MagicMock()
    view = RuleView(mock_menu)
    view.window = MagicMock()

    view.on_mouse_press(0, 800, 1, 0)

    view.window.show_view.asset_not_called()
