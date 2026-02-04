import pygame
from client.entities.player import Player
from client.entities.enemy import Enemy
from client.entities.spawn import Spawn
from client.entities.projectile import Projectile
from client.core.camera import Camera
from client.world.tilemap import TileMap


class GameplayScene:
    def __init__(self, screen_width, screen_height, tiles, tiles_ids, weights, player_id):
        self.players = {}        # player_id -> Player
        self.enemies = {}        # enemy_id -> Enemy
        self.spawns = {}         # spawn_id -> Spawn
        self.projectiles = []

        self.camera = Camera(screen_width, screen_height)
        self.local_player_id = player_id
        self.tilemap = TileMap(tiles, tiles_ids, weights)

    # =========================================================
    # Snapshot vindo do servidor
    # =========================================================
    def update_state(self, state):
        server_players = state.get("players", {})
        server_enemies = state.get("enemies", [])
        server_spawns = state.get("spawns", [])
        server_projectiles = state.get("projectiles", [])

        # ---------------- Players ----------------
        for pid, p in server_players.items():
            if pid not in self.players:
                player = Player(
                    p["x"],
                    p["y"],
                    size=p.get("size"),
                    scale=2.7,
                    anim_speed=0.12
                )
                # define alive como True inicialmente
                player.alive = True
                self.players[pid] = player
            else:
                player = self.players[pid]
                player.x = p["x"]
                player.y = p["y"]
                player.angle = p.get("angle", 0)
                player.rect.topleft = (player.x, player.y)
                # se o servidor envia estado de alive, pode atualizar aqui
                if "alive" in p:
                    player.alive = p["alive"]

        # remove players que não existem mais
        for pid in list(self.players.keys()):
            if pid not in server_players:
                del self.players[pid]

        # ---------------- Spawns ----------------
        alive_spawn_ids = set()
        for s in server_spawns:
            sid = s["id"]
            alive_spawn_ids.add(sid)

            if sid not in self.spawns:
                self.spawns[sid] = Spawn(
                    spawn_id=sid,
                    x=s["x"],
                    y=s["y"]
                )

        for sid in list(self.spawns.keys()):
            if sid not in alive_spawn_ids:
                del self.spawns[sid]

        # ---------------- Enemies ----------------
        alive_enemy_ids = set()
        for e in server_enemies:
            eid = e["id"]
            alive_enemy_ids.add(eid)

            if eid not in self.enemies:
                self.enemies[eid] = Enemy(
                    enemy_id=eid,
                    x=e["x"],
                    y=e["y"],
                    size=e["size"]
                )
            else:
                self.enemies[eid].update_position(e["x"], e["y"])

        for eid in list(self.enemies.keys()):
            if eid not in alive_enemy_ids:
                del self.enemies[eid]

        # ---------------- Projectiles ----------------
        self.projectiles.clear()
        for p in server_projectiles:
            self.projectiles.append(
                Projectile(p["x"], p["y"], p["angle"])
            )

    # =========================================================
    # Atualização visual (animações)
    # =========================================================
    def update_animations(self, dt):
        for spawn in self.spawns.values():
            spawn.update(dt)

        for enemy in self.enemies.values():
            enemy.update(dt)

        # atualiza jogadores
        for player in self.players.values():
            player.update(dt, moving=True)

    # =========================================================
    # Helper da câmera
    # =========================================================
    def get_camera_target(self):
        local = self.players.get(self.local_player_id)
        if local and getattr(local, "alive", True):
            return local

        # escolhe outro player vivo mais próximo do local
        alive_players = [p for p in self.players.values() if getattr(p, "alive", True)]
        if not alive_players:
            return None

        if local:
            alive_players.sort(key=lambda p: (p.x - local.x)**2 + (p.y - local.y)**2)
            return alive_players[0]

        return alive_players[0]

    # =========================================================
    # Render
    # =========================================================
    def draw(self, screen):
        if not self.players:
            return

        target_player = self.get_camera_target()
        if target_player:
            self.camera.update(target_player.rect)

        self.tilemap.draw(screen, self.camera)

        for spawn in self.spawns.values():
            spawn.draw(screen, self.camera)

        for enemy in self.enemies.values():
            enemy.draw(screen, self.camera)

        for player in self.players.values():
            player.draw(screen, self.camera)

        for proj in self.projectiles:
            proj.draw(screen, self.camera)
