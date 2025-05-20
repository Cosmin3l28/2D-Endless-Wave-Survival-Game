import pygame
from support import *
 
class Enemy(pygame.sprite.Sprite):
    def __init__(self, monster_name, pos,  groups):
        super().__init__(groups)
        self.sprite_type = 'enemy'
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.math.Vector2()
        
        self.image = pygame.surface((64, 64))
        self.image.fill('red')
        
    def move(self, speed):
        if self.direction.x != 0 and self.direction.y != 0:
            speed = 2
            if self.speed == 4:
                speed = 3
            if self.speed == 16:
                speed = 11
        
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center
    
    def collision(self, direction): 
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if self.hitbox.colliderect(sprite.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left # right collision
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right # left collision
        
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if self.hitbox.colliderect(sprite.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top  # down collision
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom  # up collision
    