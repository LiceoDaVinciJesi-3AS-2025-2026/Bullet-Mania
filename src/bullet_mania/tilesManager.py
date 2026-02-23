import os
import pygame

import bullet_mania.data.tiles as tiles

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