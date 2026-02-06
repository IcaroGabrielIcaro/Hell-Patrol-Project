import pygame
import os

SPRITE_PATH = "client/assets/sprites/enimies"


class Enemy:
    _base_sprites = None

    @classmethod
    def load_base_sprites(cls):
        if cls._base_sprites is not None:
            return

        cls._base_sprites = []
        for i in range(1, 8):
            img = pygame.image.load(
                os.path.join(SPRITE_PATH, f"Demon Basic-{i}.png")
            ).convert_alpha()
            cls._base_sprites.append(img)

    def __init__(self, enemy_id, x, y, size, anim_speed=0.10):
        Enemy.load_base_sprites()

        self.id = enemy_id
        self.size = size

        # ===== posição REAL (float) =====
        self.pos = pygame.Vector2(x, y)

        # ===== rect só pra render / colisão =====
        self.rect = pygame.Rect(0, 0, size, size)
        self.rect.topleft = self.pos

        # ===== ajustes de hitbox =====
        self.hitbox_scale = 0.5
        self.hitbox_offset_y = -size * 0.35

        # ===== sprites =====
        sprite_scale = int(size * 2)
        self.sprites = [
            pygame.transform.smoothscale(sprite, (sprite_scale, sprite_scale))
            for sprite in Enemy._base_sprites
        ]

        # ===== animação =====
        self.frame = 0
        self.anim_timer = 0.0
        self.anim_speed = anim_speed

        # ===== movimento =====
        self.last_pos = self.pos.copy()

    # =========================================================
    # Atualização de posição (servidor)
    # =========================================================
    def update_position(self, x, y):
        self.pos.update(x, y)
        self.rect.topleft = self.pos  # conversão só aqui

    # =========================================================
    # Hitbox REAL
    # =========================================================
    def get_hitbox(self):
        w = int(self.size * self.hitbox_scale)
        h = int(self.size * self.hitbox_scale)

        x = self.rect.centerx - w // 2
        y = self.rect.centery - h // 2 + self.hitbox_offset_y

        return pygame.Rect(x, y, w, h)

    # =========================================================
    # Atualização local (animação)
    # =========================================================
    def update(self, dt):
        delta = self.pos - self.last_pos
        moving = delta.length_squared() > 0.0001

        if moving:
            self.anim_timer += dt
            if self.anim_timer >= self.anim_speed:
                self.anim_timer -= self.anim_speed
                self.frame = (self.frame + 1) % len(self.sprites)
        else:
            self.frame = 0
            self.anim_timer = 0.0

        self.last_pos.update(self.pos)

    # =========================================================
    # Render
    # =========================================================
    def draw(self, screen, camera, debug=False):
        sprite = self.sprites[self.frame]

        screen.blit(
            sprite,
            (
                self.rect.centerx - sprite.get_width() // 2 - camera.x,
                self.rect.centery - sprite.get_height() // 2 - camera.y
            )
        )

        if debug:
            hitbox = self.get_hitbox()

            pygame.draw.rect(
                screen,
                (255, 0, 0),
                pygame.Rect(
                    hitbox.x - camera.x,
                    hitbox.y - camera.y,
                    hitbox.width,
                    hitbox.height
                ),
                2
            )

            pygame.draw.circle(
                screen,
                (0, 255, 0),
                (
                    hitbox.centerx - camera.x,
                    hitbox.centery - camera.y
                ),
                3
            )
