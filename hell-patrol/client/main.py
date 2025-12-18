import pygame
from client.config import *
from client.core.network import NetworkClient
from client.core.game import Game
from client.scenes.gameplay import GameplayScene

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
clock = pygame.time.Clock()

network = NetworkClient(SERVER_HOST, SERVER_PORT)
scene = GameplayScene()
game = Game(screen, network, scene)

game.run(clock)

pygame.quit()
