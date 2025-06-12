from support import WIDTH, HEIGHT
import pygame, sys

class Button:
    def __init__(self, text, width, height, pos):
        self.rect = pygame.Rect(pos[0], pos[1], width, height)
        self.color = '#475F77'
        self.hover_color = '#576D87'
        self.text = pygame.font.Font(None, 32).render(text, True, 'White')
        self.text_rect = self.text.get_rect(center=self.rect.center)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(screen, current_color, self.rect, border_radius=8)
        screen.blit(self.text, self.text_rect)
        return self.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]


class MainMenu:
    def __init__(self):
        self.play_button = Button("Play", 200, 40, (WIDTH//2 - 100, HEIGHT//2 - 70))
        self.settings_button = Button("Settings", 200, 40, (WIDTH//2 - 100, HEIGHT//2 ))
        self.quit_button = Button("Quit", 200, 40, (WIDTH//2 - 100, HEIGHT//2 + 70))
        self.title_font = pygame.font.Font(None, 72)

    def draw(self, screen):
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
        self.overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 128))  # Overlay semi-transparent
        self.font = pygame.font.Font(None, 74)
        self.button_menu = Button("Main Menu", 200, 40, (WIDTH //2 - 100, HEIGHT - 300))
        
    def draw(self, screen):
        screen.blit(self.overlay, (0, 0))
        # Text pauză
        text = self.font.render("PAUSED - Press ESC to resume", True, 'White')
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text,text_rect)

        if self.button_menu.draw(screen):
            return "menu"
        return "paused"
    
class UpgradeMenu:
    def __init__(self, upgrades):
        self.overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 180))
        self.upgrades = upgrades
        self.buttons = []
        start_y = HEIGHT // 2 - 60
        for i, up in enumerate(upgrades):
            btn = Button(f"{up['name']} ({up['cost']})", 250, 40, (WIDTH//2 - 125, start_y + i*60))
            self.buttons.append(btn)
        self.skip_button = Button("Skip", 250, 40, (WIDTH//2 - 125, start_y + len(upgrades)*60))

    def draw(self, screen, player):
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