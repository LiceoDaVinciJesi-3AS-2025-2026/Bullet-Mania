import pygame

from bullet_mania.config.gameConfig import RENDER_SIZE, WINDOW_SIZE
import bullet_mania.data.player as player
import bullet_mania.data.world as world

scale = pygame.Vector2(
    RENDER_SIZE[0] / WINDOW_SIZE[0],
    RENDER_SIZE[1] / WINDOW_SIZE[1]
)

def shoot(position, mouse_position, owner_id="local", velocity=0.5, lifetime=2000):
    if player.AMMO > 0 and player.IS_RELOADING == False:
        player.AMMO -= 1

        player_pos = pygame.Vector2(position)
        mouse_pos = pygame.Vector2((mouse_position[0] * scale[0], mouse_position[1] * scale[1]))

        direction = mouse_pos - player_pos

        if direction.length() != 0:
            direction = direction.normalize()

        world.BULLETS.append([ [player_pos[0], player_pos[1]], direction, velocity, lifetime, owner_id ])

def reload():
    if not player.IS_RELOADING:
        player.IS_RELOADING = True