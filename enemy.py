import pygame
from support import moster_data
from bullet import EnemyBullet

class Enemy(pygame.sprite.Sprite):
    def __init__(self, monster_name, pos, groups, obstacle_sprites=None, player=None, bullet_group=None):
        super().__init__(groups)
        
        data = moster_data[monster_name]
        self.type = monster_name

        self.image = pygame.Surface((64, 64))
        self.image.fill('black')  # <-- dreptunghi negru
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-10, -10)
        self.obstacle_sprites = obstacle_sprites
        self.player = player

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

    def update(self):
        if self.shooting:
            if pygame.time.get_ticks() - self.pause_start >= self.shoot_pause:
                self.shooting = False
        else:
            self.move_towards_player()
        if self.shoot_interval:
            self.shoot()

    def move_towards_player(self):
        dx = self.player.rect.centerx - self.rect.centerx
        dy = self.player.rect.centery - self.rect.centery
        dist = max(1, (dx**2 + dy**2) ** 0.5)
        self.direction = pygame.math.Vector2(dx / dist, dy / dist)
        self.move(self.speed)

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
    
    def shoot(self):
        current_time = pygame.time.get_ticks()
        if self.shooting:
            return
        if current_time - self.last_shot >= self.shoot_interval:
            direction = pygame.math.Vector2(self.player.rect.center) - pygame.math.Vector2(self.rect.center)
            bullet = EnemyBullet(
                self.rect.center,
                direction,
                [self.player.level.visible_sprites, self.bullet_group],
                self.obstacle_sprites,
                self.player,
                self.damage,
            )
            self.bullet_group.add(bullet)
            self.last_shot = current_time
            self.shooting = True
            self.pause_start = current_time