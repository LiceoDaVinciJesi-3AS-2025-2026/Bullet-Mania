def load_tiles(tiles_data, tiles_list):
    for layer in tiles_data:
        tiles_list.append([])

        for tile in layer:
            x, y, width, height, color = tile
            tiles_list[-1].append((x, y, width, height, color))