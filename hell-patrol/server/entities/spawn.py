import random
from shared.world import WORLD_WIDTH, WORLD_HEIGHT

SPAWN_DELAY = 1.5  # segundos até virar inimigo

_spawn_id = 0
def next_spawn_id():
    global _spawn_id
    _spawn_id += 1
    return _spawn_id


class Spawn:
    def __init__(self):
        self.id = next_spawn_id()
        self.x = random.randint(0, WORLD_WIDTH)
        self.y = random.randint(0, WORLD_HEIGHT)
        self.timer = 0.0
        self.done = False

    def update(self, dt):
        self.timer += dt
        if self.timer >= SPAWN_DELAY:
            self.done = True

    def to_dict(self):
        return {
            "id": self.id,
            "x": int(self.x),
            "y": int(self.y),
            "progress": min(self.timer / SPAWN_DELAY, 1.0)
        }
