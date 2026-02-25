import pygame
import bullet_mania.data.assets as assets

vignette_image = None
muzzle_fire_image = None

import bullet_mania.data.assets as assets

vignette_image = None
muzzle_fire_image = None

def draw_bullet_bloom_effect(render_surface: pygame.Surface, position: list | tuple, size: float, color: list | tuple):
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

def draw_muzzle_fire_effect(render_surface: pygame.Surface, position: list | tuple, alpha: int, rotation: float):
    global muzzle_fire_image

    if muzzle_fire_image is None:
        muzzle_fire_image = assets.ASSETS["muzzle_fire"]
    
    if muzzle_fire_image.get_alpha() != alpha:
        muzzle_fire_image.set_alpha(alpha)
    
    if rotation:
        muzzle_fire_image = pygame.transform.rotate(muzzle_fire_image, rotation)

    render_surface.blit(muzzle_fire_image, position)

def draw_vignette_effect(render_surface: pygame.Surface, alpha: int):
    global vignette_image

    if vignette_image is None:
        vignette_image = assets.ASSETS["vignette"]
    
    if vignette_image.get_alpha() != alpha:
        vignette_image.set_alpha(alpha)

    render_surface.blit(vignette_image, (0, 0))
