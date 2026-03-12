import arcade

from src import settings
from src.gameEngine import GameEngine


class TableView(arcade.View):
    def __init__(self):
        super().__init__()

        self.engine = GameEngine()

        self.player_sprites = arcade.SpriteList()
        self.enemy_sprites = arcade.SpriteList()

        self.enemy_heart = []
        self.player_heart = []

        self.txt_enemy_c = None
        self.txt_player_c = None
        self.msg = None

        self.card_X = 56
        self.card_Y = 76

        self.game_status = 0  # 1 = WIN ! 2 = LOSE ! 3 = Heart WIN ! 4 = Heart LOSE

        self.setup()

    def setup(self):

        pos_heart = 870
        for i in range(3):

            e_heart = arcade.Text("♥", pos_heart + (i * 25), 375, (166, 23, 13), 20)
            self.enemy_heart.append(e_heart)

            p_heart = arcade.Text("♥", pos_heart + (i * 25), 305, (166, 23, 13), 20)
            self.player_heart.append(p_heart)

        self.txt_enemy_c = arcade.Text(
            "Enemy couples: ", 30, 375, arcade.color.WHITE, 14, bold=True
        )
        self.txt_player_c = arcade.Text(
            "Player couples: ", 30, 315, arcade.color.WHITE, 14, bold=True
        )
        self.update_cards_position()

    def update_cards_position(self):
        self.player_sprites.clear()
        self.enemy_sprites.clear()

        player_hand = self.engine.get_player_hand()
        enemy_hand = self.engine.get_enemy_hand()

        for i, card in enumerate(player_hand):
            card.center_x = 200 + (i * 60)
            card.center_y = 150
            card.flip(face_up=True)
            self.player_sprites.append(card)

        for i, card in enumerate(enemy_hand):
            card.center_x = 200 + (i * 60)
            card.center_y = 550
            card.flip(face_up=False)
            self.enemy_sprites.append(card)

    def on_show_view(self):
        arcade.set_background_color((5, 105, 25))

    def on_draw(self):
        self.clear()

        if self.game_status == 0:
            arcade.draw_line(
                0, settings.fY / 2, settings.fX, settings.fY / 2, arcade.color.WHITE, 1
            )

            for i in self.player_heart:
                i.draw()
            for i in self.enemy_heart:
                i.draw()

            self.txt_enemy_c.draw()
            self.txt_player_c.draw()

            self.player_sprites.draw()
            self.enemy_sprites.draw()

            arcade.draw_rect_outline(
                arcade.XYWH(85, 460, 75, 105), arcade.color.WHITE, border_width=2
            )
            arcade.draw_rect_outline(
                arcade.XYWH(85, 240, 75, 105), arcade.color.WHITE, border_width=2
            )
        else:
            if self.game_status == 1:
                self.msg = arcade.Text(
                    "YOU WIN THE GAME !!",
                    settings.fX / 2,
                    settings.fY / 2 + 200,
                    arcade.color.YELLOW,
                    40,
                    align="center",
                    anchor_x="center",
                    anchor_y="center",
                )
            elif self.game_status == 2:
                self.msg = arcade.Text(
                    "Oh noo\nGame Over\nTry again !!",
                    settings.fX / 2,
                    settings.fY / 2 + 200,
                    arcade.color.YELLOW,
                    40,
                    align="center",
                    anchor_x="center",
                    anchor_y="center",
                    multiline=True,
                    width=settings.fX,
                )
            elif self.game_status == 3:
                self.msg = arcade.Text(
                    "YOU WIN !!\nOpponent has no lives left",
                    settings.fX / 2,
                    settings.fY / 2 + 200,
                    arcade.color.YELLOW,
                    40,
                    align="center",
                    anchor_x="center",
                    anchor_y="center",
                    multiline=True,
                    width=settings.fX,
                )
            elif self.game_status == 4:
                self.msg = arcade.Text(
                    "Game Over\nNo lives remaining\ntry again !!",
                    settings.fX / 2,
                    settings.fY / 2 + 200,
                    arcade.color.YELLOW,
                    40,
                    align="center",
                    anchor_x="center",
                    anchor_y="center",
                    multiline=True,
                    width=settings.fX,
                )

            self.msg.draw()

            arcade.draw_rect_filled(
                arcade.XYWH(settings.fX / 2, 100, settings.bX, settings.bY),
                arcade.color.DARK_RED,
            )
            arcade.draw_text(
                "EXIT",
                settings.fX / 2,
                100,
                arcade.color.WHITE,
                20,
                anchor_x="center",
                anchor_y="center",
            )

    def lose_heart(self, is_player: bool):
        game_over = self.engine.apply_damage(is_player)

        target = self.engine.player if is_player else self.engine.enemy
        heart_txt = self.player_heart if is_player else self.enemy_heart

        ptr = target.health
        if 0 <= ptr < len(heart_txt):
            heart_txt[ptr].color = arcade.color.BLACK

        if game_over:
            if is_player:
                self.game_status = 4
            else:
                self.game_status = 3

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if self.game_status == 0:

            print("Game function")

        else:
            if (
                settings.fX / 2 - settings.bX / 2
                < x
                < settings.fX / 2 + settings.bX / 2
                and 100 - settings.bY / 2 < y < 100 + settings.bY / 2
            ):
                from src.gui import MenuView

                self.window.show_view(MenuView())
