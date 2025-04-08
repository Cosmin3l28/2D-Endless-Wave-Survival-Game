import pygame, sys, time
import entities
import os
import utils

class Game:
    def __init__(self):
        pygame.init()

        #set the name of the window
        pygame.display.set_caption("survival game")
        #get the resolution of the screen
        self.screen_resolution = pygame.display.Info()
        #set the size of the window
        #self.screen_resolution.current_w
        #self.screen_resolution.current_h
        #https://pyga.me/docs/ref/display.html#pygame.didsplay.set_mode
        #need to make logic for the window to be resizable through the settings menu or something
        #need to add open GL support for the windows
        #need to add douyble buffering for the window
        #need to add vsync for the window
        self.screen = pygame.display.set_mode((389,209), pygame.SCALED|pygame.HWSURFACE)
        self.framerate = 60
        self.mainClock = pygame.time.Clock()
        self.last_time = time.time()
        self.delta_time = 0
        #self.window_icon = pygame.image.load("assets/icon.png")
        self.movement = [False, False, False, False] # up, down, left, righta
        self.assets = {
            'background': pygame.image.load("assets/images/background/background.png").convert_alpha(),
            'player/ninja/idle/idle' : utils.Animation(utils.load_images_from_folder("assets/images/entities/player/ninja/idle/idle"), 10),
            'player/ninja/idle/idle_up' : utils.Animation(utils.load_images_from_folder("assets/images/entities/player/ninja/idle/idle_up"), 10),
            'player/ninja/idle/idle_down' : utils.Animation(utils.load_images_from_folder("assets/images/entities/player/ninja/idle/idle_down"), 10),
            'player/ninja/walk/walk' : utils.Animation(utils.load_images_from_folder("assets/images/entities/player/ninja/walk/walk"), 10),
            'player/ninja/walk/walk_up' : utils.Animation(utils.load_images_from_folder("assets/images/entities/player/ninja/walk/walk_up"), 10),
            'player/ninja/walk/walk_down' : utils.Animation(utils.load_images_from_folder("assets/images/entities/player/ninja/walk/walk_down"), 10),
            'player/ninja/run/run' : utils.Animation(utils.load_images_from_folder("assets/images/entities/player/ninja/run/run"), 10),
            'player/ninja/run/run_up' : utils.Animation(utils.load_images_from_folder("assets/images/entities/player/ninja/run/run_up"), 10),
            'player/ninja/run/run_down' : utils.Animation(utils.load_images_from_folder("assets/images/entities/player/ninja/run/run_down"), 10),
        }
        #create the player entity
        self.player = entities.Player(self, "player/ninja", (0,0), (32,32)) 
   
        self.test_rect = [pygame.Rect(0, 0, 50, 50)] # create a rectangle for the player
        self.camera = utils.Camera(self, self.screen.width, self.screen.height) # create a camera for the player
        self.arena = utils.Arena(self, 635, 300) # create an arena for the player

    def run(self):
        running = True
        # main loop
        while running:
            # every frame, calculate the time it took to render the last frame  
            # (delta time)

            self.mainClock.tick(self.framerate)
            self.delta_time = time.time() - self.last_time
            self.last_time = time.time()
            # calculate the speed of the game

            #https://forum.gdevelop.io/t/solved-character-shaking-not-on-a-wall/38933
            self.arena.render_background() # render the background
            self.player.render(self.screen, self.camera.camera_scroll) # render the player on the screen
            self.player.update(self.movement) # update the player position based on the movement
            self.camera.update_camera_scroll() # update the camera position based on the player position
            # draw the collision area
            #Example for the game speed
            # if fps is 100, delta time is 0.01 so the game speed needs to be delta time * fps = 1
            # if fps is 50, delta time is 0.02 so the game speed needs to be delta time * fps = 1
            # using dela time * fps will make the game speed consistent regardless of the fps
            # https://www.construct.net/en/tutorials/delta-time-framerate-2
            
            self.arena.handle_collision()
                        
            for event in pygame.event.get():
                # check for key pressess
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        self.movement[0] = True
                    if event.key == pygame.K_s:
                        self.movement[1] = True
                    if event.key == pygame.K_a:
                        self.movement[2] = True
                    if event.key == pygame.K_d:
                        self.movement[3] = True
                    if event.key == pygame.K_LSHIFT:
                        self.player.running = True
                    if event.key == pygame.K_SPACE:
                        self.player.dash = True
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                # check for key releases
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        self.movement[0] = False
                    if event.key == pygame.K_s:
                        self.movement[1] = False
                    if event.key == pygame.K_a:
                        self.movement[2] = False
                    if event.key == pygame.K_d:
                        self.movement[3] = False
                    if event.key == pygame.K_SPACE:
                        self.player.dash = False
                    if event.key == pygame.K_LSHIFT:
                        self.player.running = False

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            #update the screen
            pygame.display.update()

Game().run()