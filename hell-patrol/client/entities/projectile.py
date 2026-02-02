# client/entities/projectile.py
import pygame
import os

class Projectile:
    def __init__(self, x, y, angle, scale=1.3):
        base = "client/assets/sprites/tiros/quadrado"
        files = sorted(os.listdir(base))

        self.frames = [
            pygame.transform.scale_by(
                pygame.image.load(os.path.join(base, f)).convert_alpha(),
                scale
            )
            for f in files
        ]

        self.frame = 0
        self.x = x
        self.y = y
        self.angle = angle

    def draw(self, screen, camera):
        img = pygame.transform.rotate(self.frames[self.frame], self.angle)
        rect = img.get_rect(center=camera.apply_pos((self.x, self.y)))
        screen.blit(img, rect)
