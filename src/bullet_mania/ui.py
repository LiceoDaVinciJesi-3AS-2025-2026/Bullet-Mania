import pygame

import bullet_mania.data.player as player

Normalfont = pygame.font.SysFont('Impact', 30, False, False)

def render_ui(screen: pygame.Surface):
    info = Normalfont.render(f"Ammo left: {player.AMMO}", True, "white")
    screen.blit(info, (65, 530))