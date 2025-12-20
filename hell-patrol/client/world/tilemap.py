import pygame
import random
from shared.world import (
    TILE_SIZE,
    WORLD_TILES_X,
    WORLD_TILES_Y,
    WORLD_HEIGHT,
    WORLD_WIDTH
)

BIG_TILE_SIZE = TILE_SIZE * 2

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

        self.big_tiles = []
        self.generate_big_tiles()

    def generate_big_tiles(self):
        BIG_TILE_FILES = [
            "hellTileBig1.png",
            "hellTileBig2.png"
        ]

        big_images = []
        for name in BIG_TILE_FILES:
            img = pygame.image.load(
                f"client/assets/sprites/tiles/{name}"
            ).convert_alpha()
            img = pygame.transform.scale(img, (BIG_TILE_SIZE, BIG_TILE_SIZE))
            big_images.append(img)

        MAX_BIG_TILES = 8
        SPAWN_CHANCE = 0.06

        BIG_GRID_X = 48
        BIG_GRID_Y = 96

        attempts = 0
        while len(self.big_tiles) < MAX_BIG_TILES and attempts < 300:
            attempts += 1

            if random.random() > SPAWN_CHANCE:
                continue

            # 🔹 SNAP DIFERENTE PARA CADA EIXO
            x = (random.randint(0, WORLD_WIDTH - BIG_TILE_SIZE) // BIG_GRID_X) * BIG_GRID_X
            y = (random.randint(0, WORLD_HEIGHT - BIG_TILE_SIZE) // BIG_GRID_Y) * BIG_GRID_Y

            new_rect = pygame.Rect(x, y, BIG_TILE_SIZE, BIG_TILE_SIZE)

            # 🔹 Verifica sobreposição
            overlap = False
            for bt in self.big_tiles:
                existing_rect = pygame.Rect(
                    bt["x"], bt["y"],
                    BIG_TILE_SIZE, BIG_TILE_SIZE
                )
                if new_rect.colliderect(existing_rect):
                    overlap = True
                    break

            if overlap:
                continue

            self.big_tiles.append({
                "x": x,
                "y": y,
                "img": random.choice(big_images)
            })



    def draw(self, screen, camera):
        left   = camera.x
        top    = camera.y
        right  = camera.x + camera.screen_width
        bottom = camera.y + camera.screen_height

        start_y = max(0, top // TILE_SIZE)
        end_y   = min(WORLD_TILES_Y - 1, (bottom - 1) // TILE_SIZE)

        # 🟫 Base
        for y in range(start_y, end_y + 1):
            is_offset = self.row_offset[y]
            offset_x = -TILE_SIZE // 2 if is_offset else 0

            row = self.map[y]

            for x in range(len(row)):
                world_x = x * TILE_SIZE + offset_x
                world_y = y * TILE_SIZE

                screen.blit(
                    self.tiles[row[x]],
                    (world_x - camera.x, world_y - camera.y)
                )

        # 🟥 Big tiles (overlay)
        for bt in self.big_tiles:
            screen.blit(
                bt["img"],
                (bt["x"] - camera.x, bt["y"] - camera.y)
            )
