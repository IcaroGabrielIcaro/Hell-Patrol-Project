from server.entities.player import Player

class Room:
    def __init__(self):
        self.players = {}

    def add_player(self, player_id):
        self.players[player_id] = Player()

    def remove_player(self, player_id):
        del self.players[player_id]

    def handle_action(self, player_id, msg):
        if msg["action"] == "move":
            self.players[player_id].move(msg["dx"], msg["dy"])

    def get_state(self):
        return {
            "players": {
                pid: p.to_dict()
                for pid, p in self.players.items()
            }
        }
