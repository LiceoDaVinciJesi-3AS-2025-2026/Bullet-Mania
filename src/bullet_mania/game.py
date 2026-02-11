import pygame

from bullet_mania.config.gameConfig import *

PLAYER_POSITION = [0, 0]
PLAYER_SPEED = [0, 0]

PLAYER_SIDE = 1
PLAYER_MOUSE_POSITION = [0, 0]

running = False

def run():
    global running

    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Bullet Mania")

    clock = pygame.time.Clock()

    running = True

    while running:
        input()
        update()
        render()
        clock.tick(FPS)
        print(f"Running at {clock.get_fps()}fps")

def input():
    global running, PLAYER_SPEED

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            # reset player speed
            PLAYER_SPEED = [0, 0]

            # movement on X axis (left/right)
            if event.key == pygame.K_a:
                PLAYER_SPEED[0] = -1
            if event.key == pygame.K_d:
                PLAYER_SPEED[0] = 1
            
            # movement on Y axis (up/down)
            if event.key == pygame.K_w:
                PLAYER_SPEED[1] = -1
            if event.key == pygame.K_s:
                PLAYER_SPEED[1] = 1

    print("Gathering input")

def update():
    global PLAYER_POSITION, PLAYER_SPEED

    PLAYER_POSITION[0] += PLAYER_SPEED[0]
    PLAYER_POSITION[1] += PLAYER_SPEED[1]

    print(PLAYER_POSITION)

def render():
    print("Rendering")
