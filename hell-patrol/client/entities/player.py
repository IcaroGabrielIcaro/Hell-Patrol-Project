import pygame

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 40)

    def draw(self, screen):
        pygame.draw.rect(screen, (200, 50, 50), self.rect)
