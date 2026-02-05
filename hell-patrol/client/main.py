import pygame
from client.core.application import GameApplication

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.mouse.set_visible(False)

app = GameApplication(screen)
app.run()
