import math

def enemy_player_collision(enemy, player):
    # ===== hitbox inimigo =====
    enemy_w = enemy.size * 0.5
    enemy_h = enemy.size * 0.5

    enemy_x = enemy.x + enemy.size / 2 - enemy_w / 2
    enemy_y = enemy.y + enemy.size / 2 - enemy_h / 2 - enemy.size * 0.35

    enemy_rect = (
        enemy_x,
        enemy_y,
        enemy_w,
        enemy_h
    )

    # ===== hitbox player =====
    player_w = player.size * 0.6
    player_h = player.size * 0.6

    player_x = player.x + player.size / 2 - player_w / 2
    player_y = player.y + player.size / 2 - player_h / 2

    player_rect = (
        player_x,
        player_y,
        player_w,
        player_h
    )

    # ===== AABB =====
    ex, ey, ew, eh = enemy_rect
    px, py, pw, ph = player_rect

    return (
        ex < px + pw and
        ex + ew > px and
        ey < py + ph and
        ey + eh > py
    )


def projectile_enemy_collision(projectile, enemy):
    px = projectile.x
    py = projectile.y + 60 

    ex = enemy.x + enemy.size / 2
    ey = enemy.y + enemy.size / 2

    dist = math.hypot(px - ex, py - ey)

    return dist < enemy.size * 0.5
