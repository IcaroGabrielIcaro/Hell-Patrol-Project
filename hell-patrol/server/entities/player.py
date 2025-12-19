from shared.world import WORLD_WIDTH, WORLD_HEIGHT, PLAYER_SIZE
import math

SPEED = 1000  # pixels por segundo

class Player:
    def __init__(self):
        self.size = PLAYER_SIZE
        self.x = (WORLD_WIDTH // 2) - (PLAYER_SIZE // 2)
        self.y = (WORLD_HEIGHT // 2) - (PLAYER_SIZE // 2)

    def move(self, dx, dy, dt):
        """
        dx, dy: direção enviada pelo cliente (-1, 0, 1)
        dt: delta time do servidor
        """

        # Vetor direção
        length = math.hypot(dx, dy)

        if length > 0:
            dx /= length
            dy /= length

        # Aplica velocidade
        self.x += dx * SPEED * dt
        self.y += dy * SPEED * dt

        # Clamp no mundo
        self.x = max(0, min(self.x, WORLD_WIDTH - self.size))
        self.y = max(0, min(self.y, WORLD_HEIGHT - self.size))

    def to_dict(self):
        return {
            "x": int(self.x),
            "y": int(self.y),
            "size": self.size
        }