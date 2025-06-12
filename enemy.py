import pygame
from support import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, monster_name, pos, groups, obstacle_sprites=None, player=None, bullet_group=None):
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

        self.health = data.get('health', 100)
        self.speed = data.get('speed', 2)
        self.loot = data.get('loot', 1)
        self.damage = data.get('damage', 10)
        self.bullet_group = bullet_group    
        self.float_x = float(self.hitbox.x)
        self.float_y = float(self.hitbox.y)
        self.shoot_interval = data.get('shoot_interval')
        self.last_shot = pygame.time.get_ticks()
        self.shoot_pause = 400
        self.shooting = False
        self.pause_start = 0

    def get_status(self):
        if not self.alive:
            return  # nu schimbăm statusul dacă e mort

        dx = self.player.rect.centerx - self.rect.centerx
        dy = self.player.rect.centery - self.rect.centery

        if abs(dx) > abs(dy):
            self.facing = 'right' if dx > 0 else 'left'
        else:
            self.facing = 'down' if dy > 0 else 'up'

        attack_zone = pygame.Rect(0, 0, 192, 192)
        attack_zone.center = self.rect.center

        if self.attacking:
            self.status = 'attack'
        elif attack_zone.colliderect(self.player.rect):
            self.attacking = True
            self.frame_index = 0
            self.has_damaged_player = False
            self.status = 'attack'
        else:
            self.status = 'walk'

    def animate(self):
        direction = 'down' if self.status == 'death' else self.facing
        animation_list = self.animations.get(self.status, {}).get(direction, [])

        if not animation_list:
            print(f"[WARN] Missing animation: {self.status}/{direction}")
            return

        self.frame_index += self.animation_speed

        if self.frame_index >= len(animation_list):
            if self.status == 'death':
                self.dead_animation_finished = True
                self.frame_index = len(animation_list) - 1
            elif self.status == 'attack':
                self.attacking = False
                self.frame_index = 0
            else:
                self.frame_index = 0

        frame = animation_list[int(self.frame_index)]
        self.image = pygame.transform.scale(frame, (192, 192))

    def update(self):
            dx = self.player.rect.centerx - self.rect.centerx
            dy = self.player.rect.centery - self.rect.centery
            dist = max(1, (dx**2 + dy**2) ** 0.5)
            #print(dist)
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
        for sprite in self.obstacle_sprites:
            if sprite == self:
                continue
            if self.hitbox.colliderect(sprite.hitbox):
                if direction == 'horizontal':
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                        self.float_x = self.hitbox.x
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
                        self.float_x = self.hitbox.x
                if direction == 'vertical':
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                        self.float_y = self.hitbox.y
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
                        self.float_y = self.hitbox.y