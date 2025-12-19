from client.entities.player import Player
from client.entities.enemy import Enemy
from client.core.camera import Camera
from client.world.tilemap import TileMap

class GameplayScene:
    def __init__(self, screen_width, screen_height, tile_image):
        self.players = {}
        self.enemies = {}
        self.camera = Camera(screen_width, screen_height)
        self.tilemap = TileMap(tile_image)

    def update_state(self, state):
        # Atualiza players
        self.players = {
            pid: Player(p["x"], p["y"], p["size"])
            for pid, p in state.get("players", {}).items()
        }
        # Atualiza inimigos
        self.enemies = [
            Enemy(e["x"], e["y"], e["size"])
            for e in state.get("enemies", [])
        ]

    def draw(self, screen):
        if not self.players and not self.enemies:
            return

        main_player = next(iter(self.players.values()), None)
        if main_player:
            self.camera.update(main_player.rect)

        # 1️⃣ Desenha o chão
        self.tilemap.draw(screen, self.camera)

        # 2️⃣ Desenha jogadores
        for player in self.players.values():
            player.draw(screen, self.camera)

        # 3️⃣ Desenha inimigos
        for enemy in self.enemies:
            enemy.draw(screen, self.camera)
