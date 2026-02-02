from shared.world import WORLD_WIDTH, WORLD_HEIGHT

class Camera:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.x = 0
        self.y = 0

    def update(self, target_rect):
        # Caso 1 — mundo MAIOR que a tela → câmera segue player
        if WORLD_WIDTH > self.screen_width:
            self.x = target_rect.centerx - self.screen_width // 2
            self.x = max(0, min(self.x, WORLD_WIDTH - self.screen_width))
        else:
            # Caso 2 — mundo MENOR que a tela → centraliza o mundo
            self.x = -(self.screen_width - WORLD_WIDTH) // 2

        if WORLD_HEIGHT > self.screen_height:
            self.y = target_rect.centery - self.screen_height // 2
            self.y = max(0, min(self.y, WORLD_HEIGHT - self.screen_height))
        else:
            self.y = -(self.screen_height - WORLD_HEIGHT) // 2

    def apply(self, rect):
        return rect.move(-self.x, -self.y)

    def apply_pos(self, pos):
        return (pos[0] - self.x, pos[1] - self.y)
