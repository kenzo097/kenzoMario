import pygame

class Player:
    def __init__(self, x, y):
        self.width = 40
        self.height = 50
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
        self.velocity_x = 0
        self.velocity_y = 0
        self.speed = 6
        self.acceleration = 0.5
        self.friction = 0.85
        self.max_speed = 7
        
        self.jump_power = -16
        self.jump_hold_time = 0
        self.max_jump_hold = 10
        self.jump_hold_power = -0.5
        self.gravity = 0.75
        self.on_ground = False
        self.coyote_time = 0
        self.max_coyote_time = 8
        
        self.facing_right = True
        self.animation_frame = 0
        self.animation_speed = 0.25
        self.animation_counter = 0
        
        self.color = (255, 0, 0)
        self.hat_color = (255, 200, 0)
        
    def update(self, keys, level):
        """Обновление игрока"""
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity_x -= self.acceleration
            self.facing_right = False
            self.animation_counter += self.animation_speed
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity_x += self.acceleration
            self.facing_right = True
            self.animation_counter += self.animation_speed
        else:
            self.velocity_x *= self.friction
            self.animation_counter = 0
        
        if self.velocity_x > self.max_speed:
            self.velocity_x = self.max_speed
        elif self.velocity_x < -self.max_speed:
            self.velocity_x = -self.max_speed
        
        if abs(self.velocity_x) < 0.1:
            self.velocity_x = 0
        
        if self.on_ground:
            self.coyote_time = self.max_coyote_time
        else:
            if self.coyote_time > 0:
                self.coyote_time -= 1
        
        jump_pressed = keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]
        can_jump = self.on_ground or self.coyote_time > 0
        
        if jump_pressed and can_jump and self.velocity_y >= 0:
            if self.jump_hold_time == 0:
                self.velocity_y = self.jump_power
                self.on_ground = False
                self.coyote_time = 0
            
            if self.jump_hold_time < self.max_jump_hold:
                self.velocity_y += self.jump_hold_power
                self.jump_hold_time += 1
        else:
            self.jump_hold_time = 0
        
        if not self.on_ground:
            self.velocity_y += self.gravity
        
        if self.velocity_y > 18:
            self.velocity_y = 18
        
        self.rect.x += int(self.velocity_x)
        self.rect.y += int(self.velocity_y)
        
        if self.velocity_y != 0:
            self.on_ground = False
        
        if abs(self.velocity_x) > 0.5:
            self.animation_frame = int(self.animation_counter) % 4
        else:
            self.animation_frame = 0
        
        if self.rect.x < 0:
            self.rect.x = 0
            self.velocity_x = 0
        if self.rect.y < 0:
            self.rect.y = 0
            self.velocity_y = 0
    
    def draw(self, screen, offset):
        """Отрисовка игрока"""
        draw_x = self.rect.x - offset[0]
        draw_y = self.rect.y - offset[1]
        
        pygame.draw.rect(screen, self.color, 
                        (draw_x + 5, draw_y + 20, self.width - 10, self.height - 20))
        pygame.draw.ellipse(screen, self.hat_color,
                           (draw_x + 2, draw_y + 5, self.width - 4, 20))
        
        eye_x = draw_x + 10 if self.facing_right else draw_x + self.width - 15
        pygame.draw.circle(screen, WHITE, (eye_x, draw_y + 25), 4)
        pygame.draw.circle(screen, BLACK, (eye_x, draw_y + 25), 2)
        
        if abs(self.velocity_x) > 0:
            arm_offset = int(5 * abs(self.animation_frame - 1))
        else:
            arm_offset = 0
        
        pygame.draw.rect(screen, (255, 150, 150),
                        (draw_x - 3, draw_y + 25 + arm_offset, 8, 15))
        pygame.draw.rect(screen, (255, 150, 150),
                        (draw_x + self.width - 5, draw_y + 25 - arm_offset, 8, 15))
        
        if abs(self.velocity_x) > 0:
            leg_offset = int(3 * abs(self.animation_frame - 1))
        else:
            leg_offset = 0
        
        pygame.draw.rect(screen, (0, 0, 200),
                        (draw_x + 8, draw_y + self.height - 10 + leg_offset, 8, 10))
        pygame.draw.rect(screen, (0, 0, 200),
                        (draw_x + self.width - 16, draw_y + self.height - 10 - leg_offset, 8, 10))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
