from src.card import Card


def test_card_init():

    card = Card(4)
    assert card.value == 4
    assert card.is_joker is False


def test_joker_init():

    card = Card(10, True)
    assert card.value == 10
    assert card.is_joker is True


def test_cards_equality():
    c1 = Card(7)
    c2 = Card(7)
    c3 = Card(8)

    assert c1 == c2
    assert c1 != c3
    assert c1 != "7"  # testing if type value is not int


def test_debug_output():
    c1 = Card(5)
    joker = Card(0, is_joker=True)
    assert c1.debug() == "[5]"
    assert joker.debug() == "[ JOKER ]"
