import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QStackedWidget
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from game_widget import GameWidget

class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Super Mario")
        self.setGeometry(100, 100, 1200, 700)
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #87CEEB, stop:1 #4682B4);
            }
            QLabel {
                color: white;
                background: transparent;
            }
            QPushButton {
                background-color: #FF6B6B;
                color: white;
                border: none;
                padding: 15px 30px;
                font-size: 18px;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FF5252;
            }
            QPushButton:pressed {
                background-color: #E53935;
            }
        """)
        
        self.high_score = self.load_high_score()
        self.game_widget = None
        self.init_ui()
    
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
    
    def init_ui(self):
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        menu_widget = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(30)
        
        title = QLabel("SUPER MARIO")
        title.setFont(QFont("Arial", 72, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #FFD700; text-shadow: 3px 3px 6px rgba(0,0,0,0.5);")
        
        start_btn = QPushButton("НАЧАТЬ ИГРУ")
        start_btn.setMinimumHeight(60)
        start_btn.clicked.connect(self.start_game)
        
        if self.high_score > 0:
            score_label = QLabel(f"Рекорд: {self.high_score}")
            score_label.setFont(QFont("Arial", 24))
            score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            score_label.setStyleSheet("color: #FFD700;")
            layout.addWidget(score_label)
        
        instructions = QLabel("Стрелки - движение\nПробел - прыжок\nESC - меню")
        instructions.setFont(QFont("Arial", 16))
        instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(title)
        layout.addWidget(start_btn)
        layout.addWidget(instructions)
        
        menu_widget.setLayout(layout)
        self.stacked_widget.addWidget(menu_widget)
    
    def start_game(self):
        if self.game_widget is None:
            self.game_widget = GameWidget(self)
            self.stacked_widget.addWidget(self.game_widget)
        self.game_widget.reset_game()
        self.stacked_widget.setCurrentWidget(self.game_widget)
    
    def show_menu(self):
        self.stacked_widget.setCurrentIndex(0)
        if self.game_widget:
            self.game_widget.pause_game()

class GameOverWindow(QMainWindow):
    def __init__(self, score, high_score, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Игра окончена")
        self.setGeometry(100, 100, 1200, 700)
        self.score = score
        self.high_score = high_score
        self.parent_window = parent
        
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2C3E50, stop:1 #000000);
            }
            QLabel {
                color: white;
                background: transparent;
            }
            QPushButton {
                background-color: #3498DB;
                color: white;
                border: none;
                padding: 15px 30px;
                font-size: 18px;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
        """)
        
        self.init_ui()
    
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(30)
        
        title = QLabel("ИГРА ОКОНЧЕНА")
        title.setFont(QFont("Arial", 48, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #E74C3C;")
        
        score_label = QLabel(f"Ваши очки: {self.score}")
        score_label.setFont(QFont("Arial", 24))
        score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        high_score_label = QLabel(f"Рекорд: {self.high_score}")
        high_score_label.setFont(QFont("Arial", 24))
        high_score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        high_score_label.setStyleSheet("color: #F39C12;")
        
        menu_btn = QPushButton("В МЕНЮ")
        menu_btn.setMinimumHeight(60)
        menu_btn.clicked.connect(self.back_to_menu)
        
        layout.addWidget(title)
        layout.addWidget(score_label)
        layout.addWidget(high_score_label)
        layout.addWidget(menu_btn)
        
        central_widget.setLayout(layout)
    
    def back_to_menu(self):
        self.close()
        if self.parent_window:
            self.parent_window.show_menu()

class VictoryWindow(QMainWindow):
    def __init__(self, score, high_score, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Победа!")
        self.setGeometry(100, 100, 1200, 700)
        self.score = score
        self.high_score = high_score
        self.parent_window = parent
        
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #27AE60, stop:1 #16A085);
            }
            QLabel {
                color: white;
                background: transparent;
            }
            QPushButton {
                background-color: #E67E22;
                color: white;
                border: none;
                padding: 15px 30px;
                font-size: 18px;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #D35400;
            }
        """)
        
        self.init_ui()
    
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(30)
        
        title = QLabel("ПОБЕДА!")
        title.setFont(QFont("Arial", 72, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #FFD700; text-shadow: 3px 3px 6px rgba(0,0,0,0.5);")
        
        score_label = QLabel(f"Ваши очки: {self.score}")
        score_label.setFont(QFont("Arial", 24))
        score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        menu_btn = QPushButton("В МЕНЮ")
        menu_btn.setMinimumHeight(60)
        menu_btn.clicked.connect(self.back_to_menu)
        
        layout.addWidget(title)
        layout.addWidget(score_label)
        layout.addWidget(menu_btn)
        
        central_widget.setLayout(layout)
    
    def back_to_menu(self):
        self.close()
        if self.parent_window:
            self.parent_window.show_menu()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    menu = MainMenu()
    menu.show()
    sys.exit(app.exec())
