from shared.world import WORLD_WIDTH, WORLD_HEIGHT, PLAYER_SIZE
from .enemy_ai import follow_closest_player

ENEMY_SPEED = 100

_enemy_id_counter = 0


def next_enemy_id():
    global _enemy_id_counter
    _enemy_id_counter += 1
    return _enemy_id_counter


class Enemy:
    def __init__(self, x, y):
        self.id = next_enemy_id()
        self.size = PLAYER_SIZE * 3
        self.x = x
        self.y = y

    def update(self, players, dt):
        dx, dy = follow_closest_player(self, players)

        self.x += dx * ENEMY_SPEED * dt
        self.y += dy * ENEMY_SPEED * dt

        # Clamp
        self.x = max(0, min(self.x, WORLD_WIDTH - self.size))
        self.y = max(0, min(self.y, WORLD_HEIGHT - self.size))

    def to_dict(self):
        return {
            "id": self.id,
            "x": int(self.x),
            "y": int(self.y),
            "size": self.size
        }
