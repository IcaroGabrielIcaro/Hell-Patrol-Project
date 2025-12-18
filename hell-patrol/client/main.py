import pygame
from client.config import *
from client.core.network import NetworkClient
from client.core.game import Game
from client.scenes.gameplay import GameplayScene

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

network = NetworkClient(SERVER_HOST, SERVER_PORT)
scene = GameplayScene()
game = Game(screen, network, scene)

game.run(clock)

pygame.quit()
