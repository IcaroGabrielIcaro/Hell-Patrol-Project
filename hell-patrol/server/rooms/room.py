from server.entities.player import Player
from server.entities.enemy import Enemy
from server.entities.projectile import Projectile
from shared.world import WORLD_WIDTH, WORLD_HEIGHT
import math
import random

class Room:
    def __init__(self):
        self.players = {}
        self.inputs = {}
        self.projectiles = []
        self.enemies = []
        self.spawn_enemy()

    def spawn_enemy(self):
        x = random.randint(100, WORLD_WIDTH - 100)
        y = random.randint(100, WORLD_HEIGHT - 100)
        self.enemies.append(Enemy(x, y))

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
        # atualiza jogadores
        for pid, player in self.players.items():
            inp = self.inputs[pid]
            player.move(inp["dx"], inp["dy"], dt)
            player.set_angle(inp["angle"])
            player.update_timers(dt)

        # atualiza inimigos
        player_list = list(self.players.values())
        for enemy in self.enemies:
            enemy.update(player_list, dt)

        # atualiza projéteis e remove os que saíram do mundo
        alive = []
        for p in self.projectiles:
            p.update(dt)
            if p.is_alive():
                alive.append(p)
        self.projectiles = alive

    def get_state(self):
        reloaded_players = []

        # verifica quais jogadores acabaram de recarregar
        for pid, player in self.players.items():
            if player.consume_reload_flag():
                reloaded_players.append(pid)

        return {
            "players": {
                pid: p.to_dict()
                for pid, p in self.players.items()
            },
            "enemies": [
                e.to_dict()
                for e in self.enemies
            ],
            "projectiles": [
                p.to_dict()
                for p in self.projectiles
            ],
            "reloaded_players": reloaded_players
        }

