import pygame
import os

class Projectile:
    def __init__(self, x, y, angle, scale=3.5):
        base = "client/assets/sprites/tiros/quadrado"

        if os.path.exists(base):
            files = sorted(os.listdir(base))
            self.frames = [
                pygame.transform.scale_by(
                    pygame.image.load(os.path.join(base, f)).convert_alpha(),
                    scale
                )
                for f in files
            ]
        else:
            surf = pygame.Surface((10, 10), pygame.SRCALPHA)
            pygame.draw.circle(surf, (255, 255, 0), (5, 5), 5)
            self.frames = [surf]

        self.frame = 0
        self.x = x
        self.y = y
        self.angle = angle

        self.rect = None  # hitbox atual

    def draw(self, screen, camera, debug_hitbox=False):
        img = pygame.transform.rotate(self.frames[self.frame], self.angle + 90)

        self.rect = img.get_rect(
            center=camera.apply_pos((self.x, self.y + 60))
        )

        screen.blit(img, self.rect)

        if debug_hitbox:
            pygame.draw.rect(
                screen,
                (255, 0, 0),   
                self.rect,
                2             
            )
