import pygame
import utils

class Entity:
    def __init__(self, game, entity_type, position, size):       
        self.game = game
        self.type = entity_type
        self.position = list(position)
        self.size = size

        self.action = '' # default action
        self.set_action('idle/idle') # set the default action to idle
        self.flip = False # default flip
        self.speed = 80 # default speed
        
    
    def rectangle(self, offset=(0,0)):
        return pygame.Rect(self.position[0] - offset[0], self.position[1] - offset[1] , self.size[0], self.size[1])

    def set_action(self, action):
        if action != self.action:
            #set the action to the new action
            self.action = action
            #get the new animation from the game files
            self.animation = self.game.assets[self.type + '/' + self.action].copy()

    def update(self, movement=(0,0,0,0)):
        if (movement[0] and (movement[2] or movement[3])) or (movement[1] and (movement[2] or movement[3])):
            # moving the player diagonally makes him move faster due to the pythagorean theorem
            self.position[0] += (movement[3] - movement[2]) * self.game.delta_time * self.speed * 0.7071
            self.position[1] += (movement[1] - movement[0]) * self.game.delta_time * self.speed * 0.7071
        else:
            self.position[0] += (movement[3] - movement[2]) * self.game.delta_time * self.speed
            self.position[1] += (movement[1] - movement[0]) * self.game.delta_time * self.speed

        entity_rectangle = self.rectangle() 
        if movement[3] == True:
            self.flip = False
        elif movement[2] == True:
            self.flip = True
            
            

    def render(self, surface, offset=(0,0)):

        surface.blit(pygame.transform.flip(self.animation.get_frame(), self.flip, False), (self.position[0] - offset[0], self.position[1] - offset[1]))
        # Draw the entity rectangle for debugging
        pygame.draw.rect(surface, (255, 0, 0), self.rectangle(offset), 1)

class Player(Entity):
    def __init__(self, game, entity_type, position, size):
        super().__init__(game, entity_type, position, size)
        self.idle_up = False
        self.idle_down = False
        self.idle = False
        self.running = False
        self.stamina = utils.Stamina_Bar(game, (10, 10), (100, 10)) # create a stamina bar for the player
        self.counter = 0
        self.stationary = True # if the player is not moving
        self.dash = False

    def update_idle_up(self):
        self.idle_up = True
        self.idle_down = False
        self.idle = False 

    def update_idle_down(self):
        self.idle_down = True
        self.idle_up = False
        self.idle = False
    
    def update_idle(self):
        self.idle = True
        self.idle_up = False
        self.idle_down = False
    
    def not_moving(self, movement=(0,0,0,0)):
        if(not movement[0] and not movement[1] and not movement[2] and not movement[3]):
            self.stationary = True
            if(self.idle_up):
                self.set_action('idle/idle_up')     
            elif(self.idle_down):
                self.set_action('idle/idle_down')
            else:
                self.set_action('idle/idle')
            return True
        return False
    
    def update(self, movement=(0,0,0,0)):
        super().update(movement)
        # Add any player-specific update logic here
        # For example, you can handle player-specific actions or states
        if not self.not_moving(movement):
            self.stationary = False
        
        if self.running and self.stamina.current_stamina > 0:
            
            self.stamina.stamina_deplete()
            self.stamina.render()

            self.speed = 110 # increase the speed of the player
            if movement[0]:
                self.set_action('run/run_up')
                self.update_idle_up()
            elif movement[1]:
                self.set_action('run/run_down')
                self.update_idle_down()
            elif movement[3]:
                self.set_action('run/run')
                self.update_idle()
            elif movement[2]:
                self.set_action('run/run')
                self.update_idle()
            self.not_moving(movement)

        else:

            self.stamina.stamina_regen()
            self.stamina.render()
            
            self.speed = 40
            if movement[0]: # Up
                self.set_action('walk/walk_up')
                self.update_idle_up()
            elif movement[1]: # Down
                self.set_action('walk/walk_down')
                self.update_idle_down()
            elif movement[3]: # Rights
                self.set_action('walk/walk')
                self.update_idle()
            elif movement[2]:
                self.set_action('walk/walk')
                self.update_idle()
            self.not_moving(movement)
            
            
        if self.dash and self.stamina.current_stamina >= 40 and self.stationary == False:
            self.stamina.dash_deplete()
            self.stamina.render()
            self.dash = False
            for i in range(0, 4):
                if movement[i] == True and i == 0:
                    self.position[1] -= 40
                if movement[i] == True and i == 1:
                    self.position[1] += 40
                if movement[i] == True and i == 2:
                    self.position[0] -= 40
                if movement[i] == True and i == 3:
                    self.position[0] += 40

            # Handle diagonal dashes
            if movement[0] and movement[2]:  # Up-Left
                self.position[0] -= 28.28  # 40 * 0.7071
                self.position[1] -= 28.28
            if movement[0] and movement[3]:  # Up-Right
                self.position[0] += 28.28
                self.position[1] -= 28.28
            if movement[1] and movement[2]:  # Down-Left
                self.position[0] -= 28.28
                self.position[1] += 28.28
            if movement[1] and movement[3]:  # Down-Right
                self.position[0] += 28.28
                self.position[1] += 28.28
            
        self.animation.animate() # animate the player

class Enemy(Entity):
    def __init__(self, game, entity_type, position, size):
        super().__init__(game, entity_type, position, size)
        self.speed = 40 # default speed
        self.animation = self.game.assets[self.type + '/' + self.action].copy()
        self.direction = (0,0) # default direction
        self.flip = False # default flip
    

