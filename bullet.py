"""Projectile classes for both player and enemy bullets."""
import pygame

class Bullet(pygame.sprite.Sprite):
    """Projectile fired by the player."""
    def __init__(self, 
                 pos: tuple, direction: tuple, 
                 groups: list, obstacle_sprites: list, 
                 enemies: list, player: pygame.sprite.Sprite, 
                 damage: int = 50
    ):
        """Initialize a new bullet instance."""
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

    def update(self) -> None:
        """Move the bullet and handle collisions."""

        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

        for sprite in self.obstacle_sprites:
            if self.rect.colliderect(sprite.rect):
                self.kill()
                return
        for enemy in list(self.enemies):
            if self.rect.colliderect(enemy.rect):
                # apelăm corect funcția care pornește animatia
                enemy.take_damage(self.damage)
                if enemy.health <= 0:
                    enemy.kill()
                    self.player.gold += enemy.loot
                self.kill()
                return

class EnemyBullet(pygame.sprite.Sprite):
    """Bullet fired by enemies."""

    def __init__(
        self,
        pos: tuple,
        direction: tuple,
        groups: list,
        obstacle_sprites: list,
        player: pygame.sprite.Sprite,
        damage: int = 10,
    ):
        """Initialize the enemy bullet."""
        super().__init__(groups)
        
        self.image = pygame.Surface((12, 6))
        self.image.fill('red')
        self.rect = self.image.get_rect(center=pos)
        self.direction = pygame.math.Vector2(direction)
        if self.direction.length() == 0:
            self.direction = pygame.math.Vector2(1, 0)
        self.direction = self.direction.normalize()
        self.speed = 5
        self.obstacle_sprites = obstacle_sprites
        self.player = player
        self.damage = damage

    def update(self) -> None:
        """Move the bullet and check collisions with the player."""

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
