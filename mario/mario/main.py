import arcade
from game_arcade import MarioGame

class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.high_score = self.load_high_score()
    
    def load_high_score(self):
        try:
            with open("data.txt", "r", encoding="utf-8") as f:
                lines = f.readlines()
                for line in lines:
                    if "рекорд" in line.lower() or "high_score" in line.lower():
                        parts = line.split(":")
                        if len(parts) == 2:
                            return int(parts[1].strip())
        except:
            pass
        return 0
    
    def on_show(self):
        arcade.set_background_color(arcade.color.SKY_BLUE)
    
    def on_draw(self):
        self.clear()
        
        title = arcade.Text("SUPER MARIO", self.window.width / 2, self.window.height - 200,
                           arcade.color.GOLD, 72, anchor_x="center", anchor_y="center",
                           bold=True)
        title.draw()
        
        text1 = arcade.Text("Нажмите SPACE для начала", self.window.width / 2, self.window.height - 350,
                           arcade.color.WHITE, 36, anchor_x="center", anchor_y="center")
        text1.draw()
        
        text2 = arcade.Text("Стрелки - движение, Пробел - прыжок", self.window.width / 2, self.window.height - 400,
                           arcade.color.WHITE, 24, anchor_x="center", anchor_y="center")
        text2.draw()
        
        if self.high_score > 0:
            score_text = arcade.Text(f"Рекорд: {self.high_score}", self.window.width / 2, self.window.height - 500,
                                    arcade.color.GOLD, 32, anchor_x="center", anchor_y="center")
            score_text.draw()
    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE or key == arcade.key.ENTER:
            game_view = MarioGame(self.high_score)
            self.window.show_view(game_view)

class GameOverView(arcade.View):
    def __init__(self, score, high_score):
        super().__init__()
        self.score = score
        self.high_score = high_score
    
    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)
    
    def on_draw(self):
        self.clear()
        
        title = arcade.Text("ИГРА ОКОНЧЕНА", self.window.width / 2, self.window.height - 250,
                           arcade.color.RED, 48, anchor_x="center", anchor_y="center",
                           bold=True)
        title.draw()
        
        score_text = arcade.Text(f"Ваши очки: {self.score}", self.window.width / 2, self.window.height - 350,
                                arcade.color.WHITE, 32, anchor_x="center", anchor_y="center")
        score_text.draw()
        
        high_text = arcade.Text(f"Рекорд: {self.high_score}", self.window.width / 2, self.window.height - 400,
                               arcade.color.GOLD, 32, anchor_x="center", anchor_y="center")
        high_text.draw()
        
        hint_text = arcade.Text("Нажмите ESC для возврата в меню", self.window.width / 2, self.window.height - 500,
                               arcade.color.WHITE, 24, anchor_x="center", anchor_y="center")
        hint_text.draw()
    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            menu_view = MenuView()
            self.window.show_view(menu_view)

class VictoryView(arcade.View):
    def __init__(self, score, high_score):
        super().__init__()
        self.score = score
        self.high_score = high_score
    
    def on_show(self):
        arcade.set_background_color(arcade.color.GREEN)
    
    def on_draw(self):
        self.clear()
        
        title = arcade.Text("ПОБЕДА!", self.window.width / 2, self.window.height - 250,
                           arcade.color.GOLD, 72, anchor_x="center", anchor_y="center",
                           bold=True)
        title.draw()
        
        score_text = arcade.Text(f"Ваши очки: {self.score}", self.window.width / 2, self.window.height - 350,
                                arcade.color.WHITE, 32, anchor_x="center", anchor_y="center")
        score_text.draw()
        
        hint_text = arcade.Text("Нажмите ESC для возврата в меню", self.window.width / 2, self.window.height - 500,
                               arcade.color.WHITE, 24, anchor_x="center", anchor_y="center")
        hint_text.draw()
    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            menu_view = MenuView()
            self.window.show_view(menu_view)

def main():
    window = arcade.Window(1200, 700, "Super Mario")
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()

if __name__ == "__main__":
    main()
