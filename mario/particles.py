import pygame
import random
import math

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.velocity_x = random.uniform(-3, 3)
        self.velocity_y = random.uniform(-5, -1)
        self.life = 1.0
        self.decay = random.uniform(0.02, 0.05)
        self.size = random.randint(3, 8)
        
    def update(self):
        """Обновление частицы"""
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.velocity_y += 0.3
        self.life -= self.decay
        
    def draw(self, screen, offset):
        """Отрисовка частицы"""
        if self.life > 0:
            draw_x = int(self.x - offset[0])
            draw_y = int(self.y - offset[1])
            size = int(self.size * self.life)
            if size > 0:
                pygame.draw.circle(screen, self.color[:3], (draw_x, draw_y), size)

class ParticleSystem:
    def __init__(self):
        self.particles = []
        
    def add_explosion(self, x, y, color, count=15):
        """Добавляет взрыв частиц"""
        for _ in range(count):
            self.particles.append(Particle(x, y, color))
    
    def add_trail(self, x, y, color):
        """Добавляет след частиц"""
        if random.random() < 0.3:
            self.particles.append(Particle(x, y, color))
    
    def update(self):
        """Обновление всех частиц"""
        for particle in self.particles[:]:
            particle.update()
            if particle.life <= 0:
                self.particles.remove(particle)
    
    def draw(self, screen, offset):
        """Отрисовка всех частиц"""
        for particle in self.particles:
            particle.draw(screen, offset)
    
    def clear(self):
        """Очистка всех частиц"""
        self.particles.clear()
