import arcade
from player_arcade import Player
from level_arcade import Level

class MarioGame(arcade.View):
    def __init__(self, high_score):
        super().__init__()
        self.game_state = "playing"
        self.current_score = 0
        self.current_level = 1
        self.max_level = 3
        self.high_score = high_score
        
        self.particle_systems = []
        
        self.level = Level(self.current_level)
        self.player = Player(100, 150)
        
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player.sprite)
        
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player.sprite,
            self.level.platform_list,
            gravity_constant=0.75
        )
        
        self.camera = None
        self.gui_camera = None
    
    def on_show_view(self):
        arcade.set_background_color(arcade.color.SKY_BLUE)
        if self.window:
            from arcade.camera import Camera2D
            self.camera = Camera2D(window=self.window)
            self.gui_camera = Camera2D(window=self.window)
            self.camera.position = (0, 0)
    
    def on_draw(self):
        self.clear()
        
        if not self.camera or not self.gui_camera:
            return
        
        self.camera.use()
        
        if self.level and self.player:
            self.level.platform_list.draw()
            self.level.coin_list.draw()
            self.level.enemy_list.draw()
            self.player_list.draw()
        
        for ps in self.particle_systems:
            ps.draw()
        
        self.gui_camera.use()
        score_text = arcade.Text(f"Очки: {self.current_score}", 10, self.window.height - 30, 
                                arcade.color.WHITE, 24)
        score_text.draw()
        level_text = arcade.Text(f"Уровень: {self.current_level}", 10, self.window.height - 60, 
                                arcade.color.WHITE, 24)
        level_text.draw()
    
    def on_update(self, delta_time):
        if not self.camera or not self.player or not self.level or self.game_state != "playing":
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
        
        if self.player.sprite.center_y < -100:
            self.game_over()
    
    def update_camera(self):
        if not self.camera:
            return
        
        player_x = self.player.sprite.center_x
        player_y = self.player.sprite.center_y
        
        offset_x = 100 if self.player.sprite.change_x > 0 else -100 if self.player.sprite.change_x < 0 else 0
        
        target_x = player_x - self.window.width / 2 + offset_x
        target_y = player_y - self.window.height / 2
        
        if target_x < 0:
            target_x = 0
        if target_x > self.level.width - self.window.width:
            target_x = self.level.width - self.window.width
        
        if target_y < 0:
            target_y = 0
        if target_y > self.level.height - self.window.height:
            target_y = self.level.height - self.window.height
        
        self.camera.position = (target_x, target_y)
    
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
            self.level = Level(self.current_level)
            self.player = Player(100, 150)
            self.player_list = arcade.SpriteList()
            self.player_list.append(self.player.sprite)
            self.physics_engine = arcade.PhysicsEnginePlatformer(
                self.player.sprite,
                self.level.platform_list,
                gravity_constant=0.75
            )
            from arcade.camera import Camera2D
            self.camera = Camera2D(window=self.window)
            self.gui_camera = Camera2D(window=self.window)
        else:
            self.victory()
    
    def game_over(self):
        self.game_state = "game_over"
        if self.current_score > self.high_score:
            self.high_score = self.current_score
            self.save_high_score()
        from main import GameOverView
        game_over_view = GameOverView(self.current_score, self.high_score)
        self.window.show_view(game_over_view)
    
    def victory(self):
        self.game_state = "victory"
        if self.current_score > self.high_score:
            self.high_score = self.current_score
            self.save_high_score()
        from main import VictoryView
        victory_view = VictoryView(self.current_score, self.high_score)
        self.window.show_view(victory_view)
    
    def save_high_score(self):
        try:
            with open("data.txt", "w", encoding="utf-8") as f:
                f.write(f"Рекорд: {self.high_score}\n")
                f.write(f"Последний уровень: {self.current_level}\n")
        except:
            pass
    
    def on_key_press(self, key, modifiers):
        if not self.player or not self.physics_engine:
            return
        
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.right_pressed = True
        elif key == arcade.key.SPACE or key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player.sprite.change_y = 16
                self.physics_engine.increment_jump_counter()
        elif key == arcade.key.ESCAPE:
            from main import MenuView
            menu_view = MenuView()
            self.window.show_view(menu_view)
    
    def on_key_release(self, key, modifiers):
        if not self.player:
            return
        
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.right_pressed = False
