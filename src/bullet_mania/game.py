import math
import random

import pygame

pygame.init()
pygame.mixer.init()

from bullet_mania.config.gameConfig import *

from bullet_mania.assetsManager import load_asset

from bullet_mania.uiManager import *
from bullet_mania.gunSystem import *
from bullet_mania.tilesManager import *
from bullet_mania.vfxManager import *

from bullet_mania.ai.aiTilesHandler import build_ai_tiles_grid
from bullet_mania.ai.aiManager import draw_bots, update_bots, add_bot

import bullet_mania.data.player as player
import bullet_mania.data.world as world
import bullet_mania.data.vfx as vfx
import bullet_mania.data.assets as assets

WIDTH, HEIGHT = WINDOW_SIZE
RENDER_WIDTH, RENDER_HEIGHT = RENDER_SIZE

PLAYER_WIDTH, PLAYER_HEIGHT = CHARACTER_SIZE
PLAYER_HITBOX_WIDTH, PLAYER_HITBOX_HEIGHT = CHARACTER_HITBOX_SIZE

player.POSITION = [0.0, 0.0]

FIRST_LAYER_ENABLED = False

running = False

render_scale = (
    WINDOW_SIZE[0] / RENDER_SIZE[0],
    WINDOW_SIZE[1] / RENDER_SIZE[1]
)

def run():
    global running, FIRST_LAYER_ENABLED

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Bullet Mania - FPS: 0.00")

    pygame.mixer.set_num_channels(32)

    pygame.mixer.music.load("src/bullet_mania/assets/sounds/music/adrenaline_rush.mp3")
    pygame.mixer.music.set_volume(0.25)
    pygame.mixer.music.play(loops=-1)

    pygame.mouse.set_visible(False)

    render_surface = pygame.Surface(RENDER_SIZE).convert_alpha()

    clock = pygame.time.Clock()

    running = True

    tiles_data_test = [
        [
            [0, 16, 16, 16, "floor"], [16, 16, 16, 16, "floor"], [32, 16, 16, 16, "floor"], [48, 16, 16, 16, "floor"], [64, 16, 16, 16, "floor"],
            [0, 32, 16, 16, "floor"], [16, 32, 16, 16, "floor"], [32, 32, 16, 16, "floor"], [48, 32, 16, 16, "floor"], [64, 32, 16, 16, "floor"],
            [0, 48, 16, 16, "floor"], [16, 48, 16, 16, "floor"], [32, 48, 16, 16, "floor"], [48, 48, 16, 16, "floor"], [64, 48, 16, 16, "floor"]
        ],
        [
            [-16, 0, 16, 16, "wall"], [0, 0, 16, 16, "wall"], [16, 0, 16, 16, "wall"], [32, 0, 16, 16, "wall"], [48, 0, 16, 16, "wall"], [64, 0, 16, 16, "wall"], [80, 0, 16, 16, "wall"],
            [-16, 16, 16, 16, "wall"], [80, 16, 16, 16, "wall"],
            [-16, 32, 16, 16, "wall"], [80, 32, 16, 16, "wall"]
        ],
        [
            [-16, -16, 16, 16, "Wall_0"], [0, -16, 16, 16, "top_wall"], [16, -16, 16, 16, "top_wall"], [32, -16, 16, 16, "top_wall"], [48, -16, 16, 16, "top_wall"], [64, -16, 16, 16, "top_wall"], [80, 0, 16, 16, "Wall_2"],
            [-16, 0, 16, 16, "Wall_8"], [80, 0, 16, 16, "Wall_8"],
            [-16, 16, 16, 16, "Wall_8"], [80, 16, 16, 16, "Wall_8"]
        ]
    ]

    load_tiles_assets()
    load_tiles(tiles_data_test, world.TILES)

    build_ai_tiles_grid()

    add_bot([20, 20])

    if len(world.TILES) > 1:
        FIRST_LAYER_ENABLED = True

    load_asset("bullet", "src/bullet_mania/assets/sprites/bullet.png", (8, 8))
    load_asset("cursor", "src/bullet_mania/assets/ui/cursor.png", (11, 11))
    load_asset("heart", "src/bullet_mania/assets/ui/heart.png", (16, 16))
    load_asset("bullet_hole", "src/bullet_mania/assets/vfx/bullet_hole.png", (12, 12))
    load_asset("ammo", "src/bullet_mania/assets/ui/ammo.png", (6, 6))
    load_asset("deagle", "src/bullet_mania/assets/guns/deagle.png", (24, 24))
    load_asset("vignette", "src/bullet_mania/assets/vfx/vignette.png", RENDER_SIZE)

    load_asset("reloading_progress_bar", "src/bullet_mania/assets/ui/reloading_progress_bar.png", (32, 32))
    load_asset("reloading_progress_tick", "src/bullet_mania/assets/ui/reloading_progress_tick.png", (5, 5))

    while running:
        delta_time = clock.get_time()

        input()
        update(delta_time)
        render(render_surface, screen)

        clock.tick(FPS)

        pygame.display.flip()
        pygame.display.set_caption(f"Bullet Mania - FPS: {clock.get_fps():.2f}")

def input():
    global running

    camera_x = player.POSITION[0] - RENDER_WIDTH / 2 + PLAYER_WIDTH / 2
    camera_y = player.POSITION[1] - RENDER_HEIGHT / 2 + PLAYER_HEIGHT / 2

    mouse_screen = pygame.mouse.get_pos()

    mouse_render = (
        mouse_screen[0] / render_scale[0],
        mouse_screen[1] / render_scale[1]
    )

    mouse_world = (
        mouse_render[0] + camera_x,
        mouse_render[1] + camera_y
    )

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # left click
                player_center_screen = (player.POSITION[0] + PLAYER_WIDTH / 2 + PLAYER_WIDTH, player.POSITION[1] + PLAYER_HEIGHT / 2)

                shoot(player_center_screen, mouse_world)

        keys = pygame.key.get_pressed()

        if player.IS_DASHING:
            player.VELOCITY[0] = player.DASH_DIRECTION[0]
            player.VELOCITY[1] = player.DASH_DIRECTION[1]
        else:
            # reset player speed
            player.VELOCITY = [0, 0]

            # movement on X axis (left/right)
            if keys[pygame.K_a]:
                player.VELOCITY[0] = -1
            if keys[pygame.K_d]:
                player.VELOCITY[0] = 1

            # movement on Y axis (up/down)
            if keys[pygame.K_w]:
                player.VELOCITY[1] = -1
            if keys[pygame.K_s]:
                player.VELOCITY[1] = 1

        # reloading
        if keys[pygame.K_r]:
            start_reload()

        # dash
        if keys[pygame.K_LSHIFT]:
            if not player.IS_DASHING and player.DASH_COOLDOWN_TIMER <= 0 and (player.VELOCITY[0] != 0 or player.VELOCITY[1] != 0):
                # preserve the direction
                player.DASH_DIRECTION[0] = player.VELOCITY[0]
                player.DASH_DIRECTION[1] = player.VELOCITY[1]
                player.IS_DASHING = True
                player.DASH_TIME = 0
                player.DASH_COOLDOWN_TIMER = player.DASH_COOLDOWN

