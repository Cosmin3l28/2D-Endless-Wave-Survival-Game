"""Utility helpers for debugging information on screen."""

import pygame

pygame.init()

pygame.init()
font = pygame.font.Font(None, 30)

def debug(info: any, y: int = 10, x: int = 10) -> None:
    """Draw debugging information to the screen.

    Args:
        info (any): Information to display.
        y (int, optional): Vertical offset. Defaults to 10.
        x (int, optional): Horizontal offset. Defaults to 10.
    """
    display_surface = pygame.display.get_surface()
    debug_surf = font.render(str(info), True, "White")
    debug_rect = debug_surf.get_rect(topleft=(x, y))
    pygame.draw.rect(display_surface, "Black", debug_rect)
    display_surface.blit(debug_surf, debug_rect)