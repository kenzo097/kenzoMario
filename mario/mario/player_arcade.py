import arcade

class Player:
    def __init__(self, x, y):
        self.sprite = arcade.SpriteSolidColor(40, 50, arcade.color.RED)
        self.sprite.center_x = x
        self.sprite.center_y = y
        
        self.left_pressed = False
        self.right_pressed = False
        
        self.speed = 6
    
    def update(self):
        if self.left_pressed:
            self.sprite.change_x = -self.speed
        elif self.right_pressed:
            self.sprite.change_x = self.speed
        else:
            self.sprite.change_x = 0
