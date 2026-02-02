import pygame
import math
from client.core.input import get_movement
from shared.protocol import make_move, make_shoot, make_reload


class Game:
    def __init__(self, screen, network, scene, crosshair_img):
        self.screen = screen
        self.network = network
        self.scene = scene
        self.crosshair_img = crosshair_img

        # 🔫 CONFIG TIRO
        self.shoot_cooldown = 0.35
        self.shoot_timer = 0

        self.max_ammo = 10
        self.ammo = self.max_ammo
        self.reloading = False

        self.crosshair_empty = pygame.image.load(
            "client/assets/sprites/mira/crosshairSquare-empty.png"
        ).convert_alpha()

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

            # ---------------- ROTACAO PELO MOUSE ----------------
            mx, my = pygame.mouse.get_pos()
            player = self.scene.players.get(self.network.player_id)

            if player:
                screen_pos = self.scene.camera.apply(player.rect).center
                diff_x = mx - screen_pos[0]
                diff_y = my - screen_pos[1]
                angle = math.degrees(math.atan2(-diff_y, diff_x))
            else:
                angle = 0
            # ----------------------------------------------------

            mouse_buttons = pygame.mouse.get_pressed()

            shot_this_frame = False

            # 🔫 ATIRAR (botão direito)
            if mouse_buttons[2] and not self.reloading:
                if self.ammo > 0 and self.shoot_timer <= 0:
                    self.network.send(make_shoot(angle))
                    self.shoot_timer = self.shoot_cooldown
                    self.ammo -= 1
                    shot_this_frame = True

            # 🔄 RECARREGAR (botão esquerdo)
            if mouse_buttons[0] and self.ammo == 0 and not self.reloading:
                self.network.send(make_reload())
                self.reloading = True

            # 🚶 MOVE SEMPRE (depois do shoot)
            self.network.send(make_move(dx, dy, angle))

            # ---------------- NETWORK ----------------
            state = self.network.receive()
            self.scene.update_state(state)

            if self.network.player_id in state.get("reloaded_players", []):
                self.ammo = self.max_ammo
                self.reloading = False

            self.scene.update_animations(dt, moving)

            # ---------------- DESENHO ----------------
            self.screen.fill((30, 30, 30))
            self.scene.draw(self.screen)

            mx, my = pygame.mouse.get_pos()
            img = self.crosshair_empty if self.ammo == 0 else self.crosshair_img
            rect = img.get_rect(center=(mx, my))
            self.screen.blit(img, rect)

            pygame.display.flip()

        self.network.close()
