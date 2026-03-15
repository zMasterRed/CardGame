import arcade

from src import settings
from src.card import Card
from src.gameEngine import GameEngine


class TableView(arcade.View):
    def __init__(self, menu_view):
        super().__init__()

        self.menu_view = menu_view
        self.engine = GameEngine()

        # Visual groupings for rendering and interactions
        self.player_sprites = arcade.SpriteList()
        self.enemy_sprites = arcade.SpriteList()
        self.player_pairs = arcade.SpriteList()
        self.enemy_pairs = arcade.SpriteList()

        self.enemy_heart = []
        self.player_heart = []

        self.txt_enemy_c = None
        self.txt_player_c = None

        # Input lock to prevent multiple clicks while an animation is running
        self.can_draw = True

        # Reusable endgame message overlay
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
        # Initialize hearts (3 lives per player and score counters)
        pos_heart = 870
        for i in range(3):
            e_heart = arcade.Text("♥", pos_heart + (i * 25), 375, (166, 23, 13), 20)
            self.enemy_heart.append(e_heart)

            p_heart = arcade.Text("♥", pos_heart + (i * 25), 305, (166, 23, 13), 20)
            self.player_heart.append(p_heart)

        self.txt_enemy_c = arcade.Text(
            f"Enemy couples: {len(self.enemy_pairs)}",
            30,
            375,
            arcade.color.WHITE,
            14,
            bold=True,
        )
        self.txt_player_c = arcade.Text(
            f"Player couples: {len(self.player_pairs)}",
            30,
            315,
            arcade.color.WHITE,
            14,
            bold=True,
        )
        self.update_cards_position()

    def update_cards_position(self):
        # Syncs visual sprites with the logic engine current state
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
            card.flip(face_up=False)  # Hide enemy cards from the player
            self.enemy_sprites.append(card)

    def on_show_view(self):
        arcade.set_background_color((5, 105, 25))  # Classic brackground green

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

            # Outlines for the pair discard piles
            arcade.draw_rect_outline(
                arcade.XYWH(85, 460, 75, 105), arcade.color.WHITE, border_width=2
            )
            arcade.draw_rect_outline(
                arcade.XYWH(85, 240, 75, 105), arcade.color.WHITE, border_width=2
            )
        else:
            # Render endgame text based on the specific win/loss condition
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
        # Blacks out the specific heart text matching the current health index
        target = self.engine.player if is_player else self.engine.enemy
        heart_txt = self.player_heart if is_player else self.enemy_heart

        ptr = target.health
        if 0 <= ptr < len(heart_txt):
            heart_txt[ptr].color = arcade.color.BLACK

    def animated_pairs(self, card: Card, is_player: bool):
        # Temporarily move matched pairs to the center screen before moving them to score piles
        if is_player:
            card.center_x = settings.fX / 2 - 300
            card.center_y = settings.fY / 2 - 50
            self.update_cards_position()

            self.player_pairs.append(card)
            self.txt_player_c.text = f"Player pairs: {len(self.player_pairs)}"

            # Queue the final discard move
            arcade.schedule_once(lambda dt: self.final_move(card, 85, 240), 2.5)
        else:
            card.center_x = settings.fX / 2 - 300
            card.center_y = settings.fY / 2 + 50
            self.update_cards_position()
            card.flip(face_up=True)

            self.enemy_pairs.append(card)
            self.txt_enemy_c.text = f"Enemy pairs: {len(self.enemy_pairs)}"

            arcade.schedule_once(lambda dt: self.final_move(card, 85, 460), 2.5)

    def final_move(self, card: Card, x: int, y: int):
        # Callback to permanently place matched cards and check win conditions
        card.center_x = x
        card.center_y = y
        self.engine.update_game_status()

    def animated_to_draw(self, card: Card, is_player: bool):
        # Highlights the drawn card in the center of the table before adding it to the hand
        card.center_x = settings.fX / 2 - 150
        card.center_y = settings.fY / 2 - 50
        if is_player:
            card.flip(face_up=is_player)
        arcade.schedule_once(lambda dt: self.hand_move(card, is_player), 2.0)

    def hand_move(self, card: Card, is_player: bool):
        # Engine synchronization and logic resolution after the draw animation finishes
        if is_player:
            self.engine.player_draws_card(card)
            if card.is_joker:
                self.lose_heart(is_player=True)
            self.update_cards_position()

            pair = self.engine.player.check_pairs()
            if pair is not None:
                self.animated_pairs(pair, is_player)

            self.engine.switch_turn()

            arcade.schedule_once(self.enemy_draw, 2.5)  # Trigger enemy turn sequence
        else:
            if card.is_joker:
                self.lose_heart(is_player=False)
            card.flip(face_up=is_player)

            pair = self.engine.enemy.check_pairs()
            if pair is not None:
                self.animated_pairs(pair, is_player)

            self.update_cards_position()

            # Release input lock so the player can draw on their next turn
            self.can_draw = True
            self.engine.switch_turn()

        self.engine.update_game_status()

    def enemy_draw(self, _time: float):
        # Entry point for the cpu turn logic
        if self.engine.game_status == "PLAYING" and self.engine.turn == "ENEMY_TURN":
            card = self.engine.enemy_draws_card()
            if card:
                # Visually detach the chosen card from the player hand instantly
                if card in self.player_sprites:
                    self.player_sprites.remove(card)
                self.enemy_sprites.append(card)
                self.animated_to_draw(card, is_player=False)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if self.engine.game_status == "PLAYING":

            if self.engine.turn == "PLAYER_TURN":
                hit_enemy = arcade.get_sprites_at_point((x, y), self.enemy_sprites)

                # 'can_draw' acts as a debounce so the player can't spam clicks during animations
                if self.can_draw:
                    if hit_enemy:
                        self.can_draw = False
                        card = hit_enemy[-1]  # Select the top card if sprites overlap
                        self.enemy_sprites.remove(card)
                        self.player_sprites.append(card)
                        self.animated_to_draw(card, is_player=True)

            else:
                return

        else:
            # Collision detection for the "Exit" button displayed during endgame
            if (
                settings.fX / 2 - settings.bX / 2
                < x
                < settings.fX / 2 + settings.bX / 2
                and 100 - settings.bY / 2 < y < 100 + settings.bY / 2
            ):
                self.window.show_view(self.menu_view)
