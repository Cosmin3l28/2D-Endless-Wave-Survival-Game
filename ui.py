"""Menu and UI components for the game."""
import pygame
from player import Player
from support import WIDTH, HEIGHT

class Button:
    def __init__(self, 
                 text: str, 
                 width: int, 
                 height: int, 
                 pos: tuple):
        """Initialize a button with text, size, and position."""
        self.rect = pygame.Rect(pos[0], pos[1], width, height)
        self.color = '#475F77'
        self.hover_color = '#576D87'
        self.text = pygame.font.Font(None, 32).render(text, True, 'White')
        self.text_rect = self.text.get_rect(center=self.rect.center)

    def draw(self, screen: pygame.Surface) -> bool:
        """Draw the button on the screen and check for interactions.

        Args:
            screen (pygame.Surface): The surface to draw the button on.

        Returns:
            bool: True if the button is clicked, False otherwise.
        """
        mouse_pos = pygame.mouse.get_pos()
        current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(screen, current_color, self.rect, border_radius=8)
        screen.blit(self.text, self.text_rect)
        return self.rect.collidepoint(
            mouse_pos) and pygame.mouse.get_pressed()[0]


class MainMenu:
    def __init__(self):
        """Initialize the main menu with buttons and title."""
        self.play_button = Button("Play", 200, 40, (WIDTH//2 - 100, HEIGHT//2 - 70))
        self.settings_button = Button("Settings", 200, 40, (WIDTH//2 - 100, HEIGHT//2 ))
        self.quit_button = Button("Quit", 200, 40, (WIDTH//2 - 100, HEIGHT//2 + 70))
        self.title_font = pygame.font.Font(None, 72)

    def draw(self, screen: pygame.Surface) -> str:
        """Draw the main menu and check for button interactions.

        Args:
            screen (pygame.Surface): The surface to draw the menu on.

        Returns:
            str: The action to take based on button clicks.
        """
        screen.fill('#47ABA9')
        title_surf = self.title_font.render("Endless Survival", True, 'White')
        title_rect = title_surf.get_rect(center=(WIDTH//2, HEIGHT//4))
        screen.blit(title_surf, title_rect)
        
        if self.play_button.draw(screen):
            return "play"
        if self.settings_button.draw(screen):
            return "settings"
        if self.quit_button.draw(screen):
            return "quit"
        return "menu"
    
class PauseMenu:
    def __init__(self):
        """Initialize the pause menu with an overlay and buttons."""
        self.overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 128))  # Overlay semi-transparent
        self.font = pygame.font.Font(None, 74)
        self.button_menu = Button("Main Menu", 200, 40, (WIDTH //2 - 100, HEIGHT - 300))

    def draw(self, screen: pygame.Surface) -> str:
        """Draw the pause menu and check for button interactions.

        Args:
            screen (pygame.Surface): The surface to draw the menu on.

        Returns:
            str: The action to take based on button clicks.
        """
        screen.blit(self.overlay, (0, 0))
        text = self.font.render("PAUSED - Press ESC to resume", True, 'White')
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text,text_rect)

        if self.button_menu.draw(screen):
            return "menu"
        return "paused"
    
class UpgradeMenu:
    def __init__(self, upgrades: list):
        """Initialize the upgrade menu with an overlay and buttons for each upgrade."""
        self.overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 180))
        self.upgrades = upgrades
        self.buttons = []
        start_y = HEIGHT // 2 - 60
        for i, up in enumerate(upgrades):
            btn = Button(f"{up['name']} ({up['cost']})", 250, 40, (WIDTH//2 - 125, start_y + i*60))
            self.buttons.append(btn)
        self.skip_button = Button("Skip", 250, 40, (WIDTH//2 - 125, start_y + len(upgrades)*60))

    def draw(self, screen: pygame.Surface, player: Player) -> str:
        """Draw the upgrade menu and check for button interactions.

        Args:
            screen (pygame.Surface): The surface to draw the menu on.
            player (Player): The player object to apply upgrades to.

        Returns:
            str: The action to take based on button clicks.
        """
        screen.blit(self.overlay, (0, 0))
        for i, btn in enumerate(self.buttons):
            if btn.draw(screen):
                upgrade = self.upgrades[i]
                if player.gold >= upgrade['cost']:
                    player.gold -= upgrade['cost']
                    upgrade['apply'](player)
                    return 'close'
        if self.skip_button.draw(screen):
            return 'close'
        return 'upgrade'    