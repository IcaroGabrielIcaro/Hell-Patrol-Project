import pygame
from shared.world import (
    TILE_SIZE,
    WORLD_TILES_X,
    WORLD_TILES_Y
)
import random

class TileMap:
    def __init__(self, tiles):
        self.tiles = tiles

        # IDs dos tiles
        self.tile_ids = list(self.tiles.keys())

        # Pesos (porcentagem relativa)
        # Quanto maior, mais comum
        self.weights = [
            50,  # hellTile1 (mais comum)
            2,  # hellTile2
            1,  # hellTile1-2
            47    # hellTile1.3 (raríssimo)
        ]

        self.map = [
            [
                random.choices(self.tile_ids, weights=self.weights, k=1)[0]
                for _ in range(WORLD_TILES_X)
            ]
            for _ in range(WORLD_TILES_Y)
        ]

    def draw(self, screen, camera):
        left   = camera.x
        top    = camera.y
        right  = camera.x + camera.screen_width
        bottom = camera.y + camera.screen_height

        start_x = max(0, left // TILE_SIZE)
        start_y = max(0, top // TILE_SIZE)
        end_x   = min(WORLD_TILES_X - 1, (right  - 1) // TILE_SIZE)
        end_y   = min(WORLD_TILES_Y - 1, (bottom - 1) // TILE_SIZE)

        for y in range(start_y, end_y + 1):
            for x in range(start_x, end_x + 1):
                tile = self.tiles[self.map[y][x]]
                screen.blit(
                    tile,
                    (x * TILE_SIZE - camera.x,
                     y * TILE_SIZE - camera.y)
                )
