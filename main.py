import pygame, sys
from settings import *
from level import Level

class Game:
    def __init__(self):
        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        pygame.display.set_caption('Zombie Survival')
        self.clock = pygame.time.Clock()
        
        # level setup
        self.level = Level()
    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill('#47ABA9')
            self.level.run()  # rulează nivelul
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()