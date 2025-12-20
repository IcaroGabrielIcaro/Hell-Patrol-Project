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

        self.gates = []
        self.generate_gates()

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

        BIG_GRID = TILE_SIZE

        attempts = 0
        while len(self.big_tiles) < MAX_BIG_TILES and attempts < 300:
            attempts += 1

            if random.random() > SPAWN_CHANCE:
                continue

            # 🔹 SNAP DIFERENTE PARA CADA EIXO
            x = (random.randint(0, WORLD_WIDTH - BIG_TILE_SIZE) // BIG_GRID) * BIG_GRID
            y = (random.randint(0, WORLD_HEIGHT - BIG_TILE_SIZE) // BIG_GRID) * BIG_GRID

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

    def generate_gates(self):
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

        self.gates = []

        self.generate_big_blocks(images)
        self.generate_corridors(images)
        self.generate_details(images)
        self.generate_center_marker(images)

    def is_free(self, x, y, w, h):
        rect = pygame.Rect(x, y, w, h)
        for g in self.gates:
            r = pygame.Rect(g["x"], g["y"], *g["img"].get_size())
            if rect.colliderect(r):
                return False
        return True
    
    def generate_corridors(self, images):
        corridor_count = random.randint(15, 18)

        for _ in range(corridor_count):
            # 🔹 ponto inicial
            x = random.randrange(0, WORLD_WIDTH, TILE_SIZE)
            y = random.randrange(0, WORLD_HEIGHT, TILE_SIZE)

            length = random.randint(6, 14)

            # 🔹 direção inicial (começa indo pra direita)
            dx, dy = 1, 0

            turns_left = random.randint(2, 4)  # limite de curvas

            for _ in range(length):
                # 🔹 escolhe tipo do gate
                key = random.choices(
                    ["S", "M"],
                    weights=[70, 30],
                    k=1
                )[0]

                img = images[key]
                w, h = img.get_size()

                if self.is_free(x, y, w, h):
                    self.gates.append({
                        "x": x,
                        "y": y,
                        "img": img
                    })

                # 🔹 chance de virar (cobra)
                if turns_left > 0 and random.random() < 0.3:
                    turns_left -= 1

                    # vira pra cima ou pra baixo
                    dx, dy = random.choice([
                        (0, -1),
                        (0, 1)
                    ])
                else:
                    # continua indo pra direita
                    dx, dy = 1, 0

                # 🔹 avança
                nx = x + dx * TILE_SIZE
                ny = y + dy * TILE_SIZE

                # 🔹 clamp de mundo
                if 0 <= nx <= WORLD_WIDTH - TILE_SIZE:
                    x = nx
                if 0 <= ny <= WORLD_HEIGHT - TILE_SIZE:
                    y = ny

    def generate_big_blocks(self, images):
        count = random.randint(3, 6)

        for _ in range(count):
            x = random.randrange(0, WORLD_WIDTH - 192, TILE_SIZE * 2)
            y = random.randrange(0, WORLD_HEIGHT - 192, TILE_SIZE * 2)

            img = images["G"]
            self.gates.append({
                "x": x,
                "y": y,
                "img": img
            })

    def generate_center_marker(self, images):
        """
        Zona central 4x4:
        - interior SEM gates
        - borda obrigatoriamente hellGateS
        """

        center_x = WORLD_TILES_X // 2
        center_y = WORLD_TILES_Y // 2

        # 🔹 área interna 4x4
        inner_tiles = set()
        for y in range(center_y - 1, center_y + 1):
            for x in range(center_x - 1, center_x + 1):
                inner_tiles.add((x, y))

        # 🔹 área da borda (anel externo)
        border_tiles = set()
        for y in range(center_y - 2, center_y + 2):
            for x in range(center_x - 2, center_x + 2):
                if (x, y) not in inner_tiles:
                    border_tiles.add((x, y))

        # 🔹 remove qualquer gate que invada o centro
        cleaned_gates = []
        for g in self.gates:
            gx = g["x"] // TILE_SIZE
            gy = g["y"] // TILE_SIZE
            if (gx, gy) not in inner_tiles:
                cleaned_gates.append(g)
        self.gates = cleaned_gates

        # 🔹 força hellGateS na borda
        img = images["S"]
        w, h = img.get_size()

        for (tx, ty) in border_tiles:
            px = tx * TILE_SIZE
            py = ty * TILE_SIZE

            # evita duplicar
            if not self.is_free(px, py, w, h):
                continue

            self.gates.append({
                "x": px,
                "y": py,
                "img": img
            })

    def generate_details(self, images):
        for g in self.gates:
            if random.random() < 0.3:
                key = random.choice(["V1", "V2"])
                img = images[key]
                w, h = img.get_size()

                ox = random.choice([-TILE_SIZE, TILE_SIZE])
                oy = random.choice([-TILE_SIZE, TILE_SIZE])

                x = g["x"] + ox
                y = g["y"] + oy

                if 0 <= x <= WORLD_WIDTH - w and 0 <= y <= WORLD_HEIGHT - h:
                    if self.is_free(x, y, w, h):
                        self.gates.append({
                            "x": x,
                            "y": y,
                            "img": img
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

        # 🚪 Gates & Vents (overlay final)
        for g in self.gates:
            screen.blit(
                g["img"],
                (g["x"] - camera.x, g["y"] - camera.y)
            )