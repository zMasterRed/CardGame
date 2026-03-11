import arcade
import settings

class TableView(arcade.View):
    def __init__(self):
        super().__init__()

        self.enemy_heart = []
        self.player_heart = []

        self. setup()

    def setup(self):
        
        pos_heart = 870
        for i in range(3):
            
            e_heart = arcade.Text("♥", pos_heart + (i * 25), 385, (166, 23, 13), 20)
            self.enemy_heart.append(e_heart)

            p_heart = arcade.Text("♥", pos_heart + (i * 25), 315, (166, 23, 13), 20)
            self.player_heart.append(p_heart)

    def on_show_view(self):
        arcade.set_background_color((5, 105, 25))
    
    def on_draw(self):
        self.clear();

        for i in self.player_heart:
            i.draw()
        for i in self.enemy_heart:
            i.draw()
