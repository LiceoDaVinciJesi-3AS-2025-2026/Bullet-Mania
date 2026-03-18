# tilesManager.py - Handle waves number and checking.

# License: See LICENSE file in the project root for details.

# Authors: 
# Lorenzo Morresi <lorenzomorresi11@gmail.com>
# Lucio M. Tagliabracci <lucio.tagliabracci@gmail.com>

import random

from bullet_mania.config.gameConfig import *

import bullet_mania.data.world as world

import bullet_mania.statsManager as statsManager

import bullet_mania.ai.aiManager as aiManager

base_enemy_number = 5
base_enemy_health = 100

def spawn_wave():
    enemy_number = base_enemy_number + world.CURRENT_HORDE * 2
    enemy_health = base_enemy_health + world.CURRENT_HORDE * 10

    for _ in range(enemy_number):
        x = random.randint(0, MAP_WIDTH*16)
        y = random.randint(0, MAP_HEIGHT*16)
        aiManager.add_bot([x, y], hp=enemy_health)

    world.CURRENT_HORDE += 1

def check_wave_end():
    if len(aiManager.bots) == 0:
        statsManager.next_horde()
        spawn_wave()