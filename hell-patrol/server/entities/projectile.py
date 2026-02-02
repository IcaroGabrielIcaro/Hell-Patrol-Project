import math
from shared.world import WORLD_WIDTH, WORLD_HEIGHT

SPEED = 1400
MAX_DISTANCE = 900  # distância máxima antes do projétil desaparecer

class Projectile:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle

        # Converte ângulo para vetor direção
        rad = math.radians(angle)
        self.dx = math.cos(rad)
        self.dy = -math.sin(rad)

        self.distance_traveled = 0

    def update(self, dt):
        vx = self.dx * SPEED * dt
        vy = self.dy * SPEED * dt

        self.x += vx
        self.y += vy

        self.distance_traveled += math.hypot(vx, vy)

    def is_alive(self):
        return (
            0 <= self.x <= WORLD_WIDTH and
            0 <= self.y <= WORLD_HEIGHT and
            self.distance_traveled < MAX_DISTANCE
        )

    def to_dict(self):
        return {
            "x": int(self.x),
            "y": int(self.y),
            "angle": self.angle
        }
