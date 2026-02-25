import os
import pygame

from bullet_mania.config.gameConfig import *

import bullet_mania.data.tiles as tiles
import bullet_mania.data.vfx as vfx

RENDER_WIDTH, RENDER_HEIGHT = RENDER_SIZE

def load_tiles_assets(assets_dir="./assets/tiles/"):
    base_path = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_path, assets_dir)

    for filename in os.listdir(full_path):
        if filename.endswith(".png"):
            tile_id = filename.split(".")[0]
            tile_surface = pygame.transform.scale(pygame.image.load(os.path.join(full_path, filename)), (16, 16))
            tiles.TILES_ASSETS[tile_id] = tile_surface

def load_tiles(tiles_data, tiles_list):
    for layer in tiles_data:
        tiles_list.append([])

        for tile in layer:
            x, y, width, height, id = tile

            image = tiles.TILES_ASSETS.get(str(id))

            tiles_list[-1].append((x, y, width, height, image))

def draw_tile(render_surface: pygame.Surface, tile: list, camera_x: float, camera_y: float, alpha: int = 255):
    tile_pos = tile[0], tile[1]
    tile_size = (tile[2], tile[3])
    tile_image = tile[4]

    tile_rendering_pos = (
        tile_pos[0] - camera_x + RENDER_WIDTH / 2 + vfx.CAM_SHAKE_OFFSET[0] - vfx.CAM_OFFSET[0],
        tile_pos[1] - camera_y + RENDER_HEIGHT / 2 + vfx.CAM_SHAKE_OFFSET[1] - vfx.CAM_OFFSET[1]
    )

    tile_image.set_alpha(alpha)

    render_surface.blit(tile_image, tile_rendering_pos)
