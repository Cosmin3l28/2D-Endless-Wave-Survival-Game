import pygame
from tile import Tile
from player import Player
from debug import debug
from support import TILESIZE, WIDTH, HEIGHT
from support import import_csv_layout, import_folder
from weapon import Weapon
from bullet import Bullet
from enemy import Enemy
import random
class Level:
    def __init__(self):
        # get the display surface
        self.display_surface = pygame.display.get_surface()
        
        # create the sprite groups
        self.visible_sprites = YsortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.last_spawn_time = pygame.time.get_ticks()
        self.spawn_interval = 2000 # spawn an enemy every 2 seconds
        
        # create the map
        self.create_map()
    
    def create_map(self):
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
                        # if style == 'walls':
                        #     pass
                        if style == 'object':
                            surf = graphics['objects'][int(col)] # we get the surface of the object from the graphics dictionary
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'object', surf) # we create the tile with the surface of the object
                        
                        
        self.player = Player((1000, 1000), [self.visible_sprites], self.obstacle_sprites) # we create the player and add it to the visible sprites and the obstacle sprites
        self.player.level = self # we set the level of the player to the current level so that we can access the level from the player
        
    def spawn_random_enemy(self):
        x = random.randint(0, 2400)
        y = random.randint(0, 2400)
        enemy = Enemy('enemy', (x,y), [self.visible_sprites, self.enemies], self.obstacle_sprites, self.player)
        self.enemies.add(enemy)

    def run(self): # here we display what happens on screen using our coustom camera that follows the player

        # spawn enemies at random intervals
        now = pygame.time.get_ticks()
        if now - self.last_spawn_time > self.spawn_interval:
            self.spawn_random_enemy()
            self.last_spawn_time = now
        self.enemies.update()
        self.bullets.update()

        for enemy in self.enemies:
            if self.player.rect.colliderect(enemy.rect):
                self.player.take_damage(0.2) # if the player collides with an enemy, take damage

        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.player.draw_stamina_bar(self.display_surface)
        self.player.draw_health_bar(self.display_surface)
        # debug(self.player.direction)
        debug(self.player.speed)
        
        
class YsortCameraGroup(pygame.sprite.Group): # to create a custom camera that follows the player
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2() # offset for the camera

        #creating the floor
        self.floor_surface = pygame.image.load('graphics/Floor.png').convert_alpha()
        #self.floor_surface = pygame.transform.scale(self.floor_surface, (4 * 640 , 4 * 640))
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))



    def custom_draw(self, player):
        # Smooth camera lag effect
        self.offset.x += (player.rect.centerx - self.half_width - self.offset.x) / 20 
        self.offset.y += (player.rect.centery - self.half_height - self.offset.y) / 20 

        self.offset.x = max(0, min(self.offset.x, self.floor_rect.width - self.display_surface.get_width())) # we want to limit the offset to the width of the floor
        self.offset.y = max(0, min(self.offset.y, self.floor_rect.height - self.display_surface.get_height())) # we want to limit the offset to the height of the floor

        offset_pos = self.floor_rect.topleft - self.offset
        # draw the floor
        self.display_surface.blit(self.floor_surface, offset_pos)
        
        # draw the sprites on the screen with the offset
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery): # sort the sprites by their y position to know w hat do display over what
            offset_pos = sprite.rect.topleft - self.offset # get the position of the sprite and subtract the offset
            self.display_surface.blit(sprite.image, offset_pos) 