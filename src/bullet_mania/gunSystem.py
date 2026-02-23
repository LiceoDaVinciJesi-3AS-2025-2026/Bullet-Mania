import pygame

from bullet_mania.config.gameConfig import RENDER_SIZE, WINDOW_SIZE
from bullet_mania.data import assets
import bullet_mania.data.player as player
import bullet_mania.data.world as world
import bullet_mania.data.vfx as vfx

RENDER_WIDTH, RENDER_HEIGHT = RENDER_SIZE

def shoot(position, mouse_pos, owner_id="local", velocity=.2, lifetime=5000):
    if player.AMMO > 0 and player.IS_RELOADING == False:
        player.AMMO -= 1

        player_pos = pygame.Vector2(position)
        mouse_pos = pygame.Vector2(mouse_pos)

        direction = mouse_pos - player_pos

        if direction.length() != 0:
            direction = direction.normalize()
        
        vfx.HAS_SHOT = True
        vfx.SHOT_TIME = 0.0

        world.BULLETS.append([ [player_pos[0], player_pos[1]], direction, velocity, lifetime, owner_id ])

def reload():
    if not player.IS_RELOADING and player.AMMO < 10:
        player.IS_RELOADING = True

def draw_bullet(render_surface: pygame.Surface, bullet_position: list | tuple, bullet_name: str):
    render_surface.blit(assets.ASSETS[bullet_name], bullet_position)
