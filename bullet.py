import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction, groups, obstacle_sprites, enemies):
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

    def update(self):
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

        for sprite in self.obstacle_sprites:
            if self.rect.colliderect(sprite.rect):
                self.kill()
                return
        for enemy in list(self.enemies):
            if self.rect.colliderect(enemy.rect):
                enemy.health -= 50
                if enemy.health <= 0:
                    enemy.kill()
                self.kill()
                return