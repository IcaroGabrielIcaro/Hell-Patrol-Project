import pygame
from client.entities.player import Player

class GameplayScene:
    def __init__(self):
        self.players = {}

    def update_state(self, state):
        self.players = {
            pid: Player(p["x"], p["y"], p["size"])
            for pid, p in state["players"].items()
        }

    def draw(self, screen):
        for player in self.players.values():
            player.draw(screen)
