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

    def update_state(self, state):
        server_players = state["players"]

        # atualiza ou cria players
        for pid, p in server_players.items():
            if pid not in self.players:
                # player novo
                if pid == self.local_player_id:
                    # player local com animação configurável
                    self.players[pid] = Player(
                        p["x"], p["y"],
                        size=p.get("size"),
                        scale=2.7,
                        anim_speed=0.12
                    )
                else:
                    # Outros players
                    self.players[pid] = Player(
                        p["x"], p["y"],
                        size=p.get("size"),
                        scale=2.7
                    )
            else:
                # atualiza player existente
                player = self.players[pid]
                player.x = p["x"]
                player.y = p["y"]
                player.angle = p.get("angle", 0)
                player.rect.topleft = (player.x, player.y)

        # remove players que saíram
        for pid in list(self.players.keys()):
            if pid not in server_players:
                del self.players[pid]

        # atualiza inimigos
        self.enemies = {
            i: Enemy(e["x"], e["y"], e["size"])
            for i, e in enumerate(state.get("enemies", []))
        }

        # atualiza projéteis
        self.projectiles = [
            Projectile(p["x"], p["y"], p["angle"])
            for p in state.get("projectiles", [])
        ]

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

        # desenha mapa
        self.tilemap.draw(screen, self.camera)

        # desenha inimigos
        for enemy in self.enemies.values():
            enemy.draw(screen, self.camera)

        # desenha jogadores
        for player in self.players.values():
            player.draw(screen, self.camera)

        # desenha projéteis
        for proj in self.projectiles:
            proj.draw(screen, self.camera)


