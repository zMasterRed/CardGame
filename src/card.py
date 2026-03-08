class Card:
    def __init__(self, value: int, is_joker: bool = False):

        self.value = value
        self.is_joker = is_joker

    def __eq__(self, other):

        if not isinstance(other, Card):
            return False

        return self.value == other.value

    def debug(self):

        if self.is_joker:
            return "[ JOKER ]"
        return f"[{self.value}]"
