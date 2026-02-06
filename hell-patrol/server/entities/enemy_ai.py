import math
import random

STOP_RADIUS = 10

def follow_closest_player(enemy, players):
    alive_players = [p for p in players if getattr(p, "alive", True)]

    if alive_players:
        # segue o player mais próximo
        closest = min(
            alive_players,
            key=lambda p: math.hypot(enemy.x - p.x, enemy.y - p.y)
        )

        dx = closest.x - enemy.x
        dy = closest.y - enemy.y
        dist = math.hypot(dx, dy)

        if dist <= STOP_RADIUS:
            return 0.0, 0.0

        return dx / dist, dy / dist
    else:
        # sem players vivos → direção aleatória
        angle = random.uniform(0, 2 * math.pi)
        return math.cos(angle), math.sin(angle)
