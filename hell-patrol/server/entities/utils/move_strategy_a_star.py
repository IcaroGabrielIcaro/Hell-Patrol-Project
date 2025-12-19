from shared.world import TILE_SIZE
import math

def follow_closest_player_smooth(enemy, players):
    if not players:
        return 0, 0

    # player mais próximo
    closest = min(players, key=lambda p: math.hypot(enemy.x - p.x, enemy.y - p.y))

    # distancia total
    dx = closest.x - enemy.x
    dy = closest.y - enemy.y
    dist = math.hypot(dx, dy)
    
    if dist < 1e-3:
        return 0, 0

    # vetor normalizado
    return dx / dist, dy / dist
