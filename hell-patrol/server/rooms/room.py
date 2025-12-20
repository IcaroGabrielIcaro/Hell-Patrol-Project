from server.entities.player import Player
from server.entities.enemy import Enemy
from shared.world import WORLD_WIDTH, WORLD_HEIGHT
import random

class Room:
    def __init__(self):
        self.players = {}
        self.inputs = {}
        self.enemies = []
        self.spawn_enemy()

    def spawn_enemy(self):
        x = random.randint(100, WORLD_WIDTH - 100)
        y = random.randint(100, WORLD_HEIGHT - 100)
        self.enemies.append(Enemy(x, y))

    def add_player(self, player_id):
        self.players[player_id] = Player()
        self.inputs[player_id] = {"dx": 0, "dy": 0}

    def remove_player(self, player_id):
        del self.players[player_id]
        del self.inputs[player_id]

    def handle_action(self, player_id, msg):
        if msg["action"] == "move":
            self.inputs[player_id]["dx"] = msg["dx"]
            self.inputs[player_id]["dy"] = msg["dy"]

    def update(self, dt):
        for pid, player in self.players.items():
            inp = self.inputs[pid]
            player.move(inp["dx"], inp["dy"], dt)

        player_list = list(self.players.values())
        for enemy in self.enemies:
            enemy.update(player_list, dt)

    def get_state(self):
        return {
            "players": {
                pid: p.to_dict()
                for pid, p in self.players.items()
            },
            "enemies": [
                e.to_dict()
                for e in self.enemies
            ]
        }
