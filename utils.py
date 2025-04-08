import pygame, os
import re

#problem : the arena rect is moving with the camera, but it should be static
#solution : create a new rect for the arena that is not affected by the camera
class Arena:
    def __init__(self, game, width, height):
        self.game = game
        self.width = width
        self.height = height
        self.arena_rect = pygame.Rect(50, 50, width, height)
    
    def render_background(self):
        # Load and render the background image
        self.game.screen.blit(self.game.assets['background'], (0 - self.game.camera.camera_scroll[0], 0 - self.game.camera.camera_scroll[1])) # draw the background
        # Draw the arena rectangle independently of the camera
        # Calculate the position of the arena rectangle relative to the background
        arena_position = (50, 50)
        self.arena_rect.topleft = (arena_position[0] - self.game.camera.camera_scroll[0], arena_position[1] - self.game.camera.camera_scroll[1])
        pygame.draw.rect(self.game.screen, (255, 0, 0), self.arena_rect, 1) # draw the arena rectangle for debugging
    
    def handle_collision(self):
        # Check for collision with the arena boundaries
        if self.game.player.position[0] < self.arena_rect.left + self.game.camera.camera_scroll[0]:
            self.game.player.position[0] = self.arena_rect.left + self.game.camera.camera_scroll[0]
        if self.game.player.position[0] + self.game.player.size[0] > self.arena_rect.right + self.game.camera.camera_scroll[0]:
            self.game.player.position[0] = self.arena_rect.right + self.game.camera.camera_scroll[0] - self.game.player.size[0]
        if self.game.player.position[1] < self.arena_rect.top + self.game.camera.camera_scroll[1]:
            self.game.player.position[1] = self.arena_rect.top + self.game.camera.camera_scroll[1]
        if self.game.player.position[1] + self.game.player.size[1] > self.arena_rect.bottom + self.game.camera.camera_scroll[1]:
            self.game.player.position[1] = self.arena_rect.bottom + self.game.camera.camera_scroll[1] - self.game.player.size[1]

#https://www.youtube.com/watch?v=u7LPRqrzry8&t=84s   
class Camera:
    def __init__(self, game ,width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.camera_scroll = [0, 0]
        self.game = game

    def update_camera_scroll(self):
        self.camera_scroll[0] +=  self.game.player.rectangle().centerx - int(self.width / 2) - self.camera_scroll[0]
        self.camera_scroll[1] +=  self.game.player.rectangle().centery - int(self.height / 2) - self.camera_scroll[1]

        # Keep the camera within the bounds of the world
        if(self.camera_scroll[0] < 0):
            self.camera_scroll[0] = 0
        if(self.camera_scroll[1] < 0):
            self.camera_scroll[1] = 0
        if(self.camera_scroll[0] > self.game.assets['background'].get_width() - self.width):
            self.camera_scroll[0] = self.game.assets['background'].get_width() - self.width
        if(self.camera_scroll[1] > self.game.assets['background'].get_height() - self.height):
            self.camera_scroll[1] = self.game.assets['background'].get_height() - self.height

def load_images_from_folder(folder):
    # the basic sort is not working because the files are not sorted by number so we need to sort them by number
    # we need to sort the files by number so we can load them in the right order
    # this is a regex to extract the number from the filename
    def extract_number(filename):
        match = re.search(r'\d+', filename)
        return int(match.group()) if match else float('inf')

    images = []
    sorted_files = sorted(os.listdir(folder), key=extract_number)
    for filename in sorted_files:
        img = pygame.image.load(os.path.join(folder, filename)).convert_alpha()
        images.append(img)
    return images

class Animation:
    def __init__(self, frames, frame_duration, loop=True):
        self.frames = frames
        self.loop = loop
        self.game_frame_index = 0
        self.frame_duration = frame_duration
        self.done = False

    def copy(self):
        return Animation(self.frames, self.frame_duration, self.loop)
    
    def animate(self, min_frame_index=0, max_frame_index=None):
        if max_frame_index is None:
            max_frame_index = len(self.frames)
        if self.loop:
            self.game_frame_index = (self.game_frame_index + 1) % (self.frame_duration * max_frame_index) + min_frame_index
        else: 
            self.game_frame_index = min(self.game_frame_index + 1, self.frame_duration * max_frame_index - 1)
            if self.game_frame_index >= self.frame_duration * max_frame_index - 1:
                self.done = True
       
    def get_frame(self):
        return self.frames[int(self.game_frame_index / self.frame_duration)]
    
class Stamina_Bar:
    def __init__(self, game, position, size, color=(255,255,255), max_stamina=100):
        self.game = game
        self.position = position
        self.size = size
        self.color = color
        self.max_stamina = max_stamina
        self.current_stamina = max_stamina

    def render(self):
        # Calculate the width of the stamina bar based on the current stamina
        width = int((self.current_stamina / self.max_stamina) * self.size[0])
        pygame.draw.rect(self.game.screen, (0, 0, 0), (self.position[0], self.position[1], self.size[0], self.size[1]))  # Draw the background
        pygame.draw.rect(self.game.screen, self.color, (self.position[0], self.position[1], width, self.size[1]))

    def stamina_regen(self):
        if self.game.player.running == False:  
            if self.current_stamina < self.max_stamina:
                if self.game.player.stationary == True:
                    self.current_stamina += 20/self.game.framerate
                self.current_stamina += 10/self.game.framerate  # Adjust the regeneration rate as needed
                if self.current_stamina > self.max_stamina:
                    self.current_stamina = self.max_stamina

    def stamina_deplete(self):
        if self.current_stamina > 0:
            self.current_stamina -= 20/self.game.framerate
            if self.current_stamina < 0:
                self.current_stamina = 0

    def dash_deplete(self):
        if self.current_stamina > 0:
            self.current_stamina -= 40
            if self.current_stamina < 0:
                self.current_stamina = 0