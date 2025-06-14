"""Enemy classes and behavior logic."""
import pygame
from support import import_folder
import os
from support import moster_data
from bullet import EnemyBullet

class Enemy(pygame.sprite.Sprite):
    """Generic enemy character that can move and attack the player."""

    def __init__(
            self,
            monster_name,
            pos,
            groups,
            obstacle_sprites=None,
            player=None,
            bullet_group=None):
        """Initialize the enemy and load its animations."""

        super().__init__(groups)
        self.sprite_type = 'enemy'
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.math.Vector2()

        data = moster_data[monster_name]
        self.type = monster_name
        self.obstacle_sprites = obstacle_sprites
        self.player = player

        self.loot = data.get('loot', 1)

        self.alive = True
        self.dead_animation_finished = False

        self.attacking = False
        self.has_damaged_player = False

        self.animations = {
            'walk': {}, 'idle': {}, 'attack': {}, 'death': {}
        }

        base_path = os.path.join('graphics', 'enemy_1')
        """Load animations for the enemy from the specified folder structure."""
        for anim_type in self.animations.keys():
            for direction in ['down', 'up', 'left', 'right']:
                path = os.path.join(base_path, anim_type, direction)
                original_frames = import_folder(path)

                if anim_type == 'idle':
                    extended_frames = []
                    for frame in original_frames[:4]:
                        extended_frames.extend([frame] * 3)
                    self.animations[anim_type][direction] = extended_frames
                else:
                    self.animations[anim_type][direction] = original_frames

        self.status = 'idle'
        self.facing = 'down'
        self.image = self.animations[self.status][self.facing][0]
        self.image = pygame.transform.scale(self.image, (192, 192))
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-10, -10)

        self.health = data.get('health', 100)
        self.speed = data.get('speed', 2)
        self.damage = data.get('damage', 10)
        self.bullet_group = bullet_group 
        self.float_x = float(self.hitbox.x)
        self.float_y = float(self.hitbox.y)
        self.shoot_interval = data.get('shoot_interval')
        self.last_shot = pygame.time.get_ticks()
        self.shoot_pause = 400
        self.shooting = False
        self.pause_start = 0

    def get_status(self) -> None:
        """Determine the current animation state of the enemy."""
        if not self.alive:
            return  # Do not update status if dead

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

    def animate(self) -> None:
        """Advance animation frames based on the current status."""
        direction = 'down' if self.status == 'death' else self.facing
        animation_list = self.animations.get(
            self.status, {}).get(
                direction, [])

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

    def update(self) -> None:
        """Update enemy behavior and animations."""
        if self.health <= 0:
            if self.alive:
                self.alive = False
                self.status = 'death'
                self.frame_index = 0
                self.dead_animation_finished = False
                self.facing = 'down'
            else:
                self.status = 'death'
                self.animate()
                if self.dead_animation_finished:
                    self.kill()
            return
        
        """Handle enemy behavior based on current status."""
        if self.shooting:
            if pygame.time.get_ticks() - self.pause_start >= self.shoot_pause:
                self.shooting = False
        else:
            if self.status == 'walk':
                self.move_towards_player()
            elif self.status == 'attack':
                self.apply_attack_damage()

        if self.shoot_interval:
            self.shoot()

        self.get_status()
        self.animate()

    def move_towards_player(self) -> None:
        """Move the enemy towards the player's current position."""
        dx = self.player.rect.centerx - self.rect.centerx
        dy = self.player.rect.centery - self.rect.centery
        dist = max(1, (dx**2 + dy**2) ** 0.5)
        self.direction = pygame.math.Vector2(dx / dist, dy / dist)
        self.move(self.speed)

    def apply_attack_damage(self) -> None:
        """Inflict damage to the player when attacking."""
        attack_zone = pygame.Rect(0, 0, 96, 96)
        attack_zone.center = self.rect.center

        if not self.has_damaged_player and int(self.frame_index) == 1:
            if attack_zone.colliderect(self.player.rect):
                self.player.take_damage(10)
                self.has_damaged_player = True

    def move(self, speed: float) -> None:
        """Move the enemy in the current direction while checking for collisions.

        Args:
            speed (float): The speed at which to move the enemy.
        """
        self.float_x += self.direction.x * speed
        self.hitbox.x = int(self.float_x)
        self.collision('horizontal')
        self.float_y += self.direction.y * speed
        self.hitbox.y = int(self.float_y)
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self, direction: str) -> None:
        """Handle collisions with map obstacles.

        Args:
            direction (str): The direction of the collision.
        """
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

    def take_damage(self, amount : int) -> None:
        """Reduce health by the provided amount.

        Args:
            amount (int): The amount of damage to inflict.
        """
        if not self.alive:
            return
        self.health -= amount

    def shoot(self) -> None:
        """Fire a bullet towards the player."""
        current_time = pygame.time.get_ticks()
        if self.shooting:
            return
        if current_time - self.last_shot >= self.shoot_interval:
            direction = (
                pygame.math.Vector2(self.player.rect.center)
                - pygame.math.Vector2(self.rect.center)
            )
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