def update(delta_time: float):
    global FIRST_LAYER_ENABLED

    # update player position with dashing
    if player.DASH_COOLDOWN_TIMER > 0:
        player.DASH_COOLDOWN_TIMER = max(0, player.DASH_COOLDOWN_TIMER - delta_time)

    if player.IS_DASHING:
        player.DASH_TIME += delta_time
        if player.DASH_TIME >= player.DASH_DURATION:
            player.IS_DASHING = False
            player.DASH_TIME = 0

    if player.IS_DASHING:
        speed_multiplier = player.DASH_MULTIPLIER
    else:
        speed_multiplier = 1

    velocity = pygame.Vector2(player.VELOCITY)
    if velocity.length() > 0:
        velocity = velocity.normalize()

    player.POSITION[0] += velocity[0] * CHARACTER_SPEED * speed_multiplier * delta_time
    player.POSITION[1] += velocity[1] * CHARACTER_SPEED * speed_multiplier * delta_time

    # collision with tiles
    if FIRST_LAYER_ENABLED:
        player_rect = pygame.Rect(
            player.POSITION[0] + (PLAYER_WIDTH - PLAYER_HITBOX_WIDTH) // 2,
            player.POSITION[1] + PLAYER_HEIGHT - PLAYER_HITBOX_HEIGHT,
            PLAYER_HITBOX_WIDTH,
            PLAYER_HITBOX_HEIGHT
        )

        for tile in world.TILES[1]:
            tile_rect = pygame.Rect(tile[0], tile[1], tile[2], tile[3])

            if tile_rect.colliderect(player_rect):
                intersection = tile_rect.clip(player_rect)

                if intersection.width < intersection.height:
                    if player.POSITION[0] < tile_rect.x:
                        player.POSITION[0] -= intersection.width
                    else:
                        player.POSITION[0] += intersection.width
                else:
                    if player.POSITION[1] < tile_rect.y:
                        player.POSITION[1] -= intersection.height
                    else:
                        player.POSITION[1] += intersection.height
    
    # update reloading logic
    if player.IS_RELOADING and player.LAST_RELOAD_TIME >= player.RELOAD_COOLDOWN:
        reload()

    if player.IS_RELOADING:
        player.LAST_RELOAD_TIME += delta_time

    # update bullets
    for bullet in world.BULLETS[:]:
        should_destroy = False

        if FIRST_LAYER_ENABLED:
            bullet_rect = pygame.Rect(bullet[0][0], bullet[0][1], 4, 4)

            for tile in world.TILES[1]:
                tile_rect = pygame.Rect(tile[0], tile[1], tile[2], tile[3])

                if tile_rect.colliderect(bullet_rect):
                    place_bullet_hole((tile[0] + random.randint(4, 12), tile[1] + random.randint(4, 12)))

                    should_destroy = True
                    break

        if bullet[3] <= 0 or should_destroy:
            world.BULLETS.remove(bullet)
            continue

        direction = bullet[1]
        velocity = bullet[2]

        bullet[0][0] += direction[0] * velocity * delta_time
        bullet[0][1] += direction[1] * velocity * delta_time

        bullet[3] -= delta_time
    
    for bullet_hole in vfx.BULLET_HOLES:
        bullet_hole[1] += delta_time
        if bullet_hole[1] >= vfx.BULLET_HOLE_DURATION:
            vfx.BULLET_HOLES.remove(bullet_hole)
    
    update_bots(delta_time)

    mouse_screen = pygame.mouse.get_pos()

    mouse_render = (
        mouse_screen[0] / render_scale[0],
        mouse_screen[1] / render_scale[1]
    )

    center_screen = pygame.Vector2(RENDER_WIDTH / 2, RENDER_HEIGHT / 2)
    mouse_rel_pos = pygame.Vector2(mouse_render[0], mouse_render[1]) - center_screen

    LOOK_AHEAD_FACTOR = 0.15

    target_offset_x = mouse_rel_pos.x * LOOK_AHEAD_FACTOR
    target_offset_y = mouse_rel_pos.y * LOOK_AHEAD_FACTOR

    MAX_OFFSET = 40
    target_offset_x = max(-MAX_OFFSET, min(MAX_OFFSET, target_offset_x))
    target_offset_y = max(-MAX_OFFSET, min(MAX_OFFSET, target_offset_y))

    vfx.CAM_OFFSET[0] += (target_offset_x - vfx.CAM_OFFSET[0]) * 0.1
    vfx.CAM_OFFSET[1] += (target_offset_y - vfx.CAM_OFFSET[1]) * 0.1
    
    # update vfx
    if vfx.HAS_SHOT:
        vfx.CAM_SHAKE_TIME = vfx.CAM_SHAKE_DURATION
        vfx.HAS_SHOT = False

    if vfx.CAM_SHAKE_TIME > 0:
        vfx.CAM_SHAKE_TIME -= delta_time

        progress = vfx.CAM_SHAKE_TIME / vfx.CAM_SHAKE_DURATION
        decay = progress

        vfx.CAM_SHAKE_OFFSET[0] = math.sin(pygame.time.get_ticks() * 0.5) * vfx.CAM_SHAKE_STRENGTH * decay
        vfx.CAM_SHAKE_OFFSET[1] = math.cos(pygame.time.get_ticks() * 0.7) * vfx.CAM_SHAKE_STRENGTH * decay
    else:
        vfx.CAM_SHAKE_OFFSET = [0.0, 0.0]

