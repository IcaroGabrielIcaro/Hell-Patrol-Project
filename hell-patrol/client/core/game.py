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

        mouse_buttons = pygame.mouse.get_pressed()
        keys = pygame.key.get_pressed()

        msg = make_move(dx, dy, angle)
        msg["player_id"] = self.network.player_id  # identifica player no servidor

        if mouse_buttons[0]:
            msg["shoot"] = True

        if keys[pygame.K_r]:
            msg["reload"] = True

        self.network.send(msg)  # envia via UDP

        state = self.network.receive()  # recebe via UDP
        self.scene.update_state(state)

        self.screen.fill((30, 30, 30))
        self.scene.draw(self.screen)

        mx, my = pygame.mouse.get_pos()

        # Protege contra estado sem player_id (pode acontecer em multiplayer)
        if self.network.player_id in state.get("players", {}):
            ammo = state["players"][self.network.player_id]["ammo"]
        else:
            ammo = 0

        img = self.crosshair_empty if ammo == 0 else self.crosshair_img
        rect = img.get_rect(center=(mx, my))
        self.screen.blit(img, rect)

        pygame.display.flip()

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

