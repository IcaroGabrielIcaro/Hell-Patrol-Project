from entities.utils.pathfinding import Pathfinder
from shared.world import TILE_SIZE
import math

# Strategy function: recebe enemy e lista de players, retorna dx, dy
def follow_closest_player_a_star(enemy, players):
    if not players:
        return 0, 0

    # pega player mais próximo
    closest = min(players, key=lambda p: math.hypot(enemy.x - p.x, enemy.y - p.y))

    # converte para célula
    start = (int(enemy.x)//TILE_SIZE, int(enemy.y)//TILE_SIZE)
    goal  = (int(closest.x)//TILE_SIZE, int(closest.y)//TILE_SIZE)

    pathfinder = Pathfinder()  # sem obstáculos por enquanto
    path = pathfinder.a_star(start, goal)

    if not path:
        return 0, 0

    # próxima célula
    next_cell = path[0]
    tx, ty = next_cell[0]*TILE_SIZE, next_cell[1]*TILE_SIZE

    # calcula direção normalizada
    dx = tx - enemy.x
    dy = ty - enemy.y
    dist = math.hypot(dx, dy)
    if dist == 0:
        return 0, 0
    return dx/dist, dy/dist
