import math
import random

import pygame

pygame.init()
pygame.mixer.init()

from bullet_mania.config.gameConfig import *

from bullet_mania.assetsManager import load_asset

from bullet_mania.ui import render_ui
from bullet_mania.gunSystem import draw_bullet_hole, shoot, start_reload, reload, draw_bullet, place_bullet_hole
from bullet_mania.tilesManager import load_tiles, load_tiles_assets

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

def run():
    global running, FIRST_LAYER_ENABLED, BULLET_IMAGE

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Bullet Mania - FPS: 0.00")

    pygame.mixer.set_num_channels(32)

    pygame.mixer.music.load("src/bullet_mania/assets/sounds/music/adrenaline-rush.mp3")
    pygame.mixer.music.set_volume(0.25)
    pygame.mixer.music.play(loops=-1)

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
         ]
    ]

    load_tiles_assets()
    load_tiles(tiles_data_test, world.TILES)

    if len(world.TILES) > 1:
        FIRST_LAYER_ENABLED = True

    load_asset("bullet", "src/bullet_mania/assets/bullet.png", (8, 8))
    load_asset("cursor", "src/bullet_mania/assets/ui/cursor.png", (11, 11))
    load_asset("heart", "src/bullet_mania/assets/ui/heart.png", (16, 16))
    load_asset("bullet_hole", "src/bullet_mania/assets/vfx/bulletHole.png", (12, 12))

    while running:
        delta_time = clock.get_time()

        input()
        update(delta_time)
        render(render_surface, screen)

        clock.tick(FPS)

        pygame.display.flip()
        pygame.display.set_caption(f"Bullet Mania - FPS: {clock.get_fps():.2f}")
        pygame.mouse.set_visible(False)

scale = pygame.Vector2(
    WINDOW_SIZE[0] / RENDER_SIZE[0],
    WINDOW_SIZE[1] / RENDER_SIZE[1]
)

