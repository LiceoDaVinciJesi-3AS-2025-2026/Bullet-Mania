import pygame

from bullet_mania.config.gameConfig import RENDER_SIZE
from bullet_mania.data import assets

from bullet_mania.vfxManager import draw_bullet_bloom_effect

import bullet_mania.data.player as player
import bullet_mania.data.world as world
import bullet_mania.data.vfx as vfx

RENDER_WIDTH, RENDER_HEIGHT = RENDER_SIZE

shoot_sound = pygame.mixer.Sound("src/bullet_mania/assets/sounds/sfx/gun_shoot.mp3")
shoot_sound.set_volume(0.12)

shell_falling_sound = pygame.mixer.Sound("src/bullet_mania/assets/sounds/sfx/gun_shell_falling.mp3")
shell_falling_sound.set_volume(0.05)

reload_sound = pygame.mixer.Sound("src/bullet_mania/assets/sounds/sfx/gun_reload.mp3")
reload_sound.set_volume(0.15)

def shoot(position, mouse_pos, owner_id="local", velocity=.5, lifetime=1500):
    if player.MAG_AMMO > 0 and player.IS_RELOADING == False:
        player.MAG_AMMO -= 1

        player_center = pygame.Vector2(position)
        mouse_vec = pygame.Vector2(mouse_pos)

        direction = mouse_vec - player_center

        if direction.length() != 0:
            direction = direction.normalize()

        vfx.HAS_SHOT = True
        vfx.SHOT_TIME = 0.0

        world.BULLETS.append([
            [player_center.x, player_center.y],
            direction,
            velocity,
            lifetime,
            owner_id
        ])

        shoot_sound.play()
        shell_falling_sound.play()

def start_reload():
    if not player.IS_RELOADING and player.MAG_AMMO < 10:
        player.IS_RELOADING = True

def reload():
    player.IS_RELOADING = False
    player.LAST_RELOAD_TIME = 0
    player.AMMO -= player.MAG_SIZE if player.AMMO >= player.MAG_SIZE else player.AMMO
    player.MAG_AMMO = player.MAG_SIZE

    reload_sound.play()

def place_bullet_hole(position):
    vfx.BULLET_HOLES.append([
        position,
        0.0
    ])

def draw_bullet_hole(render_surface: pygame.Surface, bullet_hole_position: list | tuple, bullet_hole_lifetime: float):
    progress = (bullet_hole_lifetime / vfx.BULLET_HOLE_DURATION)**2
    alpha = max(0, 255 - int(progress * 255))

    bullet_hole = assets.ASSETS["bullet_hole"]
    scaled_bullet_hole = pygame.transform.scale_by(bullet_hole, .4)
    scaled_bullet_hole.set_alpha(alpha)

    render_surface.blit(scaled_bullet_hole, bullet_hole_position)

def draw_bullet(render_surface: pygame.Surface, bullet_position: list | tuple, bullet_name: str):
    draw_bullet_bloom_effect(render_surface, bullet_position, 8, (255, 34, 0, 110))
    render_surface.blit(pygame.transform.scale_by(assets.ASSETS[bullet_name], 0.8), bullet_position)
