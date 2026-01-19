# carrega e gerencia os assets
import pygame
from shared.world import TILE_SIZE


class TileLoader:
    TILE_DEFINITION = {
        "hellTile1.png": 38,
        "hellTile1-2.png": 1,
        "hellTile1-3.png": 1,
        "hellTile2.png": 35,
        "hellTile2-1.png": 2,
        "hellTile3.png": 22,
        "hellTile3-1.png": 1,
    }

    @staticmethod
    def load_tiles():
        tiles = {}
        tile_ids = []
        weights = []

        for idx, (filename, weight) in enumerate(TileLoader.TILE_DEFINITION.items()):
            img = pygame.image.load(
                f"client/assets/sprites/tiles/{filename}"
            ).convert()

            tiles[idx] = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
            tile_ids.append(idx)
            weights.append(weight)

        return tiles, tile_ids, weights