def input():
    global running

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # left click
                mouse_screen = pygame.mouse.get_pos()

                camera_x = player.POSITION[0] - RENDER_WIDTH / 2
                camera_y = player.POSITION[1] - RENDER_HEIGHT / 2

                mouse_render = (
                    mouse_screen[0] / scale[0],
                    mouse_screen[1] / scale[1]
                )

                mouse_world = (
                    mouse_render[0] + camera_x,
                    mouse_render[1] + camera_y
                )

                shoot(player.POSITION, mouse_world)

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

    player.POSITION[0] = player.POSITION[0] + (velocity[0] * CHARACTER_SPEED * speed_multiplier * delta_time)
    player.POSITION[1] = player.POSITION[1] + (velocity[1] * CHARACTER_SPEED * speed_multiplier * delta_time)

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
    for bullet in world.BULLETS:
        should_destroy = False

        if FIRST_LAYER_ENABLED:
            for tile in world.TILES[1]:
                tile_rect = pygame.Rect(tile[0], tile[1], tile[2], tile[3])
                bullet_rect = pygame.Rect(bullet[0][0], bullet[0][1], 4, 4)

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
    global FIRST_LAYER_ENABLED, BULLET_IMAGE

    render_surface.fill(BG_COLOR)

    camera_x = player.POSITION[0] + PLAYER_WIDTH / 2
    camera_y = player.POSITION[1] + PLAYER_HEIGHT / 2

    for tile in world.TILES[0]:
        tile_pos = tile[0], tile[1]
        tile_size = (tile[2], tile[3])
        tile_image = tile[4]

        tile_rendering_pos = (
            tile_pos[0] - camera_x + RENDER_WIDTH / 2 + vfx.CAM_SHAKE_OFFSET[0],
            tile_pos[1] - camera_y + RENDER_HEIGHT / 2 + vfx.CAM_SHAKE_OFFSET[1]
        )

        render_surface.blit(tile_image, tile_rendering_pos)

        # pygame.draw.rect(render_surface, tile_color, (tile_rendering_pos[0], tile_rendering_pos[1], tile_size[0], tile_size[1]))
    
    tiles_over_player: list[list] = []

    if FIRST_LAYER_ENABLED:
        for tile in world.TILES[1]:
            tile_pos = tile[0], tile[1]

            if tile_pos[1] + tile[3] > player.POSITION[1] + PLAYER_HEIGHT and tile_pos[0] > player.POSITION[0] + PLAYER_WIDTH and tile_pos[0] + tile[3] < player.POSITION[0]:
                tiles_over_player.append(tile)
                continue

            tile_size = (tile[2], tile[3])
            tile_image = tile[4]

            tile_rendering_pos = (
                tile_pos[0] - camera_x + RENDER_WIDTH / 2 + vfx.CAM_SHAKE_OFFSET[0],
                tile_pos[1] - camera_y + RENDER_HEIGHT / 2 + vfx.CAM_SHAKE_OFFSET[1]
            )

            pygame.draw.rect(
                render_surface,
                (0, 255, 255),
                (
                    tile[0], tile[1],
                    16, 16
                )
            )

            render_surface.blit(tile_image, tile_rendering_pos)

    pygame.draw.rect(
        render_surface,
        CHARACTER_COLOR,
        (
            RENDER_WIDTH / 2 - PLAYER_WIDTH / 2 + vfx.CAM_SHAKE_OFFSET[0],
            RENDER_HEIGHT / 2 - PLAYER_HEIGHT / 2 + vfx.CAM_SHAKE_OFFSET[1],
            PLAYER_WIDTH,
            PLAYER_HEIGHT
        )
    )

    pygame.draw.rect(
        render_surface,
        (0, 0, 255),
        (
            player.POSITION[0],
            player.POSITION[1],
            PLAYER_WIDTH,
            PLAYER_HEIGHT
        )
    )

    pygame.draw.rect(
        render_surface,
        (255, 0, 0),
        (
            player.POSITION[0] + (PLAYER_WIDTH - PLAYER_HITBOX_WIDTH) // 2,
            player.POSITION[1] + PLAYER_HEIGHT - PLAYER_HITBOX_HEIGHT,
            PLAYER_HITBOX_WIDTH,
            PLAYER_HITBOX_HEIGHT
        )
    )

    for tile in tiles_over_player:
            tile_pos = tile[0], tile[1]
            tile_size = (tile[2], tile[3])
            tile_image = tile[4]

            tile_rendering_pos = (
                tile_pos[0] - camera_x + RENDER_WIDTH / 2 + vfx.CAM_SHAKE_OFFSET[0],
                tile_pos[1] - camera_y + RENDER_HEIGHT / 2 + vfx.CAM_SHAKE_OFFSET[1]
            )

            pygame.draw.rect(
                render_surface,
                (0, 255, 255),
                (
                    tile[0], tile[1],
                    16, 16
                )
            )

            render_surface.blit(tile_image, tile_rendering_pos)

    camera_x = player.POSITION[0] - RENDER_WIDTH / 2
    camera_y = player.POSITION[1] - RENDER_HEIGHT / 2

    for bullet in world.BULLETS:
        position = bullet[0]

        bullet_rendering_position = (
            position[0] - camera_x + vfx.CAM_SHAKE_OFFSET[0],
            position[1] - camera_y + vfx.CAM_SHAKE_OFFSET[1]
        )

        draw_bullet(render_surface, bullet_rendering_position, "bullet")

    
    for bullet_hole in vfx.BULLET_HOLES:
        bullet_hole_rendering_position = (
            bullet_hole[0][0] - camera_x + vfx.CAM_SHAKE_OFFSET[0],
            bullet_hole[0][1] - camera_y + vfx.CAM_SHAKE_OFFSET[1]
        )

        draw_bullet_hole(render_surface, bullet_hole_rendering_position, bullet_hole[1])

    # Draw cursor

    screen.blit(pygame.transform.scale(render_surface, WINDOW_SIZE), (0, 0))

    render_ui(screen)

    mouse_pos = pygame.mouse.get_pos()
    screen.blit(pygame.transform.scale_by(assets.ASSETS["cursor"], scale), (mouse_pos[0] - 7, mouse_pos[1] - 7))
