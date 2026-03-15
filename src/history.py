import json 
import os
import arcade

from src import settings

FILE_PATH = "history.json"

def save_game_result(result: str, player_pairs: int, hearts_left: int):
    game_data = {"result": result,
                 "pairs": player_pairs,
                 "hearts": hearts_left
                 }
    
    history = load_history()
    history.append(game_data)

    try:
        with open(FILE_PATH, "w") as f:
            json.dump(history, f, indent=4)
    except Exception as e:
        print(f"Errore nel salvataggio della cronologia: {e}")

def load_history() -> list:
    if not os.path.exists(FILE_PATH):
        return []
    try:
        with open(FILE_PATH, "r") as f:
            return json.load(f)
    except:
        return []
    
class HistoryView(arcade.View):
    def __init__(self, menu_view):
        super().__init__()
        self.menu_view = menu_view
        self.history_data = []
    def on_show_view(self):
        arcade.set_background_color((6, 56, 138))
        self.history_data = load_history()
    def on_draw(self):
        self.clear()
        arcade.draw_text(
                "HISTORY",
                settings.fX / 2,
                600,
                arcade.color.WHITE,
                40,
                anchor_x="center",
                bold=True,
            )
        arcade.draw_rect_outline(
                arcade.XYWH(settings.fX / 2, 350, 680, 350),
                arcade.color.WHITE,
                border_width=2,
            )
        last_games = self.history_data[-7:]
        start_y = 480
        if not last_games:
            arcade.draw_text(
                "No games recorded yet.",
                settings.fX / 2,
                350,
                arcade.color.LIGHT_GRAY,
                20,
                anchor_x="center"
            )
        else:
            for i, game in enumerate(reversed(last_games)):
                res_color = arcade.color.GREEN_YELLOW if "WIN" in game["result"] else arcade.color.RED_ORANGE
                
                hearts = "♥" * game["hearts"]
                txt = f"MATCH: {game['result']} | Pairs: {game['pairs']} | Health: {hearts}"
                
                arcade.draw_text(
                    txt,
                    settings.fX / 2,
                    start_y - (i * 40),
                    res_color,
                    16,
                    anchor_x="center",
                    bold=True
                )
        settings.draw_exit_button()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if (
            settings.fX / 2 - settings.bX / 2 < x < settings.fX / 2 + settings.bX / 2
            and 100 - settings.bY / 2 < y < 100 + settings.bY / 2
        ):
            self.window.show_view(self.menu_view)