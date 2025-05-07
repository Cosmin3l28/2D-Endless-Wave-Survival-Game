import pygame, sys
from level import Level
from support import WIDTH, HEIGTH, FPS
from ui import MainMenu, PauseMenu


class Game:
    def __init__(self):

        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        pygame.display.set_caption('Endless Survival')
        self.clock = pygame.time.Clock()
        
        self.main_menu = MainMenu()
        self.pause_menu = PauseMenu()

        #actual state
        self.game_state = 'menu'
        self.level = None

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.game_state == "playing":
                        self.game_state = "paused"
                    elif self.game_state == "paused":
                        self.game_state = "playing"


    def run(self):
        while True:
            
            self.handle_events()
            if self.game_state == 'menu':
                menu_result = self.main_menu.draw(self.screen)
                if menu_result == "play":
                    self.level = Level()
                    self.game_state = "playing"
                elif menu_result == "quit":
                    pygame.quit()
                    sys.exit()
            
            elif self.game_state == "playing":
                self.screen.fill('#47ABA9')
                self.level.run()

            elif self.game_state == "paused":
                self.level.visible_sprites.custom_draw(self.level.player)  # Redesenează ultimul frame
                pause_result = self.pause_menu.draw(self.screen)
                if pause_result == 'menu':
                    self.level = None
                    self.game_state = "menu"

            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()