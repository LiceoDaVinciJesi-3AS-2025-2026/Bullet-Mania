import pygame

from bullet_mania.config.gameConfig import *

PLAYER_POSITION = [0.0, 0.0]
PLAYER_VELOCITY = [0.0, 0.0]

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
        delta_time = clock.get_time()
    
        input()
        update(delta_time)
        render(screen)

        pygame.display.flip()

        clock.tick(FPS)
        print(f"Running at {clock.get_fps()} fps")

def input():
    global running, PLAYER_VELOCITY

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        
        keys = pygame.key.get_pressed()

        # reset player speed
        PLAYER_VELOCITY = [0, 0]

        # movement on X axis (left/right)
        if keys[pygame.K_a]:
            PLAYER_VELOCITY[0] = -1
        if keys[pygame.K_d]:
            PLAYER_VELOCITY[0] = 1
        
        # movement on Y axis (up/down)
        if keys[pygame.K_w]:
            PLAYER_VELOCITY[1] = -1
        if keys[pygame.K_s]:
            PLAYER_VELOCITY[1] = 1

    print("Gathering input")

def update(delta_time: float):
    global PLAYER_POSITION, PLAYER_VELOCITY

    PLAYER_POSITION[0] = PLAYER_POSITION[0] + (PLAYER_VELOCITY[0] * PLAYER_SPEED * delta_time)
    PLAYER_POSITION[1] = PLAYER_POSITION[1] + (PLAYER_VELOCITY[1] * PLAYER_SPEED * delta_time)

    print(PLAYER_POSITION)

def render(screen: pygame.Surface):
    screen.fill("red")
