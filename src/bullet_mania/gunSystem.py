import pygame
import math
import random

from bullet_mania.config.gameConfig import RENDER_SIZE, CHARACTER_SIZE
from bullet_mania.data import assets

from bullet_mania.vfxManager import draw_bullet_bloom_effect

import bullet_mania.data.player as player
import bullet_mania.data.world as world
import bullet_mania.data.vfx as vfx

PLAYER_WIDTH, PLAYER_HEIGHT = CHARACTER_SIZE
RENDER_WIDTH, RENDER_HEIGHT = RENDER_SIZE

shoot_sound = pygame.mixer.Sound("src/bullet_mania/assets/sounds/sfx/gun_shoot.mp3")
shoot_sound.set_volume(0.12)

shell_falling_sound = pygame.mixer.Sound("src/bullet_mania/assets/sounds/sfx/gun_shell_falling.mp3")
shell_falling_sound.set_volume(0.07)

reload_sound = pygame.mixer.Sound("src/bullet_mania/assets/sounds/sfx/gun_reload.mp3")
reload_sound.set_volume(0.15)

current_bullet_hole_image = None
current_bullet_image = None

current_gun_id = None
current_gun_image = None

CURRENT_SHOOTING_ORIGIN = [0.0, 0.0]

def shoot(position, mouse_pos, owner_id="local", velocity=.3, lifetime=1500):
    global CURRENT_SHOOTING_ORIGIN

    if player.MAG_AMMO > 0 and player.IS_RELOADING == False:
        player.MAG_AMMO -= 1

        player_center = pygame.Vector2(CURRENT_SHOOTING_ORIGIN)
        mouse_vec = pygame.Vector2(mouse_pos)
        mouse_vec = pygame.Vector2(
            mouse_vec.x + random.randint(-5, 5),
            mouse_vec.y + random.randint(-5, 5),
        )

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

def draw_gun(render_surface, gun_asset_id, gun_pivot_world, mouse_world, camera_x, camera_y):
    global current_gun_id, current_gun_image, CURRENT_SHOOTING_ORIGIN

    if current_gun_id != gun_asset_id:
        current_gun_image = pygame.transform.scale_by(assets.ASSETS[gun_asset_id], 0.8)
        current_gun_id = gun_asset_id

    img = current_gun_image

    # 1. SISTEMA DI COORDINATE SCHERMO
    # Convertiamo tutto su schermo per avere una mira perfetta
    screen_pivot = pygame.Vector2(
        gun_pivot_world[0] - camera_x + RENDER_WIDTH / 2,
        gun_pivot_world[1] - camera_y + RENDER_HEIGHT / 2
    )
    
    # Invertiamo la tua formula originaria per riottenere il "mouse_render"
    screen_mouse = pygame.Vector2(
        mouse_world[0] - camera_x + player.POSITION[0] + PLAYER_WIDTH,
        mouse_world[1] - camera_y + player.POSITION[1] + PLAYER_HEIGHT
    )

    # 2. CALCOLO DELL'ANGOLO (ORA AFFIDABILE)
    dx = screen_mouse.x - screen_pivot.x
    dy = screen_mouse.y - screen_pivot.y
    angle = math.degrees(math.atan2(-dy, dx))

    # 3. FLIP DELL'ARMA
    # Se stiamo mirando a sinistra (dx negativo su schermo), capovolgiamo l'arma
    if dx < 0:
        img = pygame.transform.flip(img, False, True)

    # 4. MATEMATICA DEL PIVOT (MID-LEFT)
    # Calcoliamo il vettore che va DAL PIVOT (mid-left) AL CENTRO dell'immagine base
    # Dato che il pivot è a X=0 e il centro è a X=w/2, la distanza orizzontale è w/2.
    pivot_to_center = pygame.Vector2(img.get_width() / 2, 0)
    
    # Ruotiamo questo vettore. Usiamo -angle perché pygame.transform.rotate 
    # gira in senso antiorario, ma Vector2.rotate in Pygame gira in senso orario!
    rotated_pivot_to_center = pivot_to_center.rotate(-angle)

    # 5. ROTAZIONE
    rotated_image = pygame.transform.rotate(img, angle)
    rotated_rect = rotated_image.get_rect()

    # 6. POSIZIONAMENTO FINALE
    # Il nuovo centro è semplicemente: (posizione del pivot a schermo) + (vettore ruotato)
    rotated_rect.center = screen_pivot + rotated_pivot_to_center

    muzzle_offset_local = pygame.Vector2(img.get_width(), 0)

    rotated_muzzle_offset = muzzle_offset_local.rotate(-angle)

    muzzle_world = pygame.Vector2(gun_pivot_world) + rotated_muzzle_offset

    CURRENT_SHOOTING_ORIGIN = [muzzle_world.x, muzzle_world.y-10]

    render_surface.blit(rotated_image, rotated_rect)

def draw_bullet_hole(render_surface: pygame.Surface, bullet_hole_position: list | tuple, bullet_hole_lifetime: float):
    global current_bullet_hole_image

    progress = (bullet_hole_lifetime / vfx.BULLET_HOLE_DURATION)**2
    alpha = max(0, 255 - int(progress * 255))

    if current_bullet_hole_image is None:
        current_bullet_hole_image = pygame.transform.scale_by(assets.ASSETS["bullet_hole"], .4)

    current_bullet_hole_image.set_alpha(alpha)

    render_surface.blit(current_bullet_hole_image, bullet_hole_position)

def draw_bullet(render_surface: pygame.Surface, bullet_position: list | tuple, bullet_name: str):
    global current_bullet_image

    if current_bullet_image is None:
        current_bullet_image = assets.ASSETS[bullet_name]

    render_surface.blit(current_bullet_image, bullet_position)
    draw_bullet_bloom_effect(render_surface, bullet_position, 8, (219, 115, 64, 50))
