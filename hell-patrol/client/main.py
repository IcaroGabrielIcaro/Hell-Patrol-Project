import pygame
from client.config import *
from client.core.network import NetworkClient
from client.core.game import Game
from client.scenes.gameplay import GameplayScene
from client.world.tilemap import TileMap
from shared.world import TILE_SIZE

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
clock = pygame.time.Clock()

network = NetworkClient(SERVER_HOST, SERVER_PORT)
screen_width, screen_height = screen.get_size()

tile_files = [
    "hellTile1.png",
    "hellTile1-2.png",
    "hellTile1.3.png",
    "hellTile2.png",
]

tiles = {}

for i, name in enumerate(tile_files):
    img = pygame.image.load(
        f"client/assets/sprites/tiles/{name}"
    ).convert()
    tiles[i] = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))

scene = GameplayScene(screen_width, screen_height, tiles, network.player_id)
game = Game(screen, network, scene)

game.run(clock)

pygame.quit()
