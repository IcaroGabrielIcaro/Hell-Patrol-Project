import pygame

class Enemy:
    def __init__(self, x, y, size):
        self.size = size
        self.rect = pygame.Rect(x, y, size, size)

    def draw(self, screen, camera):
        pygame.draw.rect(
            screen,
            (200, 200, 50),  # vermelho (placeholder)
            pygame.Rect(
                self.rect.x - camera.x,
                self.rect.y - camera.y,
                self.rect.width,
                self.rect.height
            )
        )
