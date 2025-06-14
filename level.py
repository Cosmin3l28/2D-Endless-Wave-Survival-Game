"""Game level containing player, enemies and map logic."""
import pygame
from tile import Tile
from player import Player
from debug import debug
from support import TILESIZE, WIDTH, HEIGHT
from support import import_csv_layout, import_folder
from weapon import Weapon
from bullet import Bullet
from enemy_factory import create_enemy
import random
class Level:
    def __init__(self):
        """Initialize the game level, setting up the display, sprite groups, and map."""
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = YsortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.last_spawn_time = pygame.time.get_ticks()
        self.spawn_interval = 2000
        self.enemy_bullets = pygame.sprite.Group()  # group for enemy bullets
        self.wave = 1
        self.wave_finished = False
        self.create_map()  # create the map

    def start_wave(self, wave: int) -> None:
        """Start a new enemy wave.

        Args:
            wave (int): The wave number to start.
        """
        self.wave = wave
        self.wave_finished = False
        enemy_count = 5 + (wave - 1) * 2
        for i in range(enemy_count):
            if wave > 2 and random.random() < 0.3:
                self.spawn_random_enemy('shooter')
            else:
                self.spawn_random_enemy('enemy')
    
    def create_map(self) -> None:
        """Create the game map by loading tile layouts and graphics."""
        layout = {
            'boundary': import_csv_layout('graphics/map_restrictions.csv'), 
            'object': import_csv_layout('graphics/map_objects.csv'),
        }

        graphics = {
            'objects': import_folder('graphics/Objects'),
        }

        for style, layout in layout.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x,y), [self.obstacle_sprites], 'invisibile')
                        if style == 'object':
                            surf = graphics['objects'][int(col)] # we get the surface of the object from the graphics dictionary
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'object', surf) # we create the tile with the surface of the object
                        
                        
        self.player = Player((1000, 1000), [self.visible_sprites], self.obstacle_sprites) # we create the player and add it to the visible sprites and the obstacle sprites
        self.player.level = self  # we set the level of the player to the current level so that we can access the level from the player

    def spawn_random_enemy(self, enemy_type='enemy') -> None:
        """Spawn a random enemy at a random position.

        Args:
            enemy_type (str, optional): The type of enemy to spawn. Defaults to 'enemy'.
        """
        x = random.randint(300, 2100)
        y = random.randint(300, 2100)
        enemy = create_enemy(
            enemy_type,
            (x, y),
            groups=[self.visible_sprites, self.enemies],
            obstacle_sprites=self.obstacle_sprites,
            player=self.player,
            bullet_group=self.enemy_bullets,
        )
        enemy.speed += (self.wave - 1) * 0.2  # Scale enemy speed based on current wave

    def run(self) -> bool:
        """Run the level logic and update all entities.

        Returns:
            bool: True if the wave is finished, False otherwise.
        """
        if len(self.enemies) == 0 and not self.wave_finished:
            self.wave_finished = True

        self.enemies.update()
        self.enemy_bullets.update()
        self.bullets.update()

        for enemy in self.enemies:
            if self.player.rect.colliderect(enemy.rect):
                self.player.take_damage(0.2) # if the player collides with an enemy, take damage

        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.player.draw_stamina_bar(self.display_surface)
        self.player.draw_health_bar(self.display_surface)
        self.player.draw_gold(self.display_surface)
        debug(self.player.speed)
        return self.wave_finished
        
"""A camera group that sorts sprites by their y-coordinate for rendering."""       
class YsortCameraGroup(pygame.sprite.Group):
    
    def __init__(self):
        super().__init__()
        """Initialize the camera group, setting up the display surface and offset."""
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()  # offset for the camera
        self.floor_surface = pygame.image.load('graphics/Floor.png').convert_alpha()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))

    def custom_draw(self, player: pygame.sprite.Sprite) -> None:
        """Draw the camera group, applying the camera offset.

        Args:
            player (pygame.sprite.Sprite): The player sprite to center the camera on.
        """   
        self.offset.x += (player.rect.centerx - self.half_width - self.offset.x) / 20  # Smooth camera lag effect
        self.offset.y += (player.rect.centery - self.half_height - self.offset.y) / 20 
        self.offset.x = max(0, min(self.offset.x, self.floor_rect.width - self.display_surface.get_width()))  # We want to limit the offset to the width of the floor
        self.offset.y = max(0, min(self.offset.y, self.floor_rect.height - self.display_surface.get_height()))  # We want to limit the offset to the height of the floor

        offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, offset_pos)  # Draw the floor
        
        """Draw all sprites in the group, applying the camera offset."""
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):  # Sort the sprites by their y position to know what to display over what
            offset_pos = sprite.rect.topleft - self.offset  # Get the position of the sprite and subtract the offset
            self.display_surface.blit(sprite.image, offset_pos)