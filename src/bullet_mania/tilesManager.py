# tilesManager.py - Handle tiles loading, map loading and tiles rendering.

# License: See LICENSE file in the project root for details.

# Authors: 
# Lorenzo Morresi <lorenzomorresi11@gmail.com>
# Lucio M. Tagliabracci <lucio.tagliabracci@gmail.com>

import os

import pygame

from bullet_mania.config.gameConfig import *

import bullet_mania.data.tiles as tiles

RENDER_WIDTH, RENDER_HEIGHT = RENDER_SIZE

TILES_BUFFER: list[tuple] = []

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

def draw_tile(tile: list, tile_rendering_pos: tuple, alpha: int = 255):
    tile_image = tile[4]

    tile_image.set_alpha(alpha)

    TILES_BUFFER.append((tile_image, tile_rendering_pos))

def draw_tiles_buffer(render_surface: pygame.Surface):
    global TILES_BUFFER

    render_surface.blits(blit_sequence=TILES_BUFFER)
    TILES_BUFFER = []
