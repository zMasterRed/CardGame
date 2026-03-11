import arcade
import settings

class TableView(arcade.View):
    def __init__(self):
        super().__init__()

        self.enemy_heart = []
        self.player_heart = []

        self.txt_enemy_c = None
        self.txt_player_c = None


        self.path_joker = ":resources:images/cards/cardJoker.png"
        self.path_card_back = ":resources:images/cards/cardBack_blue2.png"

        self.card_X = 56
        self.card_Y = 76
        
        self. setup()

    def setup(self):
        
        pos_heart = 870
        for i in range(3):
            
            e_heart = arcade.Text("♥", pos_heart + (i * 25), 375, (166, 23, 13), 20)
            self.enemy_heart.append(e_heart)

            p_heart = arcade.Text("♥", pos_heart + (i * 25), 305, (166, 23, 13), 20)
            self.player_heart.append(p_heart)

        card = ["A","2","3","4","5","6","7","8","9"]

        self.txt_enemy_c = arcade.text(
            "Enemy couples: ", 30, 500,
            arcade.color.WHITE, 14, bold = True
        )
        self.txt_player_c = arcade.text(
            "Player couples: ", 30, 400,
            arcade.color.WHITE, 14, bold = True
        )


    def on_show_view(self):
        arcade.set_background_color((5, 105, 25))
    
    def on_draw(self):

        self.clear();


        arcade.draw_line(0, settings.fY/2, settings.fX, settings.fY/2,arcade.color.WHITE, 1)


        for i in self.player_heart:
            i.draw()
        for i in self.enemy_heart:
            i.draw()

        
        self.txt_enemy_c.draw()
        self.txt_player_c.draw()



        arcade.draw_rect_outline(
            arcade.XYWH(85, 460, 75,105),
            arcade.color.WHITE,
            border_width = 2
        )
        arcade.draw_rect_outline(
            arcade.XYWH(85, 240, 75,105),
            arcade.color.WHITE,
            border_width = 2
        )
