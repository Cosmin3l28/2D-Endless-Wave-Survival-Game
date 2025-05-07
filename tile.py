import pygame
from settings import *
#we want to implement hitbox for tiles so that we can add 3d depth effect
#the player can stand behind or cover objects depending of weather he is in front or behind the hitbox of the object
class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type='tile', surface = pygame.Surface((TILESIZE, TILESIZE))):
        super().__init__(groups)#we initiate the tile class as a sprite
        self.sprite_type = sprite_type
        self.image = surface
        #self.image = pygame.transform.scale(self.image, (64, 64))
        #self.image = pygame.image.load('graphics/tiles/tile.png').convert_alpha()#we load the image of the tile
        if self.sprite_type == 'object':
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(-50, -50)
            self.hitbox.y = self.hitbox.y + 50
            self.hitbox.height = self.hitbox.height - 50
            self.hitbox.x = self.hitbox.x + 10
            self.hitbox.width = self.hitbox.width - 20
        else:
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(0, -20) # we want to make the hitbox smaller than the tile so that we can see the tile and not the hitbox