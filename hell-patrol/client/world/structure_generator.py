import pygame
import random
from shared.world import TILE_SIZE, WORLD_WIDTH, WORLD_HEIGHT, WORLD_TILES_X, WORLD_TILES_Y


# -------------------------------------------------
# Carregamento das imagens
# -------------------------------------------------
def load_gate_images():
    GATE_FILES = {
        "S": ("hellGrateS.png", 96, 96),
        "M": ("hellGrateM.png", 192, 96),
        "G": ("hellGrateB.png", 192, 192),
        "V1": ("hellVent1.png", 96, 96),
        "V2": ("hellVent2.png", 96, 96),
    }

    images = {}
    for key, (name, w, h) in GATE_FILES.items():
        img = pygame.image.load(
            f"client/assets/sprites/gates/{name}"
        ).convert_alpha()
        images[key] = pygame.transform.scale(img, (w, h))

    return images


# -------------------------------------------------
# Utilitário de colisão
# -------------------------------------------------
def is_free(x, y, w, h, gates):
    rect = pygame.Rect(x, y, w, h)
    for g in gates:
        r = pygame.Rect(g["x"], g["y"], *g["img"].get_size())
        if rect.colliderect(r):
            return False
    return True


# -------------------------------------------------
# Estruturas grandes
# -------------------------------------------------
def generate_big_blocks(gates, images):
    count = random.randint(3, 6)

    for _ in range(count):
        x = random.randrange(0, WORLD_WIDTH - 192, TILE_SIZE * 2)
        y = random.randrange(0, WORLD_HEIGHT - 192, TILE_SIZE * 2)

        gates.append({
            "x": x,
            "y": y,
            "img": images["G"]
        })


# -------------------------------------------------
# Corredores tipo "cobra"
# -------------------------------------------------
def generate_corridors(gates, images):
    corridor_count = random.randint(15, 18)

    for _ in range(corridor_count):
        x = random.randrange(0, WORLD_WIDTH, TILE_SIZE)
        y = random.randrange(0, WORLD_HEIGHT, TILE_SIZE)

        length = random.randint(6, 14)
        dx, dy = 1, 0
        turns_left = random.randint(2, 4)

        for _ in range(length):
            key = random.choices(["S", "M"], weights=[70, 30], k=1)[0]
            img = images[key]
            w, h = img.get_size()

            if is_free(x, y, w, h, gates):
                gates.append({"x": x, "y": y, "img": img})

            if turns_left > 0 and random.random() < 0.3:
                turns_left -= 1
                dx, dy = random.choice([(0, -1), (0, 1)])
            else:
                dx, dy = 1, 0

            nx = x + dx * TILE_SIZE
            ny = y + dy * TILE_SIZE

            if 0 <= nx <= WORLD_WIDTH - TILE_SIZE:
                x = nx
            if 0 <= ny <= WORLD_HEIGHT - TILE_SIZE:
                y = ny


# -------------------------------------------------
# Centro da arena
# -------------------------------------------------
def generate_center_marker(gates, images):
    center_x = WORLD_TILES_X // 2
    center_y = WORLD_TILES_Y // 2

    inner_tiles = set()
    for y in range(center_y - 1, center_y + 1):
        for x in range(center_x - 1, center_x + 1):
            inner_tiles.add((x, y))

    border_tiles = set()
    for y in range(center_y - 2, center_y + 2):
        for x in range(center_x - 2, center_x + 2):
            if (x, y) not in inner_tiles:
                border_tiles.add((x, y))

    # remove gates dentro do centro
    gates[:] = [
        g for g in gates
        if (g["x"] // TILE_SIZE, g["y"] // TILE_SIZE) not in inner_tiles
    ]

    img = images["S"]
    w, h = img.get_size()

    for (tx, ty) in border_tiles:
        px = tx * TILE_SIZE
        py = ty * TILE_SIZE

        if is_free(px, py, w, h, gates):
            gates.append({"x": px, "y": py, "img": img})


# -------------------------------------------------
# Detalhes decorativos
# -------------------------------------------------
def generate_details(gates, images):
    original_gates = gates.copy()

    for g in original_gates:
        if random.random() < 0.3:
            key = random.choice(["V1", "V2"])
            img = images[key]
            w, h = img.get_size()

            ox = random.choice([-TILE_SIZE, TILE_SIZE])
            oy = random.choice([-TILE_SIZE, TILE_SIZE])

            x = g["x"] + ox
            y = g["y"] + oy

            if 0 <= x <= WORLD_WIDTH - w and 0 <= y <= WORLD_HEIGHT - h:
                if is_free(x, y, w, h, gates):
                    gates.append({"x": x, "y": y, "img": img})


# -------------------------------------------------
# Função principal chamada pelo TileMap
# -------------------------------------------------
def generate_structures():
    gates = []
    images = load_gate_images()

    generate_big_blocks(gates, images)
    generate_corridors(gates, images)
    generate_details(gates, images)
    generate_center_marker(gates, images)

    return gates
