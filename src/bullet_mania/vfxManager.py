import pygame
import bullet_mania.data.assets as assets

def draw_bullet_bloom_effect(render_surface: pygame.Surface, position, size, color):
    bloom_surface = pygame.Surface((size*2, size*2), pygame.SRCALPHA)

    pygame.draw.circle(
        bloom_surface,
        color,
        (size, size),
        size
    )

    render_surface.blit(
        bloom_surface,
        (position[0] - size/2, position[1] - size/2)
    )

def draw_vignette_effect(render_surface: pygame.Surface, alpha: int):
    vignette = assets.ASSETS["vignette"]
    vignette.set_alpha(alpha)
    render_surface.blit(vignette, (0, 0))
