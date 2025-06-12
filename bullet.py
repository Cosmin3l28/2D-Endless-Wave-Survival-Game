import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction, groups, obstacle_sprites, enemies, player, damage=50):
        super().__init__(groups)
        self.image = pygame.Surface((10, 4))
        self.image.fill('yellow')
        self.rect = self.image.get_rect(center=pos)
        self.direction = pygame.math.Vector2(direction)
        if self.direction.length() == 0:
            self.direction = pygame.math.Vector2(1, 0)
        self.direction = self.direction.normalize()
        self.speed = 10
        self.obstacle_sprites = obstacle_sprites
        self.enemies = enemies
        self.player = player
        self.damage = damage

    def update(self):
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

        for sprite in self.obstacle_sprites:
            if self.rect.colliderect(sprite.rect):
                self.kill()
                return
        for enemy in list(self.enemies):
            if self.rect.colliderect(enemy.rect):
                enemy.health -= self.damage
                if enemy.health <= 0:
                    enemy.kill()
                    self.player.gold += enemy.loot
                self.kill()
                return
            
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction, groups, obstacle_sprites, player, damage=10):
        super().__init__(groups)
        self.image = pygame.Surface((8, 3))
        self.image.fill('red')
        self.rect = self.image.get_rect(center=pos)
        self.direction = pygame.math.Vector2(direction)
        if self.direction.length() == 0:
            self.direction = pygame.math.Vector2(1, 0)
        self.direction = self.direction.normalize()
        self.speed = 8
        self.obstacle_sprites = obstacle_sprites
        self.player = player
        self.damage = damage

    def update(self):
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed
        for sprite in self.obstacle_sprites:
            if self.rect.colliderect(sprite.rect):
                self.kill()
                return
        if self.rect.colliderect(self.player.rect):
            self.player.take_damage(self.damage)
            self.kill()
            return