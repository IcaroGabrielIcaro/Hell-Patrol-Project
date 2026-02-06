import pygame
import math
from client.core.input import get_movement
from shared.protocol import make_move


class Game:
    def __init__(self, screen, network, scene):
        self.screen = screen
        self.network = network
        self.scene = scene

        # mira
        self.crosshair_img = pygame.image.load(
            "client/assets/sprites/mira/crosshairSquare.png"
        ).convert_alpha()
        self.crosshair_img = pygame.transform.scale_by(self.crosshair_img, 2.3)

        self.crosshair_empty = pygame.image.load(
            "client/assets/sprites/mira/crosshairSquare-empty.png"
        ).convert_alpha()
        self.crosshair_empty = pygame.transform.scale_by(self.crosshair_empty, 2.3)

    def update_and_draw(self, dt):
        """
        Atualiza e desenha um frame do jogo.
        Retorna True para continuar, False para sair.
        """
        dx, dy = get_movement()

        mx, my = pygame.mouse.get_pos()
        player = self.scene.players.get(self.network.player_id)

        if player:
            screen_pos = self.scene.camera.apply(player.rect).center
            diff_x = mx - screen_pos[0]
            diff_y = my - screen_pos[1]
            angle = math.degrees(math.atan2(-diff_y, diff_x))
        else:
            angle = 0

            # ---------------- Input ----------------
            dx, dy = get_movement()
            mx, my = pygame.mouse.get_pos()

            player = self.scene.players.get(self.network.player_id)

        if mouse_buttons[0]:
            msg["shoot"] = True

        if keys[pygame.K_r]:
            msg["reload"] = True

            # ---------------- Network send ----------------
            msg = make_move(dx, dy, angle)
            msg["player_id"] = self.network.player_id

        state = self.network.receive()  # recebe via UDP
        self.scene.update_state(state)

        self.screen.fill((30, 30, 30))
        self.scene.draw(self.screen)

        mx, my = pygame.mouse.get_pos()

            # ---------------- Network receive ----------------
            state = self.network.receive()
            self.scene.update_state(state)
            self.scene.update_animations(dt)

            # ---------------- Render ----------------
            self.screen.fill((30, 30, 30))
            self.scene.draw(self.screen)

            # ---------------- Crosshair ----------------
            mx, my = pygame.mouse.get_pos()

            players_state = state.get("players", {})
            if self.network.player_id in players_state:
                ammo = players_state[self.network.player_id].get("ammo", 0)
            else:
                ammo = 0

        return True  # Continua rodando

    def run(self, clock):
        """Loop de jogo original (para compatibilidade)."""
        running = True

        while running:
            dt = clock.tick(60) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if not self.update_and_draw(dt):
                running = False

        self.network.close()

