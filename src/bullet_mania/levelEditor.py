import math
import random

import pygame

pygame.init()
pygame.mixer.init()

from bullet_mania.config.gameConfig import *

from bullet_mania.assetsManager import load_asset

from bullet_mania.uiManager import render_ui, draw_reload_text, draw_reloading_text
from bullet_mania.gunSystem import draw_bullet_hole, shoot, start_reload, reload, draw_bullet, place_bullet_hole
from bullet_mania.tilesManager import load_tiles, load_tiles_assets, draw_tile

import bullet_mania.data.assets as assets

WIDTH, HEIGHT = WINDOW_SIZE

CURRENT_LAYER = 0
TILES: list[list] = []

CAMERA_POSITION = [0.0, 0.0]
CAMERA_VELOCITY = [0.0, 0.0]
CAMERA_SENS = 0.05

running = False

TextFont = pygame.font.Font("src/bullet_mania/assets/fonts/GNF.ttf", 25)
NumberFont = pygame.font.Font("src/bullet_mania/assets/fonts/GNF.ttf", 35)

def draw_editor_ui(screen: pygame.Surface):
    global CURRENT_LAYER

    current_layer_text = TextFont.render(f"Current Layer: {CURRENT_LAYER}", True, (255, 255, 255))

    screen.blit(current_layer_text, (20, 20))

def run_editor():
    global running

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Bullet Mania Level Editor")

    render_surface = pygame.Surface(RENDER_SIZE).convert_alpha()

    clock = pygame.time.Clock()

    running = True

    while running:
        delta_time = clock.get_time()

        input()
        update(delta_time)
        render(render_surface, screen)

        clock.tick(FPS)

        pygame.display.flip()

def input():
    global running, CAMERA_POSITION, CAMERA_VELOCITY, CAMERA_SENS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LSHIFT]:
            CAMERA_SENS = 0.1
        else:
            CAMERA_SENS = 0.05

        CAMERA_VELOCITY = [0.0, 0.0]

        if keys[pygame.K_a]:
            CAMERA_VELOCITY[0] -= 1
        if keys[pygame.K_d]:
            CAMERA_VELOCITY[0] += 1
        if keys[pygame.K_w]:
            CAMERA_VELOCITY[1] -= 1
        if keys[pygame.K_s]:
            CAMERA_VELOCITY[1] += 1

def update(delta_time: float):
    CAMERA_POSITION[0] += CAMERA_VELOCITY[0] * CAMERA_SENS * delta_time
    CAMERA_POSITION[1] += CAMERA_VELOCITY[1] * CAMERA_SENS * delta_time

def render(render_surface: pygame.Surface, screen: pygame.Surface):
    render_surface.fill(BG_COLOR)

    pygame.draw.rect(render_surface, (255, 0, 255), (0 - CAMERA_POSITION[0], 0 - CAMERA_POSITION[1], 16, 16))

    screen.blit(pygame.transform.scale(render_surface, (WIDTH, HEIGHT)), (0, 0))

    draw_editor_ui(screen)