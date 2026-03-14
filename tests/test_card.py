import pytest

from src.card import Card


def test_card_init():

    card = Card(4)
    assert card.value == 4
    assert card.is_joker is False


def test_joker_init():

    card = Card(0, True)
    assert card.value == 0
    assert card.is_joker is True


def test_cards_equality():
    c1 = Card(7)
    c2 = Card(7)
    c3 = Card(8)

    assert c1 == c2
    assert c1 != c3
    assert c1 != "7"  # testing if type value is not int


def test_card_flip():
    card = Card(10)
    assert card.face_up is True

    card.flip(False)
    assert card.face_up is False
    assert card.path_back.endswith("cardBack_blue2.png")

    card.flip(True)
    assert card.face_up is True
    assert card.path_front.endswith("cardSpades10.png")


def test_get_path_joker():
    card = Card(0, is_joker=True)
    assert card.get_path() == ":resources:images/cards/cardJoker.png"
    assert card.path_front == ":resources:images/cards/cardJoker.png"


def test_get_path_ace():
    """Test if 1 becomes ace"""
    card = Card(1, is_joker=False)
    assert card.get_path() == ":resources:images/cards/cardSpadesA.png"
    assert "cardSpadesA" in card.path_front


@pytest.mark.parametrize("val", [2, 5, 9])
def test_get_path_various_numbers(val):
    """Test multiple path"""
    card = Card(val)
    assert card.get_path() == f":resources:images/cards/cardSpades{val}.png"
    assert f"{val}" in card.path_front


def test_debug_output():
    c1 = Card(5)
    joker = Card(0, is_joker=True)
    assert c1.debug() == "[5]"
    assert joker.debug() == "[ JOKER ]"
