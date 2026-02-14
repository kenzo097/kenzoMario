import pygame
import random
import math

class Platform:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (139, 69, 19)
        
    def draw(self, screen, offset):
        draw_x = self.rect.x - offset[0]
        draw_y = self.rect.y - offset[1]
        pygame.draw.rect(screen, self.color, (draw_x, draw_y, self.rect.width, self.rect.height))
        pygame.draw.rect(screen, (101, 50, 14), (draw_x, draw_y, self.rect.width, 5))

class Enemy:
    def __init__(self, x, y):
        self.width = 35
        self.height = 35
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.velocity_x = -2
        self.direction = -1
        self.animation_frame = 0
        self.animation_counter = 0
        
    def update(self, platforms):
        """Обновление врага"""
        self.rect.x += self.velocity_x
        
        self.animation_counter += 0.1
        self.animation_frame = int(self.animation_counter) % 2
        
        on_platform = False
        for platform in platforms:
            if (self.rect.bottom == platform.rect.top and
                self.rect.right > platform.rect.left and
                self.rect.left < platform.rect.right):
                on_platform = True
                if (self.rect.right >= platform.rect.right or
                    self.rect.left <= platform.rect.left):
                    self.velocity_x *= -1
                break
        
        if not on_platform:
            check_x = self.rect.right if self.velocity_x > 0 else self.rect.left
            found_platform = False
            for platform in platforms:
                if (self.rect.bottom <= platform.rect.top + 10 and
                    self.rect.bottom >= platform.rect.top - 10 and
                    check_x >= platform.rect.left and
                    check_x <= platform.rect.right):
                    found_platform = True
                    break
            
            if not found_platform:
                self.velocity_x *= -1
    
    def draw(self, screen, offset):
        draw_x = self.rect.x - offset[0]
        draw_y = self.rect.y - offset[1]
        
        pygame.draw.ellipse(screen, (139, 69, 19), 
                           (draw_x, draw_y, self.width, self.height))
        
        eye_y = draw_y + 10
        pygame.draw.circle(screen, WHITE, (draw_x + 10, eye_y), 5)
        pygame.draw.circle(screen, WHITE, (draw_x + self.width - 10, eye_y), 5)
        pygame.draw.circle(screen, BLACK, (draw_x + 10, eye_y), 3)
        pygame.draw.circle(screen, BLACK, (draw_x + self.width - 10, eye_y), 3)
        
        leg_offset = 2 if self.animation_frame == 0 else -2
        pygame.draw.rect(screen, (100, 50, 10),
                        (draw_x + 5, draw_y + self.height - 5 + leg_offset, 6, 5))
        pygame.draw.rect(screen, (100, 50, 10),
                        (draw_x + self.width - 11, draw_y + self.height - 5 - leg_offset, 6, 5))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Coin:
    def __init__(self, x, y):
        self.radius = 15
        self.rect = pygame.Rect(x - self.radius, y - self.radius, 
                               self.radius * 2, self.radius * 2)
        self.animation_counter = 0
        self.collected = False
        
    def update(self):
        """Обновление монеты"""
        self.animation_counter += 0.1
        
    def draw(self, screen, offset):
        if self.collected:
            return
        
        draw_x = self.rect.centerx - offset[0]
        draw_y = self.rect.centery - offset[1]
        
        # Эффект вращения
        scale = 1.0 + 0.2 * abs(math.sin(self.animation_counter))
        
        # Монета
        pygame.draw.circle(screen, (255, 215, 0), 
                          (int(draw_x), int(draw_y)), 
                          int(self.radius * scale))
        pygame.draw.circle(screen, (255, 255, 0), 
                          (int(draw_x), int(draw_y)), 
                          int(self.radius * scale * 0.7))

