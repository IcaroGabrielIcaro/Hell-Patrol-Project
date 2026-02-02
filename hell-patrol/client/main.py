import pygame
from client.config import *
from client.core.network import NetworkClient
from client.core.game import Game
from client.core.display import Display
from client.assets.loader import TileLoader
from client.scenes.gameplay import GameplayScene

# inicializa pygame
pygame.init()

# inicia a tela
screen, screen_width, screen_height = Display.init_fullscreen()
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()

# conecta com o servidor
network = NetworkClient(SERVER_HOST, SERVER_PORT)

# carrega os assets
tiles, tile_ids, weights = TileLoader.load_tiles()

# inicia o jogo
scene = GameplayScene(screen_width, screen_height, tiles, tile_ids, weights, network.player_id)
game = Game(screen, network, scene)

# loop principal
game.run(clock)

pygame.quit()

