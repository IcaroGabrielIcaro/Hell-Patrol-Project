import pygame
import math
import os
from client.core.input import get_movement
from shared.protocol import make_move, make_shoot, make_reload

class Game:
    def __init__(self, screen, network, scene):
        self.screen = screen
        self.network = network
        self.scene = scene

        # config de tiro
        self.shoot_cooldown = 0.35
        self.shoot_timer = 0

        self.max_ammo = 10
        self.ammo = self.max_ammo
        self.reloading = False

        # carrega mira
        self.crosshair_img = None
        self.crosshair_empty = None

        try:
            self.crosshair_img = pygame.image.load(
                "client/assets/sprites/mira/crosshairSquare.png"
            ).convert_alpha()
            self.crosshair_img = pygame.transform.scale_by(self.crosshair_img, 2.3)

            self.crosshair_empty = pygame.image.load(
                "client/assets/sprites/mira/crosshairSquare-empty.png"
            ).convert_alpha()
            self.crosshair_empty = pygame.transform.scale_by(self.crosshair_empty, 2.3)
        except:
            pass

    def run(self, clock):
        running = True

        while running:
            dt = clock.tick(60) / 1000
            self.shoot_timer -= dt

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            dx, dy = get_movement()
            moving = dx != 0 or dy != 0

            # rotação pelo mouse
            mx, my = pygame.mouse.get_pos()
            player = self.scene.players.get(self.network.player_id)

            if player:
                screen_pos = self.scene.camera.apply(player.rect).center
                diff_x = mx - screen_pos[0]
                diff_y = my - screen_pos[1]
                angle = math.degrees(math.atan2(-diff_y, diff_x))
            else:
                angle = 0

            mouse_buttons = pygame.mouse.get_pressed()
            keys = pygame.key.get_pressed()

            # verifica ações
            shoot = False
            reload = False

            # atirar (botão esquerdo)
            if mouse_buttons[0] and not self.reloading:
                if self.ammo > 0 and self.shoot_timer <= 0:
                    shoot = True
                    self.shoot_timer = self.shoot_cooldown
                    self.ammo -= 1

            # recarregar (tecla R)
            if keys[pygame.K_r] and self.ammo < self.max_ammo and not self.reloading:
                reload = True
                self.reloading = True

            # envia movimento com ações
            msg = make_move(dx, dy, angle)
            if shoot:
                msg["shoot"] = True
            if reload:
                msg["reload"] = True

            self.network.send(msg)

            # recebe estado do servidor
            state = self.network.receive()
            self.scene.update_state(state)

            # verifica se terminou de recarregar
            if self.network.player_id in state.get("reloaded_players", []):
                self.ammo = self.max_ammo
                self.reloading = False

            self.scene.update_animations(dt, moving)

            # desenha tudo
            self.screen.fill((30, 30, 30))
            self.scene.draw(self.screen)

            # desenha mira
            if self.crosshair_img:
                mx, my = pygame.mouse.get_pos()
                img = self.crosshair_empty if (self.crosshair_empty and self.ammo == 0) else self.crosshair_img
                rect = img.get_rect(center=(mx, my))
                self.screen.blit(img, rect)

            pygame.display.flip()

        self.network.close()

