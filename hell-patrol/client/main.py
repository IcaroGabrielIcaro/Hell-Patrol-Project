import pygame
from client.config import *
from client.core.network import NetworkClient
from client.core.game import Game
from client.scenes.gameplay import GameplayScene
from shared.world import TILE_SIZE

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.mouse.set_visible(False)

SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
clock = pygame.time.Clock()

network = NetworkClient(SERVER_HOST, SERVER_PORT)
screen_width, screen_height = screen.get_size()

TILE_DEFINITION = {
    "hellTile1.png":   38,
    "hellTile1-2.png": 1,
    "hellTile1-3.png": 1,

    "hellTile2.png":   35,
    "hellTile2-1.png": 2,

    "hellTile3.png":   22,
    "hellTile3-1.png": 1,
}

tiles = {}
tile_ids = []
weights = []

for idx, (filename, weight) in enumerate(TILE_DEFINITION.items()):
    img = pygame.image.load(
        f"client/assets/sprites/tiles/{filename}"
    ).convert()

    tiles[idx] = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    tile_ids.append(idx)
    weights.append(weight)

crosshair_img = pygame.image.load(
    "client/assets/sprites/mira/crosshairSquare.png"
).convert_alpha()

CROSSHAIR_SCALE = 2.3  # 🔥 ajuste o tamanho aqui

if CROSSHAIR_SCALE != 1:
    crosshair_img = pygame.transform.scale_by(crosshair_img, CROSSHAIR_SCALE)

scene = GameplayScene(screen_width, screen_height, tiles, tile_ids, weights, network.player_id)
game = Game(screen, network, scene, crosshair_img)

game.run(clock)

pygame.quit()
