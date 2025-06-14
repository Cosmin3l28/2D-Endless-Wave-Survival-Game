"""Weapon sprite used by the player."""
import pygame

class Weapon(pygame.sprite.Sprite):
    """Weapon sprite used by the player."""
    def __init__(self, 
                 player: pygame.sprite.Sprite, 
                 groups: list[pygame.sprite.Group],
                 ):
        """Create a weapon sprite bound to a player."""
        super().__init__(groups)
        self.original_image = pygame.image.load(
            'graphics/weapons/GUN_test.png').convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect(
            center=player.rect.center)
        self.player = player
        self.direction = pygame.math.Vector2(1, 0)
        self.handle_offset = pygame.math.Vector2(4, 2)
        
    def update_weapon(self) -> None:

        """Update the weapon's position and rotation based on the player's direction."""
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) + self.player.level.visible_sprites.offset
        player_center = pygame.Vector2(self.player.rect.center)
        direction = mouse_pos - player_center
        # Normalize the direction vector to avoid division by zero
        if direction.length() == 0:
            direction = pygame.Vector2(1, 0)
        self.direction = direction.normalize()
        angle = -self.direction.angle_to(pygame.Vector2(1, 0))
        print(angle)
        # Rotate the weapon image based on the angle
        if (angle) < -90 or (angle) > 90:
            flipped_image = pygame.transform.flip(self.original_image, True, False)
            if angle > -180 and angle < -90:
                self.image = pygame.transform.rotate(flipped_image,  -(180 + angle))
            elif angle < 180:
                self.image = pygame.transform.rotate(flipped_image,  (180 - angle))
                print("flipped")
        else:
            self.image = pygame.transform.rotate(self.original_image, - angle)
        offset = self.direction * 40
        handle = self.handle_offset.rotate(angle)
        self.rect = self.image.get_rect(center=player_center + offset - handle)