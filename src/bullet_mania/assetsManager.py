import pygame

import bullet_mania.data.assets as assets

def load_asset(asset_name: str, asset_path: str, size: tuple[int, int] | list | None = None) -> pygame.Surface:
    asset = pygame.image.load(asset_path).convert_alpha()

    if size is not None:
        asset = pygame.transform.scale(asset, size)

    assets.ASSETS[asset_name] = asset
    return asset
