import pygame
from client.entities.player import Player
from client.core.camera import Camera

class GameplayScene:
    def __init__(self, screen_width, screen_height):
        self.players = {}
        self.camera = Camera(screen_width, screen_height)

    def update_state(self, state):
        self.players = {
            pid: Player(p["x"], p["y"], p["size"])
            for pid, p in state["players"].items()
        }

    def draw(self, screen):
        if not self.players:
            return

        # Usa o primeiro player como alvo da câmera
        main_player = next(iter(self.players.values()))
        self.camera.update(main_player.rect)

        for player in self.players.values():
            player.draw(screen, self.camera)
