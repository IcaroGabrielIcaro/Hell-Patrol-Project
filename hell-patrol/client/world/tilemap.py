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
        # Área visível em coordenadas do mundo
        left   = camera.x
        top    = camera.y
        right  = camera.x + camera.screen_width
        bottom = camera.y + camera.screen_height

        # Converte pixels → índices de tile
        start_x = left // TILE_SIZE
        start_y = top // TILE_SIZE
        end_x   = (right  - 1) // TILE_SIZE
        end_y   = (bottom - 1) // TILE_SIZE

        # Clamp para os limites do mundo lógico
        start_x = max(0, start_x)
        start_y = max(0, start_y)
        end_x   = min(WORLD_TILES_X - 1, end_x)
        end_y   = min(WORLD_TILES_Y - 1, end_y)

        # Desenha apenas tiles válidos
        for y in range(start_y, end_y + 1):
            for x in range(start_x, end_x + 1):
                world_x = x * TILE_SIZE
                world_y = y * TILE_SIZE

                screen_x = world_x - camera.x
                screen_y = world_y - camera.y

                screen.blit(self.tile, (screen_x, screen_y))
