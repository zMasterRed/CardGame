import arcade

from src import settings
from src.rule import RuleView
from src.table import TableView


class MenuView(arcade.View):
    def on_show_view(self):
        arcade.set_background_color((6, 56, 138))

    def on_draw(self):
        self.clear()

        arcade.draw_text(
            "OldMaid",
            settings.fX / 2,
            600,
            arcade.color.WHITE_SMOKE,
            anchor_x="center",
            font_size=55,
            bold=True,
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
            "Rules",
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
            "History",
            settings.fX / 2,
            240,
            arcade.color.BLACK,
            anchor_x="center",
            anchor_y="center",
            font_size=20,
        )

    # in arcade version 3.0+ x, y are float, int otherwise
    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        bY2 = settings.bY / 2

        bLeft = settings.fX / 2 - settings.bX / 2
        bRight = settings.fX / 2 + settings.bX / 2

        if bLeft < x < bRight:

            # Play Button
            topPlay = 400 + bY2
            bottomPlay = 400 - bY2
            # Rule Button
            topRule = 320 + bY2
            bottomRule = 320 - bY2
            # History Button
            topHistory = 240 + bY2
            bottomHistory = 240 - bY2

            if bottomPlay < y < topPlay:
                # open Table
                table = TableView(self)
                self.window.show_view(table)

            if bottomRule < y < topRule:
                # open Rule
                rule = RuleView(self)
                self.window.show_view(rule)

            if bottomHistory < y < topHistory:
                # open History
                print("History")


def runMenu():
    window = arcade.Window(settings.fX, settings.fY, "OldMaid - Menu")
    menu = MenuView()
    window.show_view(menu)
    arcade.run()
