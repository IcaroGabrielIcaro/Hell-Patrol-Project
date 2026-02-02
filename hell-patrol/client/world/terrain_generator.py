import random
from shared.world import WORLD_TILES_X, WORLD_TILES_Y

def generate_base_map(tile_ids, weights):
    tile_map = []
    row_offset = []

    for y in range(WORLD_TILES_Y):
        is_offset = random.random() < 0.22
        row_offset.append(is_offset)

        row_size = WORLD_TILES_X + (1 if is_offset else 0)

        row = [
            random.choices(tile_ids, weights=weights, k=1)[0]
            for _ in range(row_size)
        ]

        tile_map.append(row)

    return tile_map, row_offset
