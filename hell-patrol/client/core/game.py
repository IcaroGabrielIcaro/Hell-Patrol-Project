import pygame
from client.core.input import get_movement
from shared.protocol import make_move
import math

class Game:
    def __init__(self, screen, network, scene, crosshair_img):
        self.screen = screen
        self.network = network
        self.scene = scene
        self.crosshair_img = crosshair_img

    def run(self, clock):
        running = True

        while running:
            dt = clock.tick(60) / 1000  # ⬅️ tempo entre frames

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            dx, dy = get_movement()
            moving = dx != 0 or dy != 0  # ⬅️ usado só pra animação

            # ---------------- ROTACAO PELO MOUSE ----------------
            mx, my = pygame.mouse.get_pos()

            player = self.scene.players.get(self.network.player_id)

            if player:
                # posição do player na TELA (considerando câmera)
                screen_pos = self.scene.camera.apply(player.rect).center

                diff_x = mx - screen_pos[0]
                diff_y = my - screen_pos[1]

                angle = math.degrees(math.atan2(-diff_y, diff_x))
            else:
                angle = 0
            # ----------------------------------------------------

            self.network.send(make_move(dx, dy, angle))

            state = self.network.receive()
            self.scene.update_state(state)

            # 🔹 Atualiza animações locais (não dependem do servidor)
            self.scene.update_animations(dt, moving)

            self.screen.fill((30, 30, 30))
            self.scene.draw(self.screen)

            # 🎯 DESENHA A MIRA
            mx, my = pygame.mouse.get_pos()
            rect = self.crosshair_img.get_rect(center=(mx, my))
            self.screen.blit(self.crosshair_img, rect)


            pygame.display.flip()

        self.network.close()
