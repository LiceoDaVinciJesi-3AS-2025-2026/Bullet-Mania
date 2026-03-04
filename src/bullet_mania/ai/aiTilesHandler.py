import bullet_mania.config.gameConfig as config
import bullet_mania.data.world as world

AI_TILES_GRID: list = []

def build_ai_tiles_grid():
    global AI_TILES_GRID

    grid = [[0 for _ in range(config.MAP_WIDTH)] for _ in range(config.MAP_HEIGHT)]
    
    for tile in world.TILES[1]:
        x, y, w, h, img = tile

        grid_y = y // 16
        grid_x = x // 16
        
        grid[grid_y][grid_x] = 1
    
    AI_TILES_GRID = grid
