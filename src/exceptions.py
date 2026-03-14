class CardGameError(Exception):
    """Base class for game exception"""

    pass


class InsufficientHealth(CardGameError):
    def __init__(self) -> None:
        msg = "Player has not enough health"
        super().__init__(msg)


class PlayerNotFound(CardGameError):
    def __init__(self) -> None:
        msg = "Player not found"
        super().__init__(msg)
