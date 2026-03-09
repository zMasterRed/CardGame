import arcade
import settings


class MenuView(arcade.View):
    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_GREEN)

    def on_draw(self):
        self.clear()

        arcade.draw_text(
            "CardGame",
            settings.fX / 2,
            600,
            arcade.color.WHITE,
            anchor_x="center",
            font_size=55,
        )

        arcade.draw_rect_filled(
            arcade.XYWH(settings.fX / 2, 400, settings.bX, settings.bY),
            arcade.color.LIGHT_GRAY,
        )
        arcade.draw_text(
            "Play",
            settings.fX / 2,
            400,
            arcade.color.BLACK,
            anchor_x="center",
            anchor_y="center",
            font_size=20,
        )

        arcade.draw_rect_filled(
            arcade.XYWH(settings.fX / 2, 320, settings.bX, settings.bY),
            arcade.color.LIGHT_GRAY,
        )
        arcade.draw_text(
            "Rule",
            settings.fX / 2,
            320,
            arcade.color.BLACK,
            anchor_x="center",
            anchor_y="center",
            font_size=20,
        )

        arcade.draw_rect_filled(
            arcade.XYWH(settings.fX / 2, 240, settings.bX, settings.bY),
            arcade.color.LIGHT_GRAY,
        )
        arcade.draw_text(
            "Play",
            settings.fX / 2,
            240,
            arcade.color.BLACK,
            anchor_x="center",
            anchor_y="center",
            font_size=20,
        )


def runMenu():
    window = arcade.Window(settings.fX, settings.fY, "CardGame - Menu")
    menu = MenuView()
    window.show_view(menu)
    arcade.run()
