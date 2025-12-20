import pygame
import random
from shared.world import (
    TILE_SIZE,
    WORLD_TILES_X,
    WORLD_TILES_Y
)

class TileMap:
    def __init__(self, tiles, tile_ids, weights):
        self.tiles = tiles
        self.tile_ids = tile_ids
        self.weights = weights

        self.map = []
        self.row_offset = []

        for y in range(WORLD_TILES_Y):
            is_offset = random.random() < 0.22
            self.row_offset.append(is_offset)

            row_size = WORLD_TILES_X + (1 if is_offset else 0)

            row = [
                random.choices(
                    population=self.tile_ids,
                    weights=self.weights,
                    k=1
                )[0]
                for _ in range(row_size)
            ]

            self.map.append(row)

    def draw(self, screen, camera):
        left   = camera.x
        top    = camera.y
        right  = camera.x + camera.screen_width
        bottom = camera.y + camera.screen_height

        start_y = max(0, top // TILE_SIZE)
        end_y   = min(WORLD_TILES_Y - 1, (bottom - 1) // TILE_SIZE)

        for y in range(start_y, end_y + 1):

            is_offset = self.row_offset[y]
            offset_x = -TILE_SIZE // 2 if is_offset else 0

            row = self.map[y]

            for x in range(len(row)):
                world_x = x * TILE_SIZE + offset_x
                world_y = y * TILE_SIZE

                screen_x = world_x - camera.x
                screen_y = world_y - camera.y

                screen.blit(
                    self.tiles[row[x]],
                    (screen_x, screen_y)
                )
