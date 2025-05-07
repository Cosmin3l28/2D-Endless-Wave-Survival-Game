import pygame
from support import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups,obstacle_sprites):
        super().__init__(groups)#we initiate the tile class as a sprite
        self.image = pygame.image.load('graphics/player/left_idle/sprite_invers_0.png').convert_alpha()#we load the image of the tile
        self.image = pygame.transform.scale(self.image, (96, 96)) # we want to scale the image to the size of the tile
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-60, -24) # we want to make the hitbox smaller than the tile so that we can see the tile and not the hitbox
        
        self.import_player_assets()
        self.status = 'down' # we want to set the status of the player to idle down
        self.frame_index = 0
        self.animation_speed = 0.1
        self.melee = False # we want to set the attacking status to false
        self.melee_time = None
        self.melee_cooldown = 3000
        self.melee_speed = 0.1
        self.animation_melee = False
        self.frame_melee_index = 0

        self.direction = pygame.math.Vector2() # x and y for movement
        self.speed = 4
        self.stamina = 100
        
        self.obstacle_sprites = obstacle_sprites # we need this to check for collisions with the obstacles
 
    def import_player_assets(self):
        character_path = 'graphics/player/'
        self.animations = {
            'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
            'right': [], 'left': [], 'up': [], 'down': [],
            'down_attack': [], 'right_attack': [], 'up_attack': [], 'left_attack': []
        }            
        for animation in self.animations.keys():
            fullpath = character_path + animation
            self.animations[animation] = import_folder(fullpath) # we get the list of images from the folder

    def input(self):
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        if keys[pygame.K_w]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pygame.K_s]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0
        
        if keys[pygame.K_a]:
            self.direction.x = -1
            self.status = 'left'
        elif keys[pygame.K_d]:
            self.direction.x = 1
            self.status = 'right'
        else:
            self.direction.x = 0
        
        if keys[pygame.K_LSHIFT]: #sprint
            if self.stamina > 0:
                self.speed = 7
                self.stamina -= 0.5 # we want to decrease the stamina when we sprint
            else:
                self.speed = 3
        else:
            self.speed = 3
            if 'idle' in self.status:
                self.stamina += 0.8
            else:
                self.stamina += 0.4
                
        # if keys[pygame.K_SPACE] and self.cooldown == 0: #dash
        #     self.dash = 100
        #     self.cooldown = 2000 # we want to set a cooldown for the dash
        # else:
        #     self.dash = 0
            
        self.stamina = max(0, min(self.stamina, 100))

        #attack
        if mouse[0] and self.melee == False:
            print('attack')
            self.melee = True
            self.melee_time = pygame.time.get_ticks() # we get the current time in milliseconds
            self.animation_melee = True
            self.animation_speed = self.melee_speed
            self.frame_melee_index = 0
            self.frame_index = 0 # we want to reset the frame index so that we can see the attack animation
    
    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize() # normalizes the vector to have a length of 1
            #this way we can move in diagonal without increasing the speed
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center # we want to move the rect with the hitbox so that we can see the player moving
        
    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if self.hitbox.colliderect(sprite.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left # right collision
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right # left collision
        
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if self.hitbox.colliderect(sprite.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top  # down collision
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom  # up collision

    def draw_stamina_bar(self, surface):
        # Calculăm lungimea barei în funcție de stamina curentă
        current_width = (self.stamina / 100) * 300

        # Culori
        background_color = 'black'
        stamina_color = 'white'

        # Desenăm fundalul barei
        pygame.draw.rect(surface, background_color, (10, 20, 300, 35), border_radius = 20)

        # Desenăm bara de stamina
        pygame.draw.rect(surface, stamina_color, (10, 20, current_width, 35), border_radius = 20)
        #### 2. Actualizează stamina în funcție de acțiunile jucătorului

    def update(self):
        self.input()
        self.cooldown()
        self.get_status()
        self.animate()
        self.move(self.speed)
        
    def run(self):
        self.visible_sprites.draw(self.display_surface)
        self.visible_sprites.update()

    def get_status(self):

        #idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status:
                if 'attack' in self.status:
                    self.status = self.status.replace('_attack', '_idle')
                else:
                    self.status = self.status + '_idle'

        if self.animation_melee == True:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                     self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + '_attack'

    def cooldown(self):
        current_time = pygame.time.get_ticks()
        if self.melee == True:
            self.frame_melee_index += self.animation_speed
            if self.frame_melee_index >= 4:
                self.animation_melee = False
                self.animation_speed = 0.1
            if current_time - self.melee_time >= self.melee_cooldown:
                self.melee = False

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        self.image = animation[int(self.frame_index)] # we get the image from the list of images
        self.image = pygame.transform.scale(self.image, (96, 96))
        self.rect = self.image.get_rect(center=self.hitbox.center) # we want to move the rect with the hitbox so that we can see the player moving
