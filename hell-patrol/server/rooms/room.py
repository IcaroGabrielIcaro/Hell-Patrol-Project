from server.entities.player import Player
from server.entities.enemy import Enemy
from server.entities.spawn import Spawn
from server.entities.check_collision import enemy_player_collision, projectile_enemy_collision
from server.entities.projectile import Projectile
from shared.world import WORLD_WIDTH, WORLD_HEIGHT
import math

SPAWN_INTERVAL = 3.0


class Room:
    def __init__(self):
        self.players = {}
        self.inputs = {}
        self.projectiles = []
        self.enemies = []
        self.spawns = []
        self.spawn_timer = 0.0
        self.game_over = False

    # =========================================================
    # Players
    # =========================================================
    def add_player(self, player_id):
        self.players[player_id] = Player()
        self.inputs[player_id] = {"dx": 0, "dy": 0, "angle": 0}

    def remove_player(self, player_id):
        del self.players[player_id]
        del self.inputs[player_id]

    # =========================================================
    # Projectiles
    # =========================================================
    def _create_projectile(self, player, angle):
        base_cx = player.x + player.size / 2
        base_cy = player.y + player.size / 2

        rad = math.radians(angle)
        front_x = math.cos(rad)
        front_y = -math.sin(rad)

        spawn_x = base_cx + front_x * player.center_forward
        spawn_y = base_cy + front_y * player.center_forward

        return Projectile(spawn_x, spawn_y, angle)

    # =========================================================
    # Network actions
    # =========================================================
    def handle_action(self, player_id, msg):
        player = self.players[player_id]

        # ---------------- RESTART ----------------
        if msg.get("restart") and self.game_over:
            self._restart_game()
            return

        if self.game_over:
            return  # bloqueia qualquer ação durante game over

        if msg["action"] == "move":
            self.inputs[player_id]["dx"] = msg["dx"]
            self.inputs[player_id]["dy"] = msg["dy"]
            player.set_angle(msg.get("angle", 0))

            if msg.get("shoot") and player.can_shoot():
                player.shoot()
                self.projectiles.append(self._create_projectile(player, msg["angle"]))

            if msg.get("reload"):
                player.reload()

    # =========================================================
    # Update loop
    # =========================================================
    def update(self, dt):
        if self.game_over:
            return

        # ---------------- Players ----------------
        for pid, player in self.players.items():
            if not player.alive:
                continue

            inp = self.inputs[pid]
            player.move(inp["dx"], inp["dy"], dt)
            player.set_angle(inp["angle"])
            player.update_timers(dt)

        # ---------------- Spawns ----------------
        if self.players:
            self.spawn_timer += dt
            if self.spawn_timer >= SPAWN_INTERVAL:
                self.spawn_timer -= SPAWN_INTERVAL
                self.spawns.append(Spawn())

        new_enemies = []
        alive_spawns = []

        for spawn in self.spawns:
            spawn.update(dt)
            if spawn.done:
                new_enemies.append(Enemy(spawn.x, spawn.y))
            else:
                alive_spawns.append(spawn)

        self.spawns = alive_spawns
        self.enemies.extend(new_enemies)

        # ---------------- Enemies ----------------
        alive_enemies = []

        for enemy in self.enemies:
            enemy.update(list(self.players.values()), dt)

            for player in self.players.values():
                if player.alive and enemy_player_collision(enemy, player):
                    player.alive = False

            alive_enemies.append(enemy)

        self.enemies = alive_enemies

        # ---------------- Projectiles ----------------
        alive_projectiles = []

        for proj in self.projectiles:
            proj.update(dt)
            if not proj.is_alive():
                continue

            hit = False
            for enemy in self.enemies:
                if projectile_enemy_collision(proj, enemy):
                    self.enemies.remove(enemy)
                    hit = True
                    break

            if not hit:
                alive_projectiles.append(proj)

        self.projectiles = alive_projectiles

        # ---------------- Game Over ----------------
        self.game_over = self._is_game_over()

    # =========================================================
    # Game Over / Restart
    # =========================================================
    def _is_game_over(self):
        if not self.players:
            return False

        return all(not p.alive for p in self.players.values())

    def _restart_game(self):
        self.projectiles.clear()
        self.enemies.clear()
        self.spawns.clear()
        self.spawn_timer = 0.0
        self.game_over = False

        for player in self.players.values():
            player.alive = True
            player.ammo = player.MAX_AMMO if hasattr(player, "MAX_AMMO") else 10
            player.cooldown = 0
            player.x = (WORLD_WIDTH // 2) - (player.size // 2)
            player.y = (WORLD_HEIGHT // 2) - (player.size // 2)

    # =========================================================
    # Snapshot
    # =========================================================
    def get_state(self):
        return {
            "players": {pid: p.to_dict() for pid, p in self.players.items()},
            "enemies": [e.to_dict() for e in self.enemies],
            "spawns": [s.to_dict() for s in self.spawns],
            "projectiles": [p.to_dict() for p in self.projectiles],
            "game_over": self.game_over
        }
