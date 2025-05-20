import pygame
from support import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, monster_name, pos, groups, obstacle_sprites=None, player=None):
        super().__init__(groups)
        self.sprite_type = 'enemy'
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.math.Vector2()
        self.image = pygame.Surface((64, 64))
        self.image.fill('black')  # <-- dreptunghi negru
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-10, -10)
        self.obstacle_sprites = obstacle_sprites
        self.player = player
        self.health = 100

        self.float_x = float(self.hitbox.x)
        self.float_y = float(self.hitbox.y)

    def update(self):
            dx = self.player.rect.centerx - self.rect.centerx
            dy = self.player.rect.centery - self.rect.centery
            dist = max(1, (dx**2 + dy**2) ** 0.5)
            print(dist)
            self.direction.x = dx / dist
            self.direction.y = dy / dist
            self.move(0.7)

    def move(self, speed):
        self.float_x += self.direction.x * speed
        self.hitbox.x = int(self.float_x)
        self.collision('horizontal')
        self.float_y += self.direction.y * speed
        self.hitbox.y = int(self.float_y)
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if not self.obstacle_sprites:
            return
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite == self:
                    continue
                if self.hitbox.colliderect(sprite.hitbox):
                    if self.direction.x > 0:  # moving right
                        self.hitbox.right = sprite.hitbox.left
                        self.float_x = self.hitbox.x
                    if self.direction.x < 0:  # moving left
                        self.hitbox.left = sprite.hitbox.right
                        self.float_x = self.hitbox.x
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite == self:
                    continue
                if self.hitbox.colliderect(sprite.hitbox):
                    if self.direction.y > 0:  # moving down
                        self.hitbox.bottom = sprite.hitbox.top
                        self.float_y = self.hitbox.y
                    if self.direction.y < 0:  # moving up
                        self.hitbox.top = sprite.hitbox.bottom
                        self.float_y = self.hitbox.y