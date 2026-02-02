import pygame
import math
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

        # 🔧 ajuste fino da distância da ponta da arma
        self.projectile_offset = 45  # TESTE: 35 / 40 / 45 / 50

    def update_state(self, state):
        server_players = state["players"]

        # -------------------------------
        # Atualiza ou cria players
        # -------------------------------
        for pid, p in server_players.items():
            if pid not in self.players:
                if pid == self.local_player_id:
                    self.players[pid] = Player(
                        p["x"], p["y"],
                        size=p.get("size"),
                        scale=2.7,
                        anim_speed=0.12
                    )
                else:
                    self.players[pid] = Player(
                        p["x"], p["y"],
                        size=p.get("size"),
                        scale=2.7
                    )
            else:
                player = self.players[pid]
                player.x = p["x"]
                player.y = p["y"]
                player.angle = p.get("angle", 0)
                player.rect.topleft = (player.x, player.y)

        # remove players desconectados
        for pid in list(self.players.keys()):
            if pid not in server_players:
                del self.players[pid]

        # -------------------------------
        # Atualiza inimigos
        # -------------------------------
        self.enemies = {
            i: Enemy(e["x"], e["y"], e["size"])
            for i, e in enumerate(state.get("enemies", []))
        }

        # -------------------------------
        # Atualiza projéteis (CORRIGIDO DE VERDADE)
        # -------------------------------
        self.projectiles = []

        for p in state.get("projectiles", []):
            angle = p["angle"]
            rad = math.radians(angle)

            # 🔵 vetor frontal (direção do tiro)
            front_x = math.cos(rad)
            front_y = -math.sin(rad)

            # 🟢 vetor lateral (perpendicular)
            side_x = math.sin(rad)
            side_y = math.cos(rad)

            # 🔧 AJUSTES FINOS (dinâmicos)
            front_offset = 0   # distância até a ponta do cano
            side_offset  = 0   # deslocamento da arma em relação ao centro

            spawn_x = (
                p["x"]
                + front_x * front_offset
                + side_x  * side_offset
            )

            spawn_y = (
                p["y"]
                + front_y * front_offset
                + side_y  * side_offset
            )

            self.projectiles.append(
                Projectile(spawn_x, spawn_y, angle)
            )

    def update_animations(self, dt, moving):
        player = self.players.get(self.local_player_id)
        if player:
            player.update(dt, moving)

    def draw(self, screen):
        if not self.players:
            return

        main_player = self.players.get(self.local_player_id)
        if not main_player:
            return

        self.camera.update(main_player.rect)

        # mapa
        self.tilemap.draw(screen, self.camera)

        # inimigos
        for enemy in self.enemies.values():
            enemy.draw(screen, self.camera)

        # jogadores
        for player in self.players.values():
            player.draw(screen, self.camera)

        # projéteis
        for proj in self.projectiles:
            proj.draw(screen, self.camera)