def render(render_surface: pygame.Surface, screen: pygame.Surface):
    global FIRST_LAYER_ENABLED

    render_surface.fill(BG_COLOR)

    camera_x = player.POSITION[0] + PLAYER_WIDTH / 2
    camera_y = player.POSITION[1] + PLAYER_HEIGHT / 2

    for tile in world.TILES[0]:
        draw_tile(render_surface, tile, camera_x, camera_y)
    
    tiles_over_player: list[list] = []

    if FIRST_LAYER_ENABLED:
        for layer in world.TILES[1:]:
            for tile in layer:
                tile_pos = tile[0], tile[1]

                if tile_pos[1] + tile[3] > player.POSITION[1] + PLAYER_HEIGHT and tile_pos[0] > player.POSITION[0] + PLAYER_WIDTH and tile_pos[0] + tile[3] < player.POSITION[0]:
                    tiles_over_player.append(tile)
                    continue

                draw_tile(render_surface, tile, camera_x, camera_y)

    pygame.draw.rect(
        render_surface,
        CHARACTER_COLOR,
        (
            RENDER_WIDTH / 2 - PLAYER_WIDTH / 2 + vfx.CAM_SHAKE_OFFSET[0] - vfx.CAM_OFFSET[0],
            RENDER_HEIGHT / 2 - PLAYER_HEIGHT / 2 + vfx.CAM_SHAKE_OFFSET[1] - vfx.CAM_OFFSET[1],
            PLAYER_WIDTH,
            PLAYER_HEIGHT
        )
    )

    # draw player gun

    player_center_world = (player.POSITION[0] + PLAYER_WIDTH/2 + vfx.CAM_SHAKE_OFFSET[0] - vfx.CAM_OFFSET[0], player.POSITION[1] + PLAYER_HEIGHT/2 + vfx.CAM_SHAKE_OFFSET[1] - vfx.CAM_OFFSET[1])
    hand_offset = (6, 2)

    gun_pivot_world = (player_center_world[0] + hand_offset[0], player_center_world[1] + hand_offset[1])

    mouse_screen = pygame.mouse.get_pos()

    mouse_render = (
        mouse_screen[0] / render_scale[0],
        mouse_screen[1] / render_scale[1]
    )

    draw_gun(render_surface, "deagle", gun_pivot_world, mouse_render, camera_x, camera_y)

    for tile in tiles_over_player:
        draw_tile(render_surface, tile, camera_x, camera_y)
    
    draw_bots(render_surface, camera_x, camera_y)

    for bullet_hole in vfx.BULLET_HOLES:
        position = bullet_hole[0]

        bullet_hole_rendering_position = (
            position[0] - camera_x + RENDER_WIDTH / 2 + vfx.CAM_SHAKE_OFFSET[0] - vfx.CAM_OFFSET[0],
            position[1] - camera_y + RENDER_HEIGHT / 2 + vfx.CAM_SHAKE_OFFSET[1] - vfx.CAM_OFFSET[1]
        )

        draw_bullet_hole(render_surface, bullet_hole_rendering_position, bullet_hole[1])

    for bullet in world.BULLETS:
        position = bullet[0]

        bullet_rendering_position = (
            position[0] - camera_x + RENDER_WIDTH / 2 + vfx.CAM_SHAKE_OFFSET[0] - vfx.CAM_OFFSET[0],
            position[1] - camera_y + RENDER_HEIGHT / 2 + vfx.CAM_SHAKE_OFFSET[1] - vfx.CAM_OFFSET[1]
        )

        draw_bullet(render_surface, bullet_rendering_position, "bullet")

    draw_vignette_effect(render_surface, 200)

    screen.blit(pygame.transform.scale(render_surface, WINDOW_SIZE), (0, 0))

    render_ui(screen)

    alpha = math.sin(pygame.time.get_ticks() * 0.005) * 127 + 128

    if player.MAG_AMMO == 0 and not player.IS_RELOADING:
        draw_reload_text(screen, int(255 if alpha > 100 else 0))
    elif player.IS_RELOADING:
        progress = player.LAST_RELOAD_TIME / player.RELOAD_COOLDOWN
        draw_reloading_text(screen, progress)

    mouse_pos = pygame.mouse.get_pos()
    screen.blit(pygame.transform.scale_by(assets.ASSETS["cursor"], render_scale), (mouse_pos[0] - 4*render_scale[0], mouse_pos[1] - 4*render_scale[0]))
