import pygame

import bullet_mania.data.assets as assets

def load_spritesheet(anim_id, sheet, frame_width, frame_height, row, num_frames):
    frames = []

    for i in range(num_frames):
        rect = pygame.Rect(i * frame_width, row * frame_height, frame_width, frame_height)
        frames.append(sheet.subsurface(rect))

    assets.SPRITE_SHEETS[anim_id] = frames

    return frames
