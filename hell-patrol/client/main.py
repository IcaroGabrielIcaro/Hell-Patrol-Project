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
tile_image = pygame.image.load(
    "client/assets/sprites/tiles/hellTile1.png"
).convert()

tile_image = pygame.transform.scale(
    tile_image,
    (TILE_SIZE, TILE_SIZE)
)

scene = GameplayScene(screen_width, screen_height, tile_image)
game = Game(screen, network, scene)

game.run(clock)

pygame.quit()
