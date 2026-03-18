from importlib.resources import files
from zipfile import Path

# eventualmente aggiungere tutte le funzioni relative alle cartelle che avete creato in src.
def get_sound(filename: str) -> Path:
    return files(__package__) / "assets" / "sounds" / filename

def get_font(filename: str) -> Path:
    return files(__package__) / "assets" / "fonts" / filename

def get_gun(filename: str) -> Path:
    return files(__package__) / "assets" / "guns" / filename

def get_sprite(filename: str) -> Path:
    return files(__package__) / "assets" / "sprites" / filename

def get_tile(filename: str) -> Path:
    return files(__package__) / "assets" / "tiles" / filename

def get_ui(filename: str) -> Path:
    return files(__package__) / "assets" / "ui" / filename

def get_vfx(filename: str) -> Path:
    return files(__package__) / "assets" / "vfx" / filename
