import pygame
from shared.world import (
    TILE_SIZE,
    WORLD_TILES_X,
    WORLD_TILES_Y
)

class TileMap:
    def __init__(self, tile_image):
        self.tile = tile_image

    def draw(self, screen, camera):
        # Descobre quais tiles estão visíveis pela câmera
        start_x = camera.x // TILE_SIZE
        start_y = camera.y // TILE_SIZE

        end_x = (camera.x + camera.screen_width) // TILE_SIZE + 1
        end_y = (camera.y + camera.screen_height) // TILE_SIZE + 1

        # Clamp para não desenhar fora do mundo
        start_x = max(0, start_x)
        start_y = max(0, start_y)
        end_x = min(WORLD_TILES_X, end_x)
        end_y = min(WORLD_TILES_Y, end_y)

        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                world_x = x * TILE_SIZE
                world_y = y * TILE_SIZE

                screen_x = world_x - camera.x
                screen_y = world_y - camera.y

                screen.blit(self.tile, (screen_x, screen_y))
