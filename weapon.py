import pygame

class Weapon(pygame.sprite.Sprite):
    def __init__(self,player,groups):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/weapons/GUN_test.png').convert_alpha()
        self.rect = self.image.get_rect(center=player.rect.center)  # <-- Add this line
        self.player = player
        
    def update_weapon(self):
        direction = self.player.status.split('_')[0]
        if direction == 'up':
            self.rect =  self.image.get_rect(midbottom=self.player.rect.midtop + pygame.math.Vector2(-10, 40))
        elif direction == 'down':
            self.rect =  self.image.get_rect(midtop=self.player.rect.midbottom + pygame.math.Vector2(-10,-40))
        elif direction == 'left':
            self.rect =  self.image.get_rect(midright=self.player.rect.midleft + pygame.math.Vector2(25, 12))
        elif direction == 'right':
            self.rect =  self.image.get_rect(midleft=self.player.rect.midright + pygame.math.Vector2(-25, 12))
        