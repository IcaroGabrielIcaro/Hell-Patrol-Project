from server.entities.player import Player
from server.entities.enemy import Enemy
from server.entities.projectile import Projectile
from shared.world import WORLD_WIDTH, WORLD_HEIGHT
import random
import math

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

    def handle_action(self, player_id, msg):
        player = self.players[player_id]

        if msg["action"] == "move":
            self.inputs[player_id]["dx"] = msg["dx"]
            self.inputs[player_id]["dy"] = msg["dy"]
            player.set_angle(msg.get("angle", 0))

            # processa tiro se vier junto
            if msg.get("shoot") and player.can_shoot():
                player.shoot()

                # Calcula a posição da ponta da arma
                angle_rad = math.radians(-msg["angle"])
                gun_length = 25 * 2.7  # gun_length * scale do player
                gun_offset_x = 18 * 2.7  # offset da arma em X * scale
                gun_offset_y = -4 * 2.7  # offset da arma em Y * scale

                # Centro do player
                center_x = player.x + player.size // 2
                center_y = player.y + player.size // 2

                # Aplica offset da arma com rotação
                gun_base_x = center_x + gun_offset_x * math.cos(angle_rad) - gun_offset_y * math.sin(angle_rad)
                gun_base_y = center_y + gun_offset_x * math.sin(angle_rad) + gun_offset_y * math.cos(angle_rad)

                # Adiciona o comprimento da arma na direção que ela aponta
                px = gun_base_x + math.cos(angle_rad) * gun_length
                py = gun_base_y + math.sin(angle_rad) * gun_length

                self.projectiles.append(
                    Projectile(px, py, msg["angle"])
                )

            # processa recarga se vier junto
            if msg.get("reload"):
                player.reload()

        elif msg["action"] == "shoot":
            if player.can_shoot():
                player.shoot()

                # Calcula a posição da ponta da arma
                angle_rad = math.radians(-msg["angle"])
                gun_length = 25 * 2.7  # gun_length * scale do player
                gun_offset_x = 18 * 2.7  # offset da arma em X * scale
                gun_offset_y = -4 * 2.7  # offset da arma em Y * scale

                # Centro do player
                center_x = player.x + player.size // 2
                center_y = player.y + player.size // 2

                # Aplica offset da arma com rotação
                gun_base_x = center_x + gun_offset_x * math.cos(angle_rad) - gun_offset_y * math.sin(angle_rad)
                gun_base_y = center_y + gun_offset_x * math.sin(angle_rad) + gun_offset_y * math.cos(angle_rad)

                # Adiciona o comprimento da arma na direção que ela aponta
                px = gun_base_x + math.cos(angle_rad) * gun_length
                py = gun_base_y + math.sin(angle_rad) * gun_length

                self.projectiles.append(
                    Projectile(px, py, msg["angle"])
                )

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

