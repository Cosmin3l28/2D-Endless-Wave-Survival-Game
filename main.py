import pygame, sys
import random
from level import Level
from support import WIDTH, HEIGHT, FPS
from ui import MainMenu, PauseMenu, UpgradeMenu


class Game:
    def __init__(self):

        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Endless Survival')
        self.clock = pygame.time.Clock()
        
        self.main_menu = MainMenu()
        self.pause_menu = PauseMenu()

        self.upgrade_pool = [
            {'name': 'Health +20', 'cost': 5, 'rarity': 'common', 'apply': lambda p: setattr(p, 'health', p.health + 20)},
            {'name': 'Damage +10', 'cost': 6, 'rarity': 'common', 'apply': lambda p: setattr(p, 'damage', p.damage + 10)},
            {'name': 'Speed +0.5', 'cost': 6, 'rarity': 'common', 'apply': lambda p: setattr(p, 'speed', p.speed + 0.5)},
            {'name': 'Health +50', 'cost': 15, 'rarity': 'rare', 'apply': lambda p: setattr(p, 'health', p.health + 50)},
            {'name': 'Damage +25', 'cost': 18, 'rarity': 'rare', 'apply': lambda p: setattr(p, 'damage', p.damage + 25)},
            {'name': 'Speed +1', 'cost': 20, 'rarity': 'rare', 'apply': lambda p: setattr(p, 'speed', p.speed + 1)},
        ]

        self.rarity_weights = {'common': 10, 'rare': 2}
        self.upgrade_menu = None
        self.current_wave = 1

        #actual state
        self.game_state = 'menu'
        self.level = None

    def generate_upgrade_menu(self):
        pool = self.upgrade_pool[:]
        selected = []
        for _ in range(min(3, len(pool))):
            weights = [self.rarity_weights[u['rarity']] for u in pool]
            choice = random.choices(pool, weights=weights, k=1)[0]
            selected.append(choice)
            pool.remove(choice)
        self.upgrade_menu = UpgradeMenu(selected)

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
                    # Initialize the first wave
                    self.level.start_wave(self.current_wave)
                    self.game_state = "playing"
                elif menu_result == "quit":
                    pygame.quit()
                    sys.exit()
            
            elif self.game_state == "playing":
                self.screen.fill('#47ABA9')
                # Update and draw the level
                wave_done = self.level.run()
                if wave_done:
                    self.generate_upgrade_menu()
                    self.game_state = 'upgrade'

            elif self.game_state == "paused":
                self.level.visible_sprites.custom_draw(self.level.player)  # Redesenează ultimul frame
                pause_result = self.pause_menu.draw(self.screen)
                if pause_result == 'menu':
                    self.level = None
                    self.game_state = "menu"
                
            #upgrade menu
            elif self.game_state == 'upgrade':
                upgrade_result = self.upgrade_menu.draw(self.screen, self.level.player)
                if upgrade_result == 'close':
                    self.current_wave += 1
                    self.level.start_wave(self.current_wave)
                    self.game_state = 'playing'
                    
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()