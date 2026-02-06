from shared.world import WORLD_WIDTH, WORLD_HEIGHT, PLAYER_SIZE
from .enemy_ai import follow_closest_player

ENEMY_SPEED = 200

_enemy_id_counter = 0


def next_enemy_id():
    global _enemy_id_counter
    _enemy_id_counter += 1
    return _enemy_id_counter


class Enemy:
    def __init__(self, x, y):
        self.id = next_enemy_id()
        self.size = PLAYER_SIZE * 3

        # posição real (float)
        self.x = float(x)
        self.y = float(y)

        self.vx = 0.0
        self.vy = 0.0

    def update(self, players, dt):
        dx, dy = follow_closest_player(self, players)

        self.vx = dx * ENEMY_SPEED
        self.vy = dy * ENEMY_SPEED

        self.x += self.vx * dt
        self.y += self.vy * dt

        # Clamp
        self.x = max(0.0, min(self.x, WORLD_WIDTH - self.size))
        self.y = max(0.0, min(self.y, WORLD_HEIGHT - self.size))

    def to_dict(self):
        return {
            "id": self.id,
            "x": self.x,       # float
            "y": self.y,       # float
            "vx": self.vx,     
            "vy": self.vy,
            "size": self.size
        }
