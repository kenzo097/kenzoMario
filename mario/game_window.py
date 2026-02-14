from PyQt6.QtWidgets import QMainWindow
import arcade
from arcade_game import MarioGame

class GameWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Super Mario - Игра")
        self.setGeometry(100, 100, 1200, 700)
        self.parent_menu = parent
        
        self.game = MarioGame(self)
        self.game.setup()
        self.game.show()
    
    def closeEvent(self, event):
        self.game.close()
        if self.parent_menu:
            self.parent_menu.show()
        event.accept()
    
    def show_game_over(self, score, high_score):
        from main import GameOverWindow
        self.game_over_window = GameOverWindow(score, high_score, self)
        self.game_over_window.show()
        self.hide()
    
    def show_victory(self, score, high_score):
        from main import VictoryWindow
        self.victory_window = VictoryWindow(score, high_score, self)
        self.victory_window.show()
        self.hide()
