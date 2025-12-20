from shared.world import WORLD_WIDTH, WORLD_HEIGHT, PLAYER_SIZE
from .enemy_ai import follow_closest_player

ENEMY_SPEED = 850

class Enemy:
    def __init__(self, x, y):
        self.size = PLAYER_SIZE
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
            "x": int(self.x),
            "y": int(self.y),
            "size": self.size
        }
