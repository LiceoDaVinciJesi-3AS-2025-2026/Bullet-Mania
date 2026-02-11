import pygame

from bullet_mania.config.game import *

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
    global running

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    print("Gathering input")

def update():
    print("Updating")

def render():
    print("Rendering")
