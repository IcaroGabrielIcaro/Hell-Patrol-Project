from shared.world import WORLD_WIDTH, WORLD_HEIGHT, PLAYER_SIZE
import math

SPEED = 1000
MAX_AMMO = 10
FIRE_COOLDOWN = 0.28  # agora funciona corretamente

class Player:
    def __init__(self):
        self.size = PLAYER_SIZE
        self.x = (WORLD_WIDTH // 2) - (PLAYER_SIZE // 2)
        self.y = (WORLD_HEIGHT // 2) - (PLAYER_SIZE // 2)
        self.angle = 0
        
        self.alive = True
         
        self.ammo = MAX_AMMO
        self.cooldown = 0.0
        self.just_reloaded = False

    def move(self, dx, dy, dt):
        if not self.alive:
            return
        length = math.hypot(dx, dy)
        if length > 0:
            dx /= length
            dy /= length

        self.x += dx * SPEED * dt
        self.y += dy * SPEED * dt

        self.x = max(0, min(self.x, WORLD_WIDTH - self.size))
        self.y = max(0, min(self.y, WORLD_HEIGHT - self.size))

    def set_angle(self, angle):
        if self.alive:
            self.angle = angle

    def update_timers(self, dt):
        if self.cooldown > 0:
            self.cooldown -= dt

    def can_shoot(self):
        return (self.ammo > 0 and self.cooldown <= 0) and self.alive

    def shoot(self):
        if not self.can_shoot():
            return False

        self.ammo -= 1
        self.cooldown = FIRE_COOLDOWN
        return True

    def reload(self):
        self.ammo = MAX_AMMO
        self.just_reloaded = True

    def consume_reload_flag(self):
        if self.just_reloaded:
            self.just_reloaded = False
            return True
        return False

    def to_dict(self):
        return {
            "x": int(self.x),
            "y": int(self.y),
            "size": self.size,
            "angle": self.angle,
            "ammo": self.ammo,
            "alive": self.alive
        }
