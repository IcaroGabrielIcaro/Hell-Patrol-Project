from shared.world import WORLD_WIDTH, WORLD_HEIGHT

class Camera:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.x = 0
        self.y = 0

    def update(self, target_rect):
        """
        target_rect: pygame.Rect do player (em coordenadas do mundo)
        """

        # Centraliza a câmera no player
        self.x = target_rect.centerx - self.screen_width // 2
        self.y = target_rect.centery - self.screen_height // 2

        # Clamp horizontal
        if self.x < 0:
            self.x = 0
        elif self.x > WORLD_WIDTH - self.screen_width:
            self.x = WORLD_WIDTH - self.screen_width

        # Clamp vertical
        if self.y < 0:
            self.y = 0
        elif self.y > WORLD_HEIGHT - self.screen_height:
            self.y = WORLD_HEIGHT - self.screen_height

    def apply(self, rect):
        """
        Converte um rect do mundo para a tela
        """
        return rect.move(-self.x, -self.y)
