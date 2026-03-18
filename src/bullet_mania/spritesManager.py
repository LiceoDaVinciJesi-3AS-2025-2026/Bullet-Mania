# spritesManager.py - Load spritesheet given frames data.

# License: See LICENSE file in the project root for details.

# Authors: 
# Lorenzo Morresi <lorenzomorresi11@gmail.com>
# Lucio M. Tagliabracci <lucio.tagliabracci@gmail.com>

import pygame

import bullet_mania.data.assets as assets

def load_spritesheet(anim_id, sheet, frame_width, frame_height, row, num_frames):
    frames = []

    for i in range(num_frames):
        rect = pygame.Rect(i * frame_width, row * frame_height, frame_width, frame_height)
        frames.append(sheet.subsurface(rect))

    assets.SPRITES_ANIMATIONS[anim_id] = frames

    return frames
