from shared.world import WORLD_WIDTH, WORLD_HEIGHT, PLAYER_SIZE

class Enemy:
    def __init__(self, move_strategy, size=PLAYER_SIZE, speed=5):
        self.size = size
        self.x = WORLD_WIDTH // 2
        self.y = WORLD_HEIGHT // 2
        self.speed = speed
        self.move_strategy = move_strategy  # função que retorna dx, dy

    def update(self, players):
        dx, dy = self.move_strategy(self, players)
        self.x += dx * self.speed
        self.y += dy * self.speed

        # Clamp
        self.x = max(0, min(self.x, WORLD_WIDTH - self.size))
        self.y = max(0, min(self.y, WORLD_HEIGHT - self.size))

    def to_dict(self):
        return {"x": self.x, "y": self.y, "size": self.size}
    
    