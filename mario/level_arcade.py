import arcade
import random

class Level:
    def __init__(self, level_num):
        self.level_num = level_num
        self.width = 3000
        self.height = 800
        
        self.platform_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        
        self.generate_level()
    
    def generate_level(self):
        ground = arcade.SpriteSolidColor(self.width, 50, arcade.color.BROWN)
        ground.center_x = self.width / 2
        ground.center_y = 25
        self.platform_list.append(ground)
        
        if self.level_num == 1:
            self.generate_level_1()
        elif self.level_num == 2:
            self.generate_level_2()
        elif self.level_num == 3:
            self.generate_level_3()
    
    def generate_level_1(self):
        platforms = [
            (300, 200, 200, 20),
            (600, 300, 200, 20),
            (900, 400, 200, 20),
            (1200, 300, 200, 20),
            (1500, 200, 200, 20),
            (1800, 300, 200, 20),
            (2100, 400, 200, 20),
            (2400, 300, 200, 20),
            (2700, 200, 200, 20),
        ]
        
        for x, y, w, h in platforms:
            platform = arcade.SpriteSolidColor(w, h, arcade.color.BROWN)
            platform.center_x = x
            platform.center_y = y
            self.platform_list.append(platform)
        
        enemies = [(350, 250), (650, 350), (950, 450), (1250, 350), (1550, 250)]
        for x, y in enemies:
            enemy = arcade.SpriteSolidColor(35, 35, arcade.color.DARK_BROWN)
            enemy.center_x = x
            enemy.center_y = y
            self.enemy_list.append(enemy)
        
        for i in range(15):
            coin = arcade.SpriteSolidColor(30, 30, arcade.color.GOLD)
            coin.center_x = random.randint(200, self.width - 200)
            coin.center_y = random.randint(200, 600)
            self.coin_list.append(coin)
    
    def generate_level_2(self):
        platforms = [
            (250, 250, 150, 20), (450, 350, 150, 20), (700, 450, 150, 20),
            (950, 350, 150, 20), (1200, 250, 150, 20), (1450, 400, 150, 20),
            (1700, 300, 150, 20), (1950, 450, 150, 20), (2200, 350, 150, 20),
            (2450, 250, 150, 20), (2700, 400, 150, 20),
        ]
        
        for x, y, w, h in platforms:
            platform = arcade.SpriteSolidColor(w, h, arcade.color.BROWN)
            platform.center_x = x
            platform.center_y = y
            self.platform_list.append(platform)
        
        enemies = [(300, 300), (500, 400), (750, 500), (1000, 400), 
                   (1250, 300), (1500, 450), (1750, 350), (2000, 500)]
        for x, y in enemies:
            enemy = arcade.SpriteSolidColor(35, 35, arcade.color.DARK_BROWN)
            enemy.center_x = x
            enemy.center_y = y
            self.enemy_list.append(enemy)
        
        for i in range(20):
            coin = arcade.SpriteSolidColor(30, 30, arcade.color.GOLD)
            coin.center_x = random.randint(200, self.width - 200)
            coin.center_y = random.randint(200, 650)
            self.coin_list.append(coin)
    
    def generate_level_3(self):
        heights = [200, 300, 400, 500, 250, 350, 450, 300, 400, 200, 350, 450]
        for i, h in enumerate(heights):
            x = 200 + i * 220
            platform = arcade.SpriteSolidColor(180, 20, arcade.color.BROWN)
            platform.center_x = x
            platform.center_y = h
            self.platform_list.append(platform)
        
        for i in range(12):
            x = 250 + i * 250
            y = random.choice([250, 350, 450, 300, 400, 500])
            enemy = arcade.SpriteSolidColor(35, 35, arcade.color.DARK_BROWN)
            enemy.center_x = x
            enemy.center_y = y + 40
            self.enemy_list.append(enemy)
        
        for i in range(25):
            coin = arcade.SpriteSolidColor(30, 30, arcade.color.GOLD)
            coin.center_x = random.randint(200, self.width - 200)
            coin.center_y = random.randint(200, 700)
            self.coin_list.append(coin)
    
    def draw(self):
        self.platform_list.draw()
        self.coin_list.draw()
        self.enemy_list.draw()
    
    def update(self):
        self.update_enemies()
    
    def update_enemies(self):
        for enemy in self.enemy_list:
            if not hasattr(enemy, 'direction'):
                enemy.direction = -1
            
            enemy.center_x += enemy.direction * 2
            
            if enemy.center_x < 0 or enemy.center_x > self.width:
                enemy.direction *= -1
            
            platform_hit = arcade.check_for_collision_with_list(enemy, self.platform_list)
            if not platform_hit:
                enemy.direction *= -1
