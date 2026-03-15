import arcade

from src import settings


class RuleView(arcade.View):
    def __init__(self, menu_view):
        super().__init__()
        self.menu_view = menu_view

    def on_show_view(self):
        arcade.set_background_color((6, 56, 138))

    def on_draw(self):
        self.clear()

        arcade.draw_text(
            "RULES",
            settings.fX / 2,
            600,
            arcade.color.WHITE,
            40,
            anchor_x="center",
            bold=True,
        )

        txt = "19 cards: 9 pairs + 1 Joker.\nThe first to discard all cards wins.\nWARNING! If you draw the Joker, you lose 1 heart!\nYou lose if you hold the Joker at the end or run out of hearts."

        arcade.draw_text(
            txt,
            settings.fX / 2,
            400,
            arcade.color.LIGHT_GRAY,
            20,
            anchor_x="center",
            multiline=True,
            width=600,
            align="center",
        )

        arcade.draw_rect_outline(
            arcade.XYWH(settings.fX / 2, 350, 680, 350),
            arcade.color.WHITE,
            border_width=2,
        )

        settings.draw_exit_button()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if settings.check_exit_clicked(x, y):
            self.window.show_view(self.menu_view)
