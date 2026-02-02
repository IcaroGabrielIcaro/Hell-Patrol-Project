import pygame
import random
from shared.world import TILE_SIZE, WORLD_WIDTH, WORLD_HEIGHT

BIG_TILE_SIZE = TILE_SIZE * 2

def generate_big_tiles():
    BIG_TILE_FILES = ["hellTileBig1.png", "hellTileBig2.png"]

    big_images = []
    for name in BIG_TILE_FILES:
        img = pygame.image.load(
            f"client/assets/sprites/tiles/{name}"
        ).convert_alpha()
        img = pygame.transform.scale(img, (BIG_TILE_SIZE, BIG_TILE_SIZE))
        big_images.append(img)

    big_tiles = []
    MAX_BIG_TILES = 8
    SPAWN_CHANCE = 0.06

    attempts = 0
    while len(big_tiles) < MAX_BIG_TILES and attempts < 300:
        attempts += 1

        if random.random() > SPAWN_CHANCE:
            continue

        x = (random.randint(0, WORLD_WIDTH - BIG_TILE_SIZE) // TILE_SIZE) * TILE_SIZE
        y = (random.randint(0, WORLD_HEIGHT - BIG_TILE_SIZE) // TILE_SIZE) * TILE_SIZE

        new_rect = pygame.Rect(x, y, BIG_TILE_SIZE, BIG_TILE_SIZE)

        if any(new_rect.colliderect(pygame.Rect(bt["x"], bt["y"], BIG_TILE_SIZE, BIG_TILE_SIZE)) for bt in big_tiles):
            continue

        big_tiles.append({
            "x": x,
            "y": y,
            "img": random.choice(big_images)
        })

    return big_tiles
