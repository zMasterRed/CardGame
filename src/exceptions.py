class CardGameError(Exception):
    pass


class InsufficientHealth(CardGameError):
    def __init__(self):
        msg = "Player has not enough health"
        super().__init__(msg)


class PlayerNotFound(CardGameError):
    def __init__(self):
        msg = "Player not found"
        super().__init__(msg)
