import pygame
from client.config import *
from client.core.network import NetworkClient
from client.core.game import Game
from client.scenes.gameplay import GameplayScene
from client.assets.loader import TileLoader

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.mouse.set_visible(False)

SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
clock = pygame.time.Clock()

network = NetworkClient(SERVER_HOST, SERVER_PORT)
screen_width, screen_height = screen.get_size()

tiles, tile_ids, weights = TileLoader.load_tiles()

scene = GameplayScene(screen_width, screen_height, tiles, tile_ids, weights, network.player_id)
game = Game(screen, network, scene)

game.run(clock)

pygame.quit()
