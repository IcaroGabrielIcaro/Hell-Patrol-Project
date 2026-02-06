import os
import pygame

class Spawn:
    _base_sprites = None  # <- ISSO FALTAVA


    @classmethod
    def load_base_sprites(cls, scale=2.5):
        if cls._base_sprites is not None:
            return

        cls._base_sprites = []
        base_path = "client/assets/sprites/spawnner"

        for i in range(1, 12):
            img = pygame.image.load(
                os.path.join(base_path, f"Pentagram-{i}.png")
            ).convert_alpha()

            w, h = img.get_size()
            img = pygame.transform.smoothscale(
                img,
                (int(w * scale), int(h * scale))
            )

            cls._base_sprites.append(img)

    def __init__(self, spawn_id, x, y):
        Spawn.load_base_sprites()  # garante que carregou

        self.id = spawn_id
        self.x = x
        self.y = y

        self.frames = Spawn._base_sprites
        self.frame_index = 0
        self.frame_timer = 0.0

        self.anim_speed = 0.08

    def update(self, dt):
        self.frame_timer += dt
        if self.frame_timer >= self.anim_speed:
            self.frame_timer = 0.0
            self.frame_index = (self.frame_index + 1) % len(self.frames)

    def draw(self, screen, camera):
        frame = self.frames[self.frame_index]
        rect = frame.get_rect(center=(self.x, self.y))
        rect = camera.apply(rect)
        screen.blit(frame, rect)
