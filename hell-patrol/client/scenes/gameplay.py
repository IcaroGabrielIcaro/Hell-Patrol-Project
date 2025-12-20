import pygame
from client.entities.player import Player
from client.entities.enemy import Enemy
from client.core.camera import Camera
from client.world.tilemap import TileMap

class GameplayScene:
    def __init__(self, screen_width, screen_height, tiles, tiles_ids, weights, player_id):
        self.players = {}
        self.enemies = {}
        self.camera = Camera(screen_width, screen_height)
        self.local_player_id = player_id
        self.tilemap = TileMap(tiles, tiles_ids, weights)

    def update_state(self, state):
        self.players = {
            pid: Player(p["x"], p["y"], p["size"])
            for pid, p in state["players"].items()
        }

        self.enemies = {
            i: Enemy(e["x"], e["y"], e["size"])
            for i, e in enumerate(state.get("enemies", []))
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

        for enemy in self.enemies.values():
            enemy.draw(screen, self.camera)

        # 2️⃣ Desenha os jogadores
        for player in self.players.values():
            player.draw(screen, self.camera)

