# bot structure

# [
#     [0.0, 0.0], # position
#     0, # state
#     2.0, # speed
#     100.0, # hp
#     0.0, # attack cooldown
#     [], # path to follow
#     0.0 # repath timer
# ]

import pygame
import math

from bullet_mania.config.gameConfig import *

import bullet_mania.data.player as player
import bullet_mania.data.vfx as vfx

import bullet_mania.ai.aiTilesHandler as ai_tiles

RENDER_WIDTH, RENDER_HEIGHT = RENDER_SIZE

bots: list[list] = []

IDLE = 0
CHASE = 1
ATTACK = 2

def distance(a, b):
    a = pygame.Vector2(a)
    b = pygame.Vector2(b)

    return a.distance_to(b)

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def reconstruct_path(came_from, current):
    path = [current]

    while current in came_from:
        current = came_from[current]
        path.append(current)

    path.reverse()
    return path

def get_neighbors(node, grid):
    x, y = node
    neighbors = []

    directions = [(1,0), (-1,0), (0,1), (0,-1)]

    for dx, dy in directions:
        nx = x + dx
        ny = y + dy

        if 0 <= nx < MAP_WIDTH and 0 <= ny < MAP_HEIGHT:
            if grid[int(ny)][int(nx)] == 0:
                neighbors.append((nx, ny))

    return neighbors

def astar(grid, start, goal):
    open_list = []
    open_list.append(start)

    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_list:

        current = min(open_list, key=lambda x: f_score.get(x, float("inf")))

        if current == goal:
            return reconstruct_path(came_from, current)

        open_list.remove(current)

        neighbors = get_neighbors(current, grid)

        for neighbor in neighbors:

            tentative_g = g_score[current] + 1

            if tentative_g < g_score.get(neighbor, float("inf")):

                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor, goal)

                if neighbor not in open_list:
                    open_list.append(neighbor)

    return []

def follow_path(bot, delta_time):

    if len(bot[5]) <= 1:
        return

    # prossimo nodo della path
    next_tile = bot[5][1]

    # centro del tile target
    target_x = next_tile[0] * 16 + 16 / 2
    target_y = next_tile[1] * 16 + 16 / 2

    dx = target_x - bot[0][0]
    dy = target_y - bot[0][1]

    distance = math.sqrt(dx * dx + dy * dy)

    if distance > 0:

        direction_x = dx / distance
        direction_y = dy / distance

        move_distance = bot[2] * delta_time

        # Se siamo quasi arrivati, snap e passa al prossimo nodo
        if distance <= move_distance:
            bot[0][0] = target_x
            bot[0][1] = target_y
            bot[5].pop(0)
        else:
            bot[0][0] += direction_x * move_distance
            bot[0][1] += direction_y * move_distance

def move_towards_player(bot, delta_time):
    if not bot[5] or bot[6] <= 0:

        start = (bot[0][0] // 16, bot[0][1] // 16)
        goal = (player.POSITION[0] // 16, player.POSITION[1] // 16)

        bot[5] = astar(ai_tiles.AI_TILES_GRID, start, goal)
        bot[6] = 0.5

    else:
        bot[6] -= delta_time

    follow_path(bot, delta_time)

def state_idle(bot, dist):
    if dist <= 150:
        bot[1] = CHASE

def state_chase(bot, delta_time, dist):
    if dist >= 250:
        bot[1] = IDLE
        return

    elif dist <= 100:
        bot[1] = ATTACK
        return

    move_towards_player(bot, delta_time)

def state_attack(bot, delta_time, dist):
    if dist >= 150:
        bot[1] = CHASE

    print(f"Gli sto sparando al culoz!! (DT: {delta_time})")

def add_bot(position, speed=0.08, hp=100.0):
    bot = [
        position, # position
        0, # state
        speed, # speed
        hp, # hp
        0.0, # attack cooldown
        [], # path to follow
        0.0 # repath timer
    ]

    bots.append(bot)

def update_bots(delta_time):
    for bot in bots[:]:
        dist = distance(bot[0], player.POSITION)

        if bot[1] == IDLE:
            state_idle(bot, dist)

        elif bot[1] == CHASE:
            state_chase(bot, delta_time, dist)

        elif bot[1] == ATTACK:
            state_attack(bot, delta_time, dist)

def draw_bots(render_surface: pygame.Surface, camera_x: float, camera_y: float):
    for index, bot in enumerate(bots):
        bot_pos = bot[0]

        print(f"Distanza: {distance(bot_pos, player.POSITION)}")

        bot_rendering_pos = (
            bot_pos[0] - camera_x + RENDER_WIDTH / 2 + vfx.CAM_SHAKE_OFFSET[0] - vfx.CAM_OFFSET[0],
            bot_pos[1] - camera_y + RENDER_HEIGHT / 2 + vfx.CAM_SHAKE_OFFSET[1] - vfx.CAM_OFFSET[1]
        )

        pygame.draw.rect(render_surface, (255, 0, 0), (bot_rendering_pos[0], bot_rendering_pos[1], 20, 20))
        # render_surface.blit(tile_image, tile_rendering_pos)
