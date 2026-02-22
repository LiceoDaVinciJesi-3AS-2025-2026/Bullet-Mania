import math

import pygame
pygame.init()

from bullet_mania.config.gameConfig import *

from bullet_mania.ui import render_ui
from bullet_mania.gunSystem import shoot, reload

import bullet_mania.data.player as player
import bullet_mania.data.world as world
import bullet_mania.data.vfx as vfx

WIDTH, HEIGHT = WINDOW_SIZE
RENDER_WIDTH, RENDER_HEIGHT = RENDER_SIZE

PLAYER_WIDTH, PLAYER_HEIGHT = CHARACTER_SIZE

player.POSITION = [(RENDER_WIDTH / 2 - PLAYER_WIDTH / 2), (RENDER_HEIGHT / 2 - PLAYER_HEIGHT / 2)]
CAM_SHAKE_OFFSET = [0.0, 0.0]

running = False

RECTS = [[60, 60]]

def run():
    global running

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Bullet Mania - FPS: 0.00")

    render_surface = pygame.Surface(RENDER_SIZE)

    clock = pygame.time.Clock()

    running = True

    while running:
        delta_time = clock.get_time()

        input()
        update(delta_time)
        clock.tick(FPS)
        render(render_surface, screen)

        pygame.display.flip()

        clock.tick(FPS)
        pygame.display.set_caption(f"Bullet Mania - FPS: {clock.get_fps():.2f}")

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
                shoot((RENDER_WIDTH/2, RENDER_HEIGHT/2), pygame.mouse.get_pos())

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
            reload()

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
    global CAM_SHAKE_OFFSET

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

    player.POSITION[0] = round(player.POSITION[0] + (player.VELOCITY[0] * CHARACTER_SPEED * speed_multiplier * delta_time), 4)
    player.POSITION[1] = round(player.POSITION[1] + (player.VELOCITY[1] * CHARACTER_SPEED * speed_multiplier * delta_time), 4)
    
    if player.IS_RELOADING and player.LAST_RELOAD_TIME >= player.RELOAD_COOLDOWN:
        player.IS_RELOADING = False
        player.LAST_RELOAD_TIME = 0
        player.AMMO = 10
        print("reloaded")

    if player.IS_RELOADING:
        player.LAST_RELOAD_TIME += delta_time

    for bullet in world.BULLETS:
        if bullet[3] <= 0:
            world.BULLETS.remove(bullet)
            continue

        direction = bullet[1]
        velocity = bullet[2]

        bullet[0][0] += direction[0] * velocity * delta_time
        bullet[0][1] += direction[1] * velocity * delta_time

        bullet[3] -= delta_time
    
    if vfx.HAS_SHOT:
        vfx.CAM_SHAKE_TIME = vfx.CAM_SHAKE_DURATION
        vfx.HAS_SHOT = False

    if vfx.CAM_SHAKE_TIME > 0:
        vfx.CAM_SHAKE_TIME -= delta_time

        progress = vfx.CAM_SHAKE_TIME / vfx.CAM_SHAKE_DURATION
        decay = progress

        CAM_SHAKE_OFFSET[0] = math.sin(pygame.time.get_ticks() * 0.5) * vfx.CAM_SHAKE_STRENGTH * decay
        CAM_SHAKE_OFFSET[1] = math.cos(pygame.time.get_ticks() * 0.7) * vfx.CAM_SHAKE_STRENGTH * decay

        print(CAM_SHAKE_OFFSET)
        print(vfx.CAM_SHAKE_TIME)
    else:
        CAM_SHAKE_OFFSET = [0.0, 0.0]

def render(render_surface: pygame.Surface, screen: pygame.Surface):
    render_surface.fill(BG_COLOR)

    pygame.draw.rect(render_surface, CHARACTER_COLOR, (RENDER_WIDTH/2 - PLAYER_WIDTH/2 + CAM_SHAKE_OFFSET[0], RENDER_HEIGHT/2 - PLAYER_HEIGHT/2 + CAM_SHAKE_OFFSET[1], PLAYER_WIDTH, PLAYER_HEIGHT))

    for rect in RECTS:
        rect_pos = rect[0], rect[1]
        rect_rendering_pos = rect_pos[0] - player.POSITION[0] + CAM_SHAKE_OFFSET[0], rect_pos[1] - player.POSITION[1] + CAM_SHAKE_OFFSET[1]

        pygame.draw.rect(render_surface, (255, 0, 0), (rect_rendering_pos[0], rect_rendering_pos[1], 20, 20))

    for bullet in world.BULLETS:
        position = bullet[0]

        pygame.draw.circle(render_surface, BULLET_COLOR, (position[0] + CAM_SHAKE_OFFSET[0], position[1] + CAM_SHAKE_OFFSET[1]), 2)

    screen.blit(pygame.transform.scale(render_surface, WINDOW_SIZE), (0, 0))

    render_ui(screen)
