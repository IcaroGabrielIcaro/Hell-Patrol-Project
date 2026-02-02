import pygame
import os
from pygame.math import Vector2


class Player:
    def __init__(self, x, y, scale=1.0, anim_speed=0.15):
        self.x = x
        self.y = y
        self.scale = scale
        self.anim_speed = anim_speed
        self.angle = 0

        self.frames_head = []
        self.frames_body = []

        self.load_sprites()

        self.frame_index = 0
        self.anim_timer = 0

        # hitbox baseada no corpo
        w, h = self.frames_body[0].get_size()
        self.rect = pygame.Rect(self.x, self.y, w, h)

        # 🔫 carrega arma UMA VEZ
        gun_path = "client/assets/sprites/arma/shotgun-1.png"
        self.gun_img = pygame.image.load(gun_path).convert_alpha()
        self.gun_img = pygame.transform.scale_by(self.gun_img, self.scale)

        # offsets locais (antes da rotação)
        self.gun_offset = Vector2(18 * self.scale, -4 * self.scale)
        self.head_offset = Vector2(0, -6 * self.scale)

    # -------------------------------------------------
    # Carrega sprites
    # -------------------------------------------------
    def load_sprites(self):
        base_path = "client/assets/sprites/player/centralizado"
        head_path = os.path.join(base_path, "cabeca")
        body_path = os.path.join(base_path, "corpo")

        head_files = sorted(os.listdir(head_path))
        body_files = sorted(os.listdir(body_path))

        for h_file, b_file in zip(head_files, body_files):
            head_img = pygame.image.load(os.path.join(head_path, h_file)).convert_alpha()
            body_img = pygame.image.load(os.path.join(body_path, b_file)).convert_alpha()

            if self.scale != 1.0:
                head_img = pygame.transform.scale_by(head_img, self.scale)
                body_img = pygame.transform.scale_by(body_img, self.scale)

            self.frames_head.append(head_img)
            self.frames_body.append(body_img)

    # -------------------------------------------------
    # Atualiza animação
    # -------------------------------------------------
    def update(self, dt, moving):
        if moving:
            self.anim_timer += dt
            if self.anim_timer >= self.anim_speed:
                self.anim_timer = 0
                self.frame_index = (self.frame_index + 1) % len(self.frames_body)
        else:
            self.frame_index = 0

        self.rect.topleft = (self.x, self.y)

    # -------------------------------------------------
    # Desenho
    # -------------------------------------------------
    def draw(self, screen, camera):
        screen_center = Vector2(camera.apply(self.rect).center)

        body = self.frames_body[self.frame_index]
        head = self.frames_head[self.frame_index]

        # 🔄 rota tudo pelo mesmo ângulo
        angle = self.angle + 90

        rotated_body = pygame.transform.rotate(body, angle)
        rotated_head = pygame.transform.rotate(head, angle)
        rotated_gun = pygame.transform.rotate(self.gun_img, angle)

        # offsets rotacionados
        gun_pos = screen_center + self.gun_offset.rotate(-self.angle)

        body_rect = rotated_body.get_rect(center=screen_center)
        head_rect = rotated_head.get_rect(center=screen_center)
        gun_rect = rotated_gun.get_rect(center=gun_pos)

        # ordem correta
        screen.blit(rotated_body, body_rect)
        screen.blit(rotated_head, head_rect)
        screen.blit(rotated_gun, gun_rect)
