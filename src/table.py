import arcade

from src import settings
from src.gameEngine import GameEngine


class TableView(arcade.View):
    def __init__(self, menu_view):
        super().__init__()

        self.menu_view = menu_view

        self.engine = GameEngine()

        self.player_sprites = arcade.SpriteList()
        self.enemy_sprites = arcade.SpriteList()

        self.player_pairs = arcade.SpriteList()
        self.enemy_pairs = arcade.SpriteList() 

        self.enemy_heart = []
        self.player_heart = []

        self.txt_enemy_c = None
        self.txt_player_c = None

        self.card_X = 56
        self.card_Y = 76

        self.msg = arcade.Text(
            "",
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

        if self.engine.game_status == "PLAYING":
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

            self.player_pairs.draw()
            self.enemy_pairs.draw()

            arcade.draw_rect_outline(
                arcade.XYWH(85, 460, 75, 105), arcade.color.WHITE, border_width=2
            )
            arcade.draw_rect_outline(
                arcade.XYWH(85, 240, 75, 105), arcade.color.WHITE, border_width=2
            )
        else:
            if self.engine.game_status == "WIN":
                self.msg.text = "YOU WIN THE GAME !!"
            elif self.engine.game_status == "LOSE":
                self.msg.text = "Oh noo\nGame Over\nTry again !!"
            elif self.engine.game_status == "HEART_WIN":
                self.msg.text = "YOU WIN !!\nOpponent has no lives left"
            elif self.engine.game_status == "HEART_LOSE":
                self.msg.text = "Game Over\nNo lives remaining\ntry again !!"

            self.msg.draw()

            settings.draw_exit_button()

    def lose_heart(self, is_player: bool):
        self.engine.apply_damage(is_player)

        target = self.engine.player if is_player else self.engine.enemy
        heart_txt = self.player_heart if is_player else self.enemy_heart

        ptr = target.health
        if 0 <= ptr < len(heart_txt):
            heart_txt[ptr].color = arcade.color.BLACK
    
    def animated_card(self, card: arcade.Sprite, is_player: bool):
        if is_player:
            card.center_x = settings.fX / 2 - 300
            card.center_y = settings.fY / 2 - 50

            self.player_pairs.append(card)

            arcade.schedule_once(lambda dt: self.final_move(card, 85, 240), 2.5)
        else:
            card.center_x = settings.fX/2 - 300
            card.center_y = settings.fY/2 + 50
            card.flip(face_up=True)

            self.enemy_pairs.append(card)

            arcade.schedule_once(lambda dt: self.final_move(card,85,460), 2.5)

    def final_move(self, card: arcade.Sprite, x: int, y: int):
        card.center_x = x
        card.center_y = y
        


    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if self.engine.game_status == "PLAYING":

            # Controllo carte giocatore
            hit_player = arcade.get_sprites_at_point((x, y), self.player_sprites)
            if hit_player:
                self.animated_card(hit_player[-1], is_player= True)
                return # Esci dopo aver trovato la carta

            # Controllo carte avversario
            hit_enemy = arcade.get_sprites_at_point((x, y), self.enemy_sprites)
            if hit_enemy:
                self.animated_card(hit_enemy[-1], is_player =False)

        else:
            if (
                settings.fX / 2 - settings.bX / 2
                < x
                < settings.fX / 2 + settings.bX / 2
                and 100 - settings.bY / 2 < y < 100 + settings.bY / 2
            ):
                self.window.show_view(self.menu_view)
