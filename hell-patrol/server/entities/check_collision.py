import math

def enemy_player_collision(enemy, player):
    ex = enemy.x + enemy.size / 2
    ey = enemy.y + enemy.size / 2

    px = player.x + player.size / 2
    py = player.y + player.size / 2

    dist = math.hypot(ex - px, ey - py)

    return dist < (enemy.size + player.size) * 0.4

def projectile_enemy_collision(projectile, enemy):
    px = projectile.x
    py = projectile.y

    ex = enemy.x + enemy.size / 2
    ey = enemy.y + enemy.size / 2

    dist = math.hypot(px - ex, py - ey)

    return dist < enemy.size * 0.5