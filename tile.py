"""Tile class for managing tile properties in a game."""
import pygame
from support import TILESIZE

class Tile(pygame.sprite.Sprite):
    def __init__(self, 
                 pos : tuple[int, int], 
                 groups : list[pygame.sprite.Group], 
                 sprite_type : str = 'tile', 
                 surface : pygame.Surface = pygame.Surface((TILESIZE, TILESIZE))):
        """Initialize a tile with position, groups, type, and surface."""
        super().__init__(groups)#we initiate the tile class as a sprite
        self.sprite_type = sprite_type
        self.image = surface
        if self.sprite_type == 'object':
            surface_size = self.image.get_size()
            #tower
            if surface_size == (116, 184):
                self.rect = self.image.get_rect(topleft= (pos[0] + 52, pos[1] - 120))
                self.hitbox = self.rect.inflate(-10, -100)
            #trees
            elif surface_size == (110,180):
                self.rect = self.image.get_rect(topleft= (pos[0] + 46, pos[1] - 116))
                self.hitbox = self.rect.inflate(-40, -80)
                self.hitbox.y = self.hitbox.y + 45
                self.hitbox.height = self.hitbox.height - 45
            #house1
            elif surface_size == (96, 85):
                self.rect = self.image.get_rect(topleft= (pos[0] + 20, pos[1] - 43))
                self.hitbox = self.rect.inflate(-30, -80)
            #house 2
            elif surface_size == (100, 104):
                self.rect = self.image.get_rect(topleft= (pos[0] + 36, pos[1] - 40))
                self.hitbox = self.rect.inflate(-30, -80)
                
            #mine
            elif surface_size == (164, 95):
                self.rect = self.image.get_rect(topleft= (pos[0] + 100, pos[1] - 31))
                self.hitbox = self.rect.inflate(-40, -60)

        else:
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(0, -20) # we want to make the hitbox smaller than the tile so that we can see the tile and not the hitbox