import pygame

from bullet_mania.config.gameConfig import WINDOW_SIZE, RENDER_SIZE

from bullet_mania.data import assets

import bullet_mania.data.player as player

WINDOW_WIDTH, WINDOW_HEIGHT = WINDOW_SIZE

scale = WINDOW_SIZE[0] / RENDER_SIZE[0]

TextFont = pygame.font.Font("src/bullet_mania/assets/fonts/Dedicool.ttf", 35)
NumberFont = pygame.font.Font("src/bullet_mania/assets/fonts/GNF.ttf", 35)

heart_image = None
bullet_image = None

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
    
def render_ui(screen: pygame.Surface):
    ammo = NumberFont.render(f"{player.AMMO}/{player.MAX_AMMO}", True, "white")
    screen.blit(ammo, (WINDOW_WIDTH - ammo.get_width() - 75, WINDOW_HEIGHT - ammo.get_height() - 5))
    draw_lives(screen)
    draw_mag(screen)