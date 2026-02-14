from PyQt6.QtWidgets import QWidget
import arcade
from player_arcade import Player
from level_arcade import Level
import os

class MarioGame(arcade.Window):
    def __init__(self, parent_window):
        super().__init__(1200, 700, "Mario", resizable=False)
        self.parent_window = parent_window
        self.game_state = "playing"
        self.current_score = 0
        self.current_level = 1
        self.max_level = 3
        self.high_score = self.load_high_score()
        
        self.player = None
        self.level = None
        self.physics_engine = None
        self.particle_systems = []
        self.set_mouse_visible(False)
    
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
    
    def setup(self):
        arcade.set_background_color(arcade.color.SKY_BLUE)
        self.level = Level(self.current_level)
        self.player = Player(100, 100)
        
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player.sprite,
            self.level.platform_list,
            gravity_constant=0.75
        )
        
        self.camera = arcade.Camera(self.width, self.height)
        self.gui_camera = arcade.Camera(self.width, self.height)
        
        arcade.schedule(self.update_level, 0.1)
    
    def on_draw(self):
        self.clear()
        self.camera.use()
        self.level.draw()
        self.player.draw()
        
        for ps in self.particle_systems:
            ps.draw()
        
        self.gui_camera.use()
        self.draw_ui()
    
    def draw_ui(self):
        score_text = f"Очки: {self.current_score}"
        arcade.draw_text(score_text, 10, self.height - 30, 
                        arcade.color.WHITE, 24)
        
        level_text = f"Уровень: {self.current_level}"
        arcade.draw_text(level_text, 10, self.height - 60, 
                        arcade.color.WHITE, 24)
    
    def on_update(self, delta_time):
        if self.game_state != "playing":
            return
        
        self.player.update()
        self.physics_engine.update()
        
        self.level.update()
        
        for ps in self.particle_systems[:]:
            try:
                ps.update()
                if hasattr(ps, 'is_finished') and ps.is_finished():
                    self.particle_systems.remove(ps)
            except:
                try:
                    self.particle_systems.remove(ps)
                except:
                    pass
        
        self.check_collisions()
        self.update_camera()
        
        if self.player.sprite.center_x > self.level.width - 200:
            self.complete_level()
        
        if self.player.sprite.center_y < -200:
            self.game_over()
    
    def update_camera(self):
        target_x = self.player.sprite.center_x - self.width / 2
        target_y = self.player.sprite.center_y - self.height / 2
        
        self.camera.move_to((target_x, target_y))
    
    def check_collisions(self):
        coin_hit_list = arcade.check_for_collision_with_list(
            self.player.sprite, self.level.coin_list)
        
        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            self.current_score += 100
            self.add_particles(coin.center_x, coin.center_y, arcade.color.GOLD)
        
        enemy_hit_list = arcade.check_for_collision_with_list(
            self.player.sprite, self.level.enemy_list)
        
        for enemy in enemy_hit_list:
            if self.player.sprite.center_y > enemy.center_y + 10:
                enemy.remove_from_sprite_lists()
                self.current_score += 200
                self.player.sprite.change_y = 8
                self.add_particles(enemy.center_x, enemy.center_y, arcade.color.RED)
            else:
                self.game_over()
    
    def add_particles(self, x, y, color):
        try:
            texture = arcade.make_circle_texture(5, color)
            ps = arcade.Emitter(
                center_xy=(x, y),
                emit_controller=arcade.EmitBurst(15),
                particle_factory=lambda emitter: arcade.FadeParticle(
                    filename_or_texture=texture,
                    change_xy=arcade.rand_in_circle((0.0, 0.0), 5.0),
                    lifetime=1.0
                )
            )
            self.particle_systems.append(ps)
        except:
            pass
    
    def complete_level(self):
        self.current_score += 500
        if self.current_level < self.max_level:
            self.current_level += 1
            self.setup()
        else:
            self.victory()
    
    def game_over(self):
        self.game_state = "game_over"
        if self.current_score > self.high_score:
            self.high_score = self.current_score
            self.save_high_score()
        self.parent_window.show_game_over(
            self.current_score, 
            self.high_score
        )
    
    def victory(self):
        self.game_state = "victory"
        if self.current_score > self.high_score:
            self.high_score = self.current_score
            self.save_high_score()
        self.parent_window.show_victory(
            self.current_score,
            self.high_score
        )
    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.right_pressed = True
        elif key == arcade.key.SPACE or key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player.sprite.change_y = 16
                self.physics_engine.increment_jump_counter()
        elif key == arcade.key.ESCAPE:
            self.parent_window.close()
    
    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.right_pressed = False
    
    def update_level(self, delta_time):
        if self.level:
            self.level.update_enemies()
    
    def on_close(self):
        if self.parent_window:
            self.parent_window.close()
        super().on_close()
