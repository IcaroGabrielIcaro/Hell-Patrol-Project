from server.entities.player import Player
from server.entities.enemy import Enemy
from server.entities.spawn import Spawn
from server.entities.check_collision import enemy_player_collision, projectile_enemy_collision
from server.entities.projectile import Projectile
from shared.world import WORLD_WIDTH, WORLD_HEIGHT
import math
import random

SPAWN_INTERVAL = 3.0

class Room:
    def __init__(self):
        self.players = {}
        self.inputs = {}
        self.projectiles = []
        self.enemies = []
        self.spawns = []
        self.spawn_timer = 0.0

    def add_player(self, player_id):
        self.players[player_id] = Player()
        self.inputs[player_id] = {"dx": 0, "dy": 0, "angle": 0}

    def remove_player(self, player_id):
        del self.players[player_id]
        del self.inputs[player_id]

    def _create_projectile(self, player, angle):
        """Cria um projétil na posição da arma do jogador."""
        # Centro base do sprite
        base_cx = player.x + player.size / 2
        base_cy = player.y + player.size / 2

        # Vetores direcionais
        rad = math.radians(angle)
        front_x = math.cos(rad)
        front_y = -math.sin(rad)
        side_x = math.sin(rad)
        side_y = math.cos(rad)

        # Centro lógico do player (rotacionado)
        cx = base_cx + front_x * player.center_forward + side_x * player.center_side
        cy = base_cy + front_y * player.center_forward + side_y * player.center_side

        # Ponta da arma (ajuste conforme necessário)
        RAIO_ARMA = 0
        AJUSTE_LATERAL = 0
        spawn_x = cx + front_x * RAIO_ARMA + side_x * AJUSTE_LATERAL
        spawn_y = cy + front_y * RAIO_ARMA + side_y * AJUSTE_LATERAL

        return Projectile(spawn_x, spawn_y, angle)

    def handle_action(self, player_id, msg):
        player = self.players[player_id]

        if msg["action"] == "move":
            self.inputs[player_id]["dx"] = msg["dx"]
            self.inputs[player_id]["dy"] = msg["dy"]
            player.set_angle(msg.get("angle", 0))

            # Processa tiro se vier junto
            if msg.get("shoot") and player.can_shoot():
                player.shoot()
                self.projectiles.append(self._create_projectile(player, msg["angle"]))

            # Processa recarga se vier junto
            if msg.get("reload"):
                player.reload()

        elif msg["action"] == "shoot":
            if player.can_shoot():
                player.shoot()
                self.projectiles.append(self._create_projectile(player, msg["angle"]))

        elif msg["action"] == "reload":
            player.reload()

    def update(self, dt):
        # --------------------
        # atualiza jogadores
        # --------------------
        for pid, player in self.players.items():
            if not player.alive:
                continue

            inp = self.inputs[pid]
            player.move(inp["dx"], inp["dy"], dt)
            player.set_angle(inp["angle"])
            player.update_timers(dt)

        # --------------------
        # spawns
        # --------------------
        if self.players:  
            self.spawn_timer += dt
            if self.spawn_timer >= SPAWN_INTERVAL:
                self.spawn_timer -= SPAWN_INTERVAL
                self.spawns.append(Spawn())

        new_enemies = []
        alive_spawns = []

        for spawn in self.spawns:
            spawn.update(dt)
            if spawn.done:
                new_enemies.append(Enemy(spawn.x, spawn.y))
            else:
                alive_spawns.append(spawn)

        self.spawns = alive_spawns
        self.enemies.extend(new_enemies)
        
        # --------------------
        # atualiza inimigos
        # --------------------
        player_list = list(self.players.values())
        alive_enemies = []

        for enemy in self.enemies:
            enemy.update(player_list, dt)

            killed = False

            # colisão enemy x player
            for player in player_list:
                if not player.alive:
                    continue

                if enemy_player_collision(enemy, player):
                    player.alive = False
                    killed = False  # inimigo continua vivo
                    break

            if not killed:
                alive_enemies.append(enemy)

        self.enemies = alive_enemies

        # --------------------
        # atualiza projéteis
        # --------------------
        alive_projectiles = []
        alive_enemies = self.enemies

        for proj in self.projectiles:
            proj.update(dt)
            if not proj.is_alive():
                continue

            hit = False

            for enemy in alive_enemies:
                if projectile_enemy_collision(proj, enemy):
                    hit = True
                    alive_enemies.remove(enemy)
                    break

            if not hit:
                alive_projectiles.append(proj)

        self.projectiles = alive_projectiles
        self.enemies = alive_enemies


    def get_state(self):
        reloaded_players = []

        for pid, player in self.players.items():
            if player.consume_reload_flag():
                reloaded_players.append(pid)

        return {
            "players": {pid: p.to_dict() for pid, p in self.players.items()},
            "enemies": [e.to_dict() for e in self.enemies],
            "spawns": [s.to_dict() for s in self.spawns],
            "projectiles": [p.to_dict() for p in self.projectiles],
            "reloaded_players": reloaded_players
        }
