import pygame

class Enemy:
    def __init__(self, x, y, size):
        self.rect = pygame.Rect(x, y, size, size)

    def draw(self, screen, camera):
        screen_rect = camera.apply(self.rect)
        pygame.draw.rect(screen, (50, 200, 50), screen_rect)  # verde para diferenciar
