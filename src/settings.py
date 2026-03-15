import arcade

# Window Size
fX: int = 1000
fY: int = 700

# Button Size
bX: int = 200
bY: int = 50


def draw_exit_button() -> None:
    arcade.draw_rect_filled(
        arcade.XYWH(fX / 2, 100, bX, bY),
        arcade.color.DARK_RED,
    )
    arcade.draw_text(
        "EXIT",
        fX / 2,
        100,
        arcade.color.WHITE,
        20,
        anchor_x="center",
        anchor_y="center",
    )
def check_exit_clicked(x: float, y: float) -> bool:
    return (fX / 2 - bX / 2 < x < fX / 2 + bX / 2 and 
            100 - bY / 2 < y < 100 + bY / 2)