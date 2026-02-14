import pygame

class Camera:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.x = 0
        self.y = 0
        
    def update(self, player, level_width):
        """Обновление камеры - следует за игроком"""
        target_x = player.rect.centerx - self.screen_width // 2
        
        self.x += (target_x - self.x) * 0.1
        
        if self.x < 0:
            self.x = 0
        if self.x > level_width - self.screen_width:
            self.x = level_width - self.screen_width
        
        target_y = player.rect.centery - self.screen_height // 2
        
        if target_y < self.y:
            self.y = target_y
        
        if target_y > self.y + 100:
            self.y += (target_y - self.y - 100) * 0.05
        
        if self.y < 0:
            self.y = 0
    
    def get_offset(self):
        """Возвращает смещение для отрисовки"""
        return (int(self.x), int(self.y))
    
    def set_bounds(self, level_width, level_height):
        """Устанавливает границы уровня"""
        self.level_width = level_width
        self.level_height = level_height