class Level:
    def __init__(self, level_num):
        self.level_num = level_num
        self.width = 3000
        self.height = 800
        
        # Создаем платформы в зависимости от уровня
        self.platforms = []
        self.enemies = []
        self.coins = []
        
        self.generate_level()
    
    def generate_level(self):
        """Генерация уровня"""
        ground_height = 50
        self.platforms.append(Platform(0, self.height - ground_height, 
                                       self.width, ground_height))
        
        if self.level_num == 1:
            self.generate_level_1()
        elif self.level_num == 2:
            self.generate_level_2()
        elif self.level_num == 3:
            self.generate_level_3()
    
    def generate_level_1(self):
        """Первый уровень - простой"""
        self.platforms.append(Platform(300, 600, 200, 20))
        self.platforms.append(Platform(600, 500, 200, 20))
        self.platforms.append(Platform(900, 400, 200, 20))
        self.platforms.append(Platform(1200, 500, 200, 20))
        self.platforms.append(Platform(1500, 600, 200, 20))
        self.platforms.append(Platform(1800, 500, 200, 20))
        self.platforms.append(Platform(2100, 400, 200, 20))
        self.platforms.append(Platform(2400, 500, 200, 20))
        self.platforms.append(Platform(2700, 600, 200, 20))
        
        self.enemies.append(Enemy(350, 550))
        self.enemies.append(Enemy(650, 450))
        self.enemies.append(Enemy(950, 350))
        self.enemies.append(Enemy(1250, 450))
        self.enemies.append(Enemy(1550, 550))
        
        for i in range(15):
            x = random.randint(200, self.width - 200)
            y = random.randint(100, 600)
            self.coins.append(Coin(x, y))
    
    def generate_level_2(self):
        """Второй уровень - средний"""
        self.platforms.append(Platform(250, 550, 150, 20))
        self.platforms.append(Platform(450, 450, 150, 20))
        self.platforms.append(Platform(700, 350, 150, 20))
        self.platforms.append(Platform(950, 450, 150, 20))
        self.platforms.append(Platform(1200, 550, 150, 20))
        self.platforms.append(Platform(1450, 400, 150, 20))
        self.platforms.append(Platform(1700, 500, 150, 20))
        self.platforms.append(Platform(1950, 350, 150, 20))
        self.platforms.append(Platform(2200, 450, 150, 20))
        self.platforms.append(Platform(2450, 550, 150, 20))
        self.platforms.append(Platform(2700, 400, 150, 20))
        
        self.enemies.append(Enemy(300, 500))
        self.enemies.append(Enemy(500, 400))
        self.enemies.append(Enemy(750, 300))
        self.enemies.append(Enemy(1000, 400))
        self.enemies.append(Enemy(1250, 500))
        self.enemies.append(Enemy(1500, 350))
        self.enemies.append(Enemy(1750, 450))
        self.enemies.append(Enemy(2000, 300))
        
        for i in range(20):
            x = random.randint(200, self.width - 200)
            y = random.randint(100, 550)
            self.coins.append(Coin(x, y))
    
    def generate_level_3(self):
        """Третий уровень - сложный"""
        heights = [600, 500, 400, 300, 550, 450, 350, 500, 400, 600, 450, 350]
        for i, height in enumerate(heights):
            x = 200 + i * 220
            self.platforms.append(Platform(x, height, 180, 20))
        
        for i in range(12):
            x = 250 + i * 250
            y = random.choice([550, 450, 350, 500, 400, 300])
            self.enemies.append(Enemy(x, y - 40))
        
        for i in range(25):
            x = random.randint(200, self.width - 200)
            y = random.randint(100, 500)
            self.coins.append(Coin(x, y))
    
    def update(self):
        """Обновление уровня"""
        for enemy in self.enemies:
            enemy.update(self.platforms)
        
        for coin in self.coins:
            coin.update()
    
    def draw(self, screen, offset):
        """Отрисовка уровня"""
        for platform in self.platforms:
            if (platform.rect.right > offset[0] and 
                platform.rect.left < offset[0] + screen.get_width()):
                platform.draw(screen, offset)
        
        for enemy in self.enemies:
            if (enemy.rect.right > offset[0] and 
                enemy.rect.left < offset[0] + screen.get_width()):
                enemy.draw(screen, offset)
        
        for coin in self.coins:
            if (coin.rect.right > offset[0] and 
                coin.rect.left < offset[0] + screen.get_width()):
                coin.draw(screen, offset)
