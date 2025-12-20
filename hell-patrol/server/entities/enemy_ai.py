import math

def follow_closest_player(enemy, players):
    if not players:
        return 0, 0

    closest = min(
        players,
        key=lambda p: math.hypot(enemy.x - p.x, enemy.y - p.y)
    )

    dx = closest.x - enemy.x
    dy = closest.y - enemy.y
    dist = math.hypot(dx, dy)

    if dist < 1e-3:
        return 0, 0

    return dx / dist, dy / dist
