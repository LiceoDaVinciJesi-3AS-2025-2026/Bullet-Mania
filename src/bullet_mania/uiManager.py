import pygame

from bullet_mania.config.gameConfig import WINDOW_SIZE, RENDER_SIZE, CHARACTER_SIZE

import bullet_mania.data.assets as assets
import bullet_mania.data.vfx as vfx
import bullet_mania.data.player as player

WINDOW_WIDTH, WINDOW_HEIGHT = WINDOW_SIZE

PLAYER_WIDTH, PLAYER_HEIGHT = CHARACTER_SIZE

scale = WINDOW_SIZE[0] / RENDER_SIZE[0]

TextFont = pygame.font.Font("src/bullet_mania/assets/fonts/GNF.ttf", 25)
NumberFont = pygame.font.Font("src/bullet_mania/assets/fonts/GNF.ttf", 35)

heart_image = None
bullet_image = None

reloading_progress_bar_image = None
reloading_progress_tick_image = None

time = 0

def draw_lives(screen: pygame.Surface):
    global heart_image

    if heart_image is None:
        heart_image = pygame.transform.scale_by(assets.ASSETS["heart"], scale*.8)

    for i in range(player.LIVES):
        screen.blit(heart_image, (20 + i * 60, 20))

def draw_mag(screen: pygame.Surface):
    global bullet_image

    if bullet_image is None:
        bullet_image = pygame.transform.scale_by(assets.ASSETS["ammo"], scale)
    
    for i in range(player.MAG_AMMO):
        screen.blit(bullet_image, (WINDOW_WIDTH - 45, WINDOW_HEIGHT - 35 - (i * 25)))

def draw_reload_text(screen: pygame.Surface, alpha: int):
    reload_text = TextFont.render("Reload", True, (255, 255, 255))
    reload_text.set_alpha(alpha)

    screen.blit(reload_text, (WINDOW_WIDTH/2 - reload_text.get_width()/2 - vfx.CAM_OFFSET[0]*scale, WINDOW_HEIGHT/2 - PLAYER_HEIGHT/2 - reload_text.get_height()/2 - 60  - vfx.CAM_OFFSET[1]*scale))

def draw_reloading_text(screen: pygame.Surface, progress: float):
    global reloading_progress_bar_image, reloading_progress_tick_image

    if reloading_progress_bar_image is None:
        reloading_progress_bar_image = pygame.transform.scale_by(assets.ASSETS["reloading_progress_bar"], scale)

    if reloading_progress_tick_image is None:
        reloading_progress_tick_image = pygame.transform.scale_by(assets.ASSETS["reloading_progress_tick"], scale)
    
    progress_bar_position_x = WINDOW_WIDTH/2 - reloading_progress_bar_image.get_width()/2 - vfx.CAM_OFFSET[0]*scale
    progress_bar_position_y = WINDOW_HEIGHT/2 - PLAYER_HEIGHT/2 - reloading_progress_bar_image.get_height()/2 - 60 - vfx.CAM_OFFSET[1]*scale

    screen.blit(reloading_progress_bar_image, (progress_bar_position_x, progress_bar_position_y))

    # draw progress ticks
    tick_width = reloading_progress_tick_image.get_width()
    tick_height = reloading_progress_tick_image.get_height()

    progress = progress*32*scale

    screen.blit(reloading_progress_tick_image, (
        progress_bar_position_x + progress - tick_width/2,
        progress_bar_position_y + reloading_progress_bar_image.get_height()/2 - tick_height/2 - 1
    ))

def render_ui(screen: pygame.Surface):
    ammo = NumberFont.render(f"{player.AMMO}/{player.MAX_AMMO}", True, "white")
    screen.blit(ammo, (WINDOW_WIDTH - ammo.get_width() - 75, WINDOW_HEIGHT - ammo.get_height() - 5))
    draw_lives(screen)
    draw_mag(screen)