from shared.world import WORLD_WIDTH, WORLD_HEIGHT, PLAYER_SIZE

class Player:
    def __init__(self):
        self.size = PLAYER_SIZE
        self.x = (WORLD_WIDTH // 2) - (PLAYER_SIZE // 2)
        self.y = (WORLD_HEIGHT // 2) - (PLAYER_SIZE // 2)

    def move(self, dx, dy):
        self.x += dx * 5
        self.y += dy * 5

    def to_dict(self):
        return {
            "x": self.x,
            "y": self.y,
            "size": self.size
        }