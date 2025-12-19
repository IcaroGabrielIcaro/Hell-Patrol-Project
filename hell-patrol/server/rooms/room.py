from server.entities.player import Player
from server.entities.enemy import Enemy
from server.entities.utils.move_strategy_a_star import follow_closest_player_smooth

class Room:
    def __init__(self):
        self.players = {}
        self.enemies = [Enemy(follow_closest_player_smooth) for _ in range(7)]

    def add_player(self, player_id):
        self.players[player_id] = Player()

    def remove_player(self, player_id):
        if player_id in self.players:
            del self.players[player_id]

    def handle_action(self, player_id, msg):
        if msg["action"] == "move":
            self.players[player_id].move(msg["dx"], msg["dy"])

    def update(self):
        for enemy in self.enemies:
            enemy.update(list(self.players.values()))

    def get_state(self):
        self.update()
        return {
            "players": {pid: p.to_dict() for pid,p in self.players.items()},
            "enemies": [e.to_dict() for e in self.enemies]
        }
