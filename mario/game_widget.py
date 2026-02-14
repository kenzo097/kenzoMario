from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QPainter, QColor, QPen, QBrush
import arcade
from player_arcade import Player
from level_arcade import Level
import math

class GameWidget(QWidget):
    def __init__(self, parent_menu):
        super().__init__()
        self.parent_menu = parent_menu
        self.game_state = "playing"
        self.current_score = 0
        self.current_level = 1
        self.max_level = 3
        self.high_score = self.load_high_score()
        
        self.player = None
        self.level = None
        self.physics_engine = None
        self.particles = []
        
        self.camera_x = 0
        self.camera_y = 0
        
        self.keys_pressed = set()
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)
        self.timer.start(16)
        
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setup_game()
    
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
    
    def save_high_score(self):
        try:
            with open("data.txt", "w", encoding="utf-8") as f:
                f.write(f"Рекорд: {self.high_score}\n")
                f.write(f"Последний уровень: {self.current_level}\n")
        except:
            pass
    
    def setup_game(self):
        self.level = Level(self.current_level)
        self.player = Player(100, 100)
        
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player.sprite,
            self.level.platform_list,
            gravity_constant=0.75
        )
    
    def reset_game(self):
        self.current_score = 0
        self.current_level = 1
        self.game_state = "playing"
        self.setup_game()
    
    def pause_game(self):
        self.timer.stop()
    
    def resume_game(self):
        self.timer.start(16)
    
    def update_game(self):
        if self.game_state != "playing":
            return
        
        if self.player:
            self.player.update(self.keys_pressed)
            if self.physics_engine:
                self.physics_engine.update()
        
        if self.level:
            self.level.update()
        
        self.update_particles()
        self.check_collisions()
        self.update_camera()
        
        if self.player and self.player.sprite.center_x > self.level.width - 200:
            self.complete_level()
        
        if self.player and self.player.sprite.center_y < -100:
            self.game_over()
        
        self.update()
    
    def update_camera(self):
        if self.player:
            level_height = self.level.height if self.level else 800
            target_x = self.player.sprite.center_x - self.width() / 2
            target_y = level_height - self.player.sprite.center_y - self.height() / 2
            
            self.camera_x += (target_x - self.camera_x) * 0.1
            self.camera_y += (target_y - self.camera_y) * 0.1
            
            if self.camera_x < 0:
                self.camera_x = 0
            if self.camera_y < 0:
                self.camera_y = 0
    
    def check_collisions(self):
        if not self.player or not self.level:
            return
        
        coin_hit_list = arcade.check_for_collision_with_list(
            self.player.sprite, self.level.coin_list)
        
        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            self.current_score += 100
            self.add_particles(coin.center_x, coin.center_y, QColor(255, 215, 0))
        
        enemy_hit_list = arcade.check_for_collision_with_list(
            self.player.sprite, self.level.enemy_list)
        
        for enemy in enemy_hit_list:
            if self.player.sprite.center_y > enemy.center_y + 10:
                enemy.remove_from_sprite_lists()
                self.current_score += 200
                self.player.sprite.change_y = 8
                self.add_particles(enemy.center_x, enemy.center_y, QColor(255, 0, 0))
            else:
                self.game_over()
    
    def add_particles(self, x, y, color):
        import random
        for _ in range(15):
            self.particles.append({
                'x': x,
                'y': y,
                'vx': random.uniform(-3, 3),
                'vy': random.uniform(-5, -1),
                'life': 1.0,
                'color': color,
                'size': random.randint(3, 8)
            })
    
    def update_particles(self):
        for p in self.particles[:]:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['vy'] -= 0.3
            p['life'] -= 0.02
            if p['life'] <= 0:
                self.particles.remove(p)
    
    def complete_level(self):
        self.current_score += 500
        if self.current_level < self.max_level:
            self.current_level += 1
            self.setup_game()
        else:
            self.victory()
    
    def game_over(self):
        self.game_state = "game_over"
        self.timer.stop()
        if self.current_score > self.high_score:
            self.high_score = self.current_score
            self.save_high_score()
        from main import GameOverWindow
        self.game_over_window = GameOverWindow(self.current_score, self.high_score, self.parent_menu)
        self.game_over_window.show()
        self.hide()
    
    def victory(self):
        self.game_state = "victory"
        self.timer.stop()
        if self.current_score > self.high_score:
            self.high_score = self.current_score
            self.save_high_score()
        from main import VictoryWindow
        self.victory_window = VictoryWindow(self.current_score, self.high_score, self.parent_menu)
        self.victory_window.show()
        self.hide()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        painter.fillRect(self.rect(), QColor(135, 206, 235))
        
        level_height = self.level.height if self.level else 800
        widget_height = self.height()
        
        painter.translate(-self.camera_x, -self.camera_y)
        
        if self.level:
            for platform in self.level.platform_list:
                y = level_height - platform.center_y
                painter.fillRect(
                    int(platform.center_x - platform.width / 2),
                    int(y - platform.height / 2),
                    int(platform.width),
                    int(platform.height),
                    QColor(139, 69, 19)
                )
            
            for coin in self.level.coin_list:
                y = level_height - coin.center_y
                painter.setBrush(QBrush(QColor(255, 215, 0)))
                painter.setPen(Qt.PenStyle.NoPen)
                painter.drawEllipse(
                    int(coin.center_x - coin.width / 2),
                    int(y - coin.height / 2),
                    int(coin.width),
                    int(coin.height)
                )
            
            for enemy in self.level.enemy_list:
                y = level_height - enemy.center_y
                painter.setBrush(QBrush(QColor(101, 67, 33)))
                painter.setPen(Qt.PenStyle.NoPen)
                painter.drawEllipse(
                    int(enemy.center_x - enemy.width / 2),
                    int(y - enemy.height / 2),
                    int(enemy.width),
                    int(enemy.height)
                )
        
        if self.player:
            y = level_height - self.player.sprite.center_y
            painter.setBrush(QBrush(QColor(255, 0, 0)))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRect(
                int(self.player.sprite.center_x - self.player.sprite.width / 2),
                int(y - self.player.sprite.height / 2),
                int(self.player.sprite.width),
                int(self.player.sprite.height)
            )
        
        painter.resetTransform()
        
        for p in self.particles:
            if p['life'] > 0:
                alpha = int(255 * p['life'])
                color = QColor(p['color'].red(), p['color'].green(), p['color'].blue(), alpha)
                painter.setBrush(QBrush(color))
                painter.setPen(Qt.PenStyle.NoPen)
                size = int(p['size'] * p['life'])
                if size > 0:
                    py = level_height - p['y']
                    painter.drawEllipse(
                        int(p['x'] - self.camera_x - size / 2),
                        int(py - self.camera_y - size / 2),
                        size, size
                    )
        
        painter.setPen(QPen(QColor(255, 255, 255)))
        painter.setFont(QFont("Arial", 24))
        painter.drawText(10, 30, f"Очки: {self.current_score}")
        painter.drawText(10, 60, f"Уровень: {self.current_level}")
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Left or event.key() == Qt.Key.Key_A:
            self.keys_pressed.add('left')
        elif event.key() == Qt.Key.Key_Right or event.key() == Qt.Key.Key_D:
            self.keys_pressed.add('right')
        elif event.key() == Qt.Key.Key_Space or event.key() == Qt.Key.Key_Up or event.key() == Qt.Key.Key_W:
            if self.physics_engine and self.physics_engine.can_jump():
                self.player.sprite.change_y = 16
                self.physics_engine.increment_jump_counter()
        elif event.key() == Qt.Key.Key_Escape:
            self.parent_menu.show_menu()
    
    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key.Key_Left or event.key() == Qt.Key.Key_A:
            self.keys_pressed.discard('left')
        elif event.key() == Qt.Key.Key_Right or event.key() == Qt.Key.Key_D:
            self.keys_pressed.discard('right')
    
    def focusOutEvent(self, event):
        self.keys_pressed.clear()
