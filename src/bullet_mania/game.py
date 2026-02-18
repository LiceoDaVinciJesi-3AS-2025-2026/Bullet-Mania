import pygame
pygame.init()

from bullet_mania.config.gameConfig import *

from bullet_mania.ui import render_ui
from bullet_mania.gunSystem import shoot, reload

import bullet_mania.data.player as player
import bullet_mania.data.world as world

WIDTH, HEIGHT = WINDOW_SIZE
RENDER_WIDTH, RENDER_HEIGHT = RENDER_SIZE

PLAYER_WIDTH, PLAYER_HEIGHT = CHARACTER_SIZE

player.POSITION = [(RENDER_WIDTH / 2 - PLAYER_WIDTH / 2), (RENDER_HEIGHT / 2 - PLAYER_HEIGHT / 2)]

running = False

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
                shoot((player.POSITION[0] + PLAYER_WIDTH / 2, player.POSITION[1] + PLAYER_HEIGHT / 2), pygame.mouse.get_pos())

        keys = pygame.key.get_pressed()

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

def update(delta_time: float):
    player.POSITION[0] = round(player.POSITION[0] + (player.VELOCITY[0] * CHARACTER_SPEED * delta_time), 4)
    player.POSITION[1] = round(player.POSITION[1] + (player.VELOCITY[1] * CHARACTER_SPEED * delta_time), 4)

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

def render(render_surface: pygame.Surface, screen: pygame.Surface):
    render_surface.fill(BG_COLOR)

    pygame.draw.rect(render_surface, CHARACTER_COLOR, (player.POSITION[0], player.POSITION[1], PLAYER_WIDTH, PLAYER_HEIGHT))

    for bullet in world.BULLETS:
        position = bullet[0]

        pygame.draw.circle(render_surface, BULLET_COLOR, (position[0], position[1]), 2)

    screen.blit(pygame.transform.scale(render_surface, WINDOW_SIZE), (0, 0))

    render_ui(screen)
