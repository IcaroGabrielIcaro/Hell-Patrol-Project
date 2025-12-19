import pygame
from client.entities.player import Player
from client.core.camera import Camera
from client.world.tilemap import TileMap

class GameplayScene:
    def __init__(self, screen_width, screen_height, tile_image, player_id):
        self.players = {}
        self.camera = Camera(screen_width, screen_height)
        self.local_player_id = player_id
        self.tilemap = TileMap(tile_image)

    def update_state(self, state):
        self.players = {
            pid: Player(p["x"], p["y"], p["size"])
            for pid, p in state["players"].items()
        }

    def draw(self, screen):
        if not self.players:
            return

        main_player = self.players.get(self.local_player_id)
        if not main_player:
            return

        self.camera.update(main_player.rect)

        # 1️⃣ Desenha o chão
        self.tilemap.draw(screen, self.camera)

        # 2️⃣ Desenha os jogadores
        for player in self.players.values():
            player.draw(screen, self.camera)

