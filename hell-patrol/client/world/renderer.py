import pygame
from shared.world import TILE_SIZE, WORLD_TILES_Y

def draw_tilemap(screen, camera, tiles, tile_map, row_offset, big_tiles, gates):
    left   = camera.x
    top    = camera.y
    right  = camera.x + camera.screen_width
    bottom = camera.y + camera.screen_height

    start_y = max(0, top // TILE_SIZE)
    end_y   = min(WORLD_TILES_Y - 1, (bottom - 1) // TILE_SIZE)

    # 🟫 BASE DO CHÃO
    for y in range(start_y, end_y + 1):
        is_offset = row_offset[y]
        offset_x = -TILE_SIZE // 2 if is_offset else 0

        row = tile_map[y]

        for x in range(len(row)):
            world_x = x * TILE_SIZE + offset_x
            world_y = y * TILE_SIZE

            screen.blit(
                tiles[row[x]],
                (world_x - camera.x, world_y - camera.y)
            )

    # 🟥 BIG TILES
    for bt in big_tiles:
        screen.blit(
            bt["img"],
            (bt["x"] - camera.x, bt["y"] - camera.y)
        )

    # 🚪 GATES E DETALHES
    for g in gates:
        screen.blit(
            g["img"],
            (g["x"] - camera.x, g["y"] - camera.y)
        )
