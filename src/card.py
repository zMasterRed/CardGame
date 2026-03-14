import arcade


class Card(arcade.Sprite):
    def __init__(self, value: int, is_joker: bool = False) -> None:

        self.value = value
        self.is_joker = is_joker
        self.face_up = True

        self.path_front = self.get_path()
        self.path_back = ":resources:images/cards/cardBack_blue2.png"

        super().__init__(self.path_front, scale=0.4)

    def __eq__(self, other : object) -> bool:
        if not isinstance(other, Card):
            return False

        return self.value == other.value

    def get_path(self) -> str:
        if self.is_joker:
            return ":resources:images/cards/cardJoker.png"
        # C = is the Card Value
        C = "A" if self.value == 1 else str(self.value)
        return f":resources:images/cards/cardSpades{C}.png"

    def flip(self, face_up: bool) -> None:
        self.face_up = face_up
        self.texture = arcade.load_texture(
            self.path_front if face_up else self.path_back
        )

    def debug(self) -> str:
        if self.is_joker:
            return "[ JOKER ]"
        return f"[{self.value}]"

    def __hash__(self) -> int:
        return hash(id(self))
