import pygame, sys
from level import Level
from support import WIDTH, HEIGHT, FPS
from ui import MainMenu, PauseMenu

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Endless Survival')
        self.clock = pygame.time.Clock()

        self.main_menu = MainMenu()
        self.pause_menu = PauseMenu()

        self.font = pygame.font.SysFont(None, 60)
        self.small_font = pygame.font.SysFont(None, 40)

        self.game_state = 'menu'
        self.level = None

    def reset_game(self):
        self.level = Level()
        self.game_state = 'playing'

    def handle_events(self):
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

    def update(self):
        if self.game_state == 'menu':
            self.main_menu.run(self.screen)

        elif self.game_state == 'paused':
            self.pause_menu.run(self.screen)

        elif self.game_state == 'playing':
            self.level.run()

            # Desenăm flash roșu dacă a fost lovit
        if self.level.player.damaged:
            current_time = pygame.time.get_ticks()
            if current_time - self.level.player.last_damaged_time < self.level.player.damage_flash_duration:
                red_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                red_overlay.fill((255, 0, 0, 80))  # RGBA, 80 = transparență
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

    def run(self):
        self.reset_game()
        while True:
            self.handle_events()
            self.update()
            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()
