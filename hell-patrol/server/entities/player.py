from shared.world import WORLD_WIDTH, WORLD_HEIGHT, PLAYER_SIZE

SPEED = 10

class Player:
    def __init__(self):
        self.size = PLAYER_SIZE
        self.x = (WORLD_WIDTH // 2) - (PLAYER_SIZE // 2)
        self.y = (WORLD_HEIGHT // 2) - (PLAYER_SIZE // 2)

    def move(self, dx, dy):
        self.x += dx * SPEED
        self.y += dy * SPEED

        # Clamp horizontal
        if self.x < 0:
            self.x = 0
        elif self.x > WORLD_WIDTH - self.size:
            self.x = WORLD_WIDTH - self.size

        # Clamp vertical
        if self.y < 0:
            self.y = 0
        elif self.y > WORLD_HEIGHT - self.size:
            self.y = WORLD_HEIGHT - self.size

    def to_dict(self):
        return {
            "x": self.x,
            "y": self.y,
            "size": self.size
        }