import pygame
from support import *
from weapon import Weapon
from bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups,obstacle_sprites):
        super().__init__(groups)#we initiate the tile class as a sprite
        self.image = pygame.image.load('graphics/player/left_idle/sprite_invers_0.png').convert_alpha()#we load the image of the tile
        self.image = pygame.transform.scale(self.image, (96, 96)) # we want to scale the image to the size of the tile
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-60, -24) # we want to make the hitbox smaller than the tile so that we can see the tile and not the hitbox

        self.import_player_assets()
        self.status = 'down' # we want to set the status of the player to idle down
        self.walk_status = 'down'
        self.frame_index = 0
        self.animation_speed = 0.1
        self.melee = False # we want to set the attacking status to false
        self.melee_time = None
        self.melee_cooldown = 1000
        self.melee_speed = 0.1
        self.animation_melee = False
        self.frame_melee_index = 0

        self.direction = pygame.math.Vector2() # x and y for movement
        self.speed = 2
        self.stamina = 100
        self.health = 100
        self.gold = 0
        self.damage = 50 

        # damage flash system
        self.damaged = False  # nou: indicator că jucătorul a fost lovit recent
        self.last_damaged_time = 0  # nou: timpul ultimei lovituri
        self.damage_flash_duration = 200  # nou: cât timp apare overlay-ul (în ms)
        self.can_flash = True  # nou: permite afișarea flash-ului doar dacă e activ
        self.flash_cooldown = 900  # nou: timp minim între flash-uri
        self.last_flash_time = 0  # nou: marcăm momentul când a fost ultimul flash
        
        self.weapon_index = 0 # we want to set the weapon index to 0 so that we can use the first weapon
        self.weapon = list(weapon_data.keys())[self.weapon_index] # we want to set the weapon to the first weapon in the list
        self.weapon = Weapon(self, groups) # we create the weapon and add it to the visible sprites
        
        self.is_dashing = False
        self.dash_start_time = 0
        self.dash_duration = 200  # Dash lasts 0.8 seconds (in milliseconds)
        self.dash_animation_speed = 0.3  # Faster animation speed during dash
        self.dash_c = False
        self.dash_cooldown = 4000
        
        self.obstacle_sprites = obstacle_sprites # we need this to check for collisions with the obstacles
        # self.visible_sprites = visible_sprites
        self.last_shot = 0
        self.shot_cooldown = 500  

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
        mouse_x, mouse_y = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        # Reset direction vector before setting it
        self.direction.x = 0
        self.direction.y = 0

        if keys[pygame.K_w] and not keys[pygame.K_s]:
            self.direction.y = -1
            self.walk_status = 'up'
        elif keys[pygame.K_s] and not keys[pygame.K_w]:
            self.direction.y = 1
            self.walk_status = 'down'
        else:
            self.walk_status = ''
            self.direction.y = 0

        if keys[pygame.K_a] and not keys[pygame.K_d]:
            self.direction.x = -1
            self.walk_status = self.walk_status + 'left'
        elif keys[pygame.K_d] and not keys[pygame.K_a]:
            self.direction.x = 1
            self.walk_status = self.walk_status + 'right'
        else:
            self.direction.x = 0
            self.walk_status = self.walk_status.replace('left', '')
            self.walk_status = self.walk_status.replace('right', '')
            
        if keys[pygame.K_LSHIFT]: #sprint
            if self.stamina > 0 and (self.status in self.walk_status):
                self.speed = 4
                self.stamina -= 0.4 # we want to decrease the stamina when we sprint
            else:
                self.speed = 2
        else:
            self.speed = 2
            if 'idle' in self.status:
                self.stamina += 0.8
            else:
                self.stamina += 0.4
                
        if keys[pygame.K_SPACE] and not self.is_dashing and self.stamina >= 35 and self.dash_c == False:
            self.is_dashing = True
            self.dash_start_time = pygame.time.get_ticks()
            self.stamina -= 35  # Reduce stamina when dashing
            self.dash_c = True
        
        self.stamina = max(0, min(self.stamina, 100))

        m = HEIGHT / WIDTH
        diag1_y = m * mouse_x
        diag2_y = -m * mouse_x + HEIGHT

        if mouse_y > diag1_y and mouse_y > diag2_y:
            self.status = 'down' 
        elif mouse_y < diag1_y and mouse_y > diag2_y:
            self.status = 'right'
        elif mouse_y < diag1_y and mouse_y < diag2_y:
            self.status = 'up'
        elif mouse_y > diag1_y and mouse_y < diag2_y:
            self.status = 'left'

        #attack
        if mouse[0] and self.melee == False:
            print('attack')
            self.melee = True
            self.melee_time = pygame.time.get_ticks() # we get the current time in milliseconds
            self.animation_melee = True
            self.animation_speed = self.melee_speed
            self.frame_melee_index = 0
            self.frame_index = 0 # we want to reset the frame index so that we can see the attack animation

            for enemy in self.level.enemies:
                if self.rect.colliderect(enemy.rect):
                    enemy.take_damage(100)  # folosim metoda corectă
                    if enemy.health <= 0:
                        enemy.kill()

    def move(self, speed):
        if self.direction.x != 0 and self.direction.y != 0:
            speed = 2
            if self.speed == 4:
                speed = 3
            if self.speed == 16:
                speed = 11
        
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center # we want to move the rect with the hitbox so that we can see the player moving

    def dash(self):
        if self.is_dashing:
            current_time = pygame.time.get_ticks()
            if current_time - self.dash_start_time <= self.dash_duration:
                self.speed = 16  # Increase speed during dash
                self.animation_speed = self.dash_animation_speed  # Speed up animation
            else:
                self.is_dashing = False
                self.speed = 4  # Reset to normal speed
                self.animation_speed = 0.1  # Reset animation speed to the normal one

    def shoot(self):
        mouse = pygame.mouse.get_pressed()
        if not mouse[2]:
            return
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot < self.shot_cooldown:
            return
        self.last_shot = current_time
        bullet = Bullet(self.weapon.rect.center, self.weapon.direction,
                        [self.level.visible_sprites, self.level.bullets],
                        self.obstacle_sprites, self.level.enemies, self, self.damage)
        self.level.bullets.add(bullet)

    def cooldown_dash(self):
        current_time = pygame.time.get_ticks()
        if self.dash_c == True:
            if current_time - self.dash_start_time >= self.dash_cooldown:
                self.dash_c = False

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
        current_width = (self.stamina / 100) * 300
        background_color = 'black'
        color = 'white'
        pygame.draw.rect(surface, background_color, (10, 80, 300, 35), border_radius = 20)
        pygame.draw.rect(surface, color, (10, 80, current_width, 35), border_radius = 20)

    def draw_health_bar(self, surface):
        current_width = (self.health / 100) * 300
        background_color = 'red'
        color = 'green'
        pygame.draw.rect(surface, background_color, (10, 20, 300, 35), border_radius = 20)
        pygame.draw.rect(surface, color, (10, 20, current_width, 35), border_radius = 20)

    def draw_gold(self, surface):
        font = pygame.font.Font(None, 32)
        text = font.render(f"Gold: {self.gold}", True, 'yellow')
        surface.blit(text, (10, 130))

    # Function to take damage
    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0
        if self.health == 0:
            print('Player is dead')

        current_time = pygame.time.get_ticks()
        if self.can_flash:
            self.damaged = True
            self.last_damaged_time = current_time
            self.can_flash = False
            self.last_flash_time = current_time

    def draw_gold(self, surface):
        font = pygame.font.Font(None, 32)
        text = font.render(f"Gold: {self.gold}", True, 'yellow')
        surface.blit(text, (10, 130))

    def update(self):
        self.input()
        self.cooldown_melee()    
        self.cooldown_dash()
        self.get_status()
        self.weapon.update_weapon()
        self.shoot()
        self.dash()
        self.animate()
        self.move(self.speed)

        # cooldown pentru flash roșu (nu se poate activa non-stop)
        if not self.can_flash:
            if pygame.time.get_ticks() - self.last_flash_time > self.flash_cooldown:
                self.can_flash = True

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

    def cooldown_melee(self):
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
