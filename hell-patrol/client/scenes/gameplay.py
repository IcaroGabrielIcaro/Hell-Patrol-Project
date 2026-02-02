import pygame
from client.entities.player import Player
from client.entities.enemy import Enemy
from client.entities.projectile import Projectile
from client.core.camera import Camera
from client.world.tilemap import TileMap


class GameplayScene:
    def __init__(self, screen_width, screen_height, tiles, tiles_ids, weights, player_id):
        self.players = {}
        self.enemies = {}
        self.projectiles = []
        self.camera = Camera(screen_width, screen_height)
        self.local_player_id = player_id
        self.tilemap = TileMap(tiles, tiles_ids, weights)

    # -------------------------------------------------
    # Atualização de estado vinda do servidor
    # -------------------------------------------------
    def update_state(self, state):
        server_players = state["players"]

        # 🔹 Atualiza ou cria players
        for pid, p in server_players.items():
            if pid not in self.players:
                # Player novo
                if pid == self.local_player_id:
                    # Player local com animação configurável
                    self.players[pid] = Player(
                        p["x"], p["y"],
                        scale=2.7,
                        anim_speed=0.12
                    )
                else:
                    # Outros players (mesma classe, mas poderia ser simplificado depois)
                    self.players[pid] = Player(p["x"], p["y"], scale=2.7)

            else:
                player = self.players[pid]
                player.x = p["x"]
                player.y = p["y"]
                player.angle = p.get("angle", 0)
                player.rect.topleft = (player.x, player.y)

        # 🔹 Remove players que saíram
        for pid in list(self.players.keys()):
            if pid not in server_players:
                del self.players[pid]

        # 🔹 Atualiza inimigos (eles não têm animação ainda)
        self.enemies = {
            i: Enemy(e["x"], e["y"], e["size"])
            for i, e in enumerate(state.get("enemies", []))
        }

        self.projectiles = [
            Projectile(p["x"], p["y"], p["angle"])
            for p in state.get("projectiles", [])
        ]

    # -------------------------------------------------
    # Atualiza animações (lado cliente)
    # -------------------------------------------------
    def update_animations(self, dt, moving):
        player = self.players.get(self.local_player_id)
        if player:
            player.update(dt, moving)

    # -------------------------------------------------
    # Desenho
    # -------------------------------------------------
    def draw(self, screen):
        if not self.players:
            return

        main_player = self.players.get(self.local_player_id)
        if not main_player:
            return

        self.camera.update(main_player.rect)

        # 🟫 Mapa
        self.tilemap.draw(screen, self.camera)

        # 👾 Inimigos
        for enemy in self.enemies.values():
            enemy.draw(screen, self.camera)

        # 🧍 Jogadores
        for player in self.players.values():
            player.draw(screen, self.camera)

        for proj in self.projectiles:
            proj.draw(screen, self.camera)
