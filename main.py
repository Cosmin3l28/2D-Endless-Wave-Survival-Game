"""Entry point for running the Endless Survival game."""
import pygame, sys
import random
from support import upgrade_pool
from level import Level
from support import WIDTH, HEIGHT, FPS
from ui import MainMenu, PauseMenu, UpgradeMenu


class Game:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    @classmethod
    def get_instance(cls) -> 'Game':
        return cls()

    def __init__(self):
        """Initialize the game, setting up the display, menus, and initial state."""
        if self._initialized:
            return
        self._initialized = True
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Endless Survival')
        self.clock = pygame.time.Clock()
        self.main_menu = MainMenu()
        self.pause_menu = PauseMenu()
        self.upgrade_pool = upgrade_pool
        self.rarity_weights = {'common': 10, 'rare': 2}
        self.upgrade_menu = None
        self.current_wave = 1
        self.font = pygame.font.SysFont(None, 60)
        self.small_font = pygame.font.SysFont(None, 40)
        self.rarity_weights = {'common': 10, 'rare': 2}
        self.upgrade_menu = None
        self.current_wave = 1
        self.game_state = 'menu'
        self.level = None

    def generate_upgrade_menu(self) -> None:
        """Generate a random selection of upgrades from the upgrade pool."""
        pool = self.upgrade_pool[:]
        selected = []
        for _ in range(min(3, len(pool))):
            weights = [self.rarity_weights[u['rarity']] for u in pool]
            choice = random.choices(pool, weights=weights, k=1)[0]
            selected.append(choice)
            pool.remove(choice)
        self.upgrade_menu = UpgradeMenu(selected)

    def reset_game(self) -> None:
        """Reset the game to the initial state."""
        self.level = Level()
        self.game_state = 'playing'

    def handle_events(self) -> None:
        """Handle user input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if self.game_state == "playing":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.game_state = "paused"

            elif self.game_state == "paused":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.game_state = "playing"

            elif self.game_state == "game_over":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.new_game_rect.collidepoint(event.pos):
                        self.reset_game()
                    elif self.exit_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

    def update(self) -> None:
        """Update the game state and handle transitions between menus."""
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
            
        elif self.game_state == 'upgrade':
            upgrade_result = self.upgrade_menu.draw(self.screen, self.level.player)
            if upgrade_result == 'close':
                self.current_wave += 1
                self.level.start_wave(self.current_wave)
                self.game_state = 'playing'

        if self.level.player.damaged:
            print("Player damaged, flashing red")
            current_time = pygame.time.get_ticks()
            if current_time - self.level.player.last_damaged_time < self.level.player.damage_flash_duration:
                red_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                red_overlay.fill((255, 0, 0, 80))  # RGBA, 80 = transparency
                self.screen.blit(red_overlay, (0, 0))
            else:
                self.level.player.damaged = False

            if self.level.player.health <= 0:
                self.level.player.health = 0
                self.game_state = "game_over"

        elif self.game_state == 'game_over':
            self.screen.fill((0, 0, 0))
            text = self.font.render("YOU DIED", True, (255, 0, 0))
            self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 100))

            new_game_text = self.small_font.render("New Game", True, (255, 255, 255))
            exit_text = self.small_font.render("Exit", True, (255, 255, 255))
            self.new_game_rect = new_game_text.get_rect(center=(WIDTH // 2, 250))
            self.exit_rect = exit_text.get_rect(center=(WIDTH // 2, 320))

            self.screen.blit(new_game_text, self.new_game_rect)
            self.screen.blit(exit_text, self.exit_rect)

    def run(self) -> None:
        """Start the game loop."""
        self.reset_game()
        while True:     
            self.handle_events()                
            self.update()
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game().get_instance()
    game.run()
