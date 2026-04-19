# aiGunSystem.py - Handle AI-related guns functions.

# License: See LICENSE file in the project root for details.

# Authors: 
# Lorenzo Morresi <lorenzomorresi11@gmail.com>
# Lucio M. Tagliabracci <lucio.tagliabracci@gmail.com>

import pygame
import random

from bullet_mania.config.gameConfig import *

from bullet_mania.resourcesHandler import get_sound

import bullet_mania.data.player as player
import bullet_mania.data.world as world

BOT_WIDTH, BOT_HEIGHT = BOT_CHARACTER_SIZE
BOT_HITBOX_WIDTH, BOT_HITBOX_HEIGHT = BOT_CHARACTER_HITBOX_SIZE

shoot_sound = pygame.mixer.Sound(get_sound("gun_shoot.mp3"))
shoot_sound.set_volume(0.12)

shell_falling_sound = pygame.mixer.Sound(get_sound("gun_shell_falling.mp3"))
shell_falling_sound.set_volume(0.07)

reload_sound = pygame.mixer.Sound(get_sound("gun_reload.mp3"))
reload_sound.set_volume(0.15)

def shoot_to_player(bot, velocity=.2, lifetime=1500):
    bot_center = pygame.Vector2(bot[0])
    bot_center = pygame.Vector2(
        bot_center.x + BOT_WIDTH/2,
        bot_center.y + BOT_HEIGHT/2
    )

    player_center = pygame.Vector2(player.POSITION)
    player_center = pygame.Vector2(
        player_center.x + random.randint(-15, 15),
        player_center.y + random.randint(-15, 15),
    )

    direction = player_center - bot_center

    if direction.length() != 0:
        direction = direction.normalize()

    world.BULLETS.append([
        [bot_center.x, bot_center.y],
        direction,
        velocity,
        lifetime,
        f"_bot"
    ])

    shoot_sound.play()
    shell_falling_sound.play()
