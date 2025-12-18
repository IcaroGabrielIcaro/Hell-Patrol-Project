import pygame
from client.core.input import get_movement
from shared.protocol import make_move

class Game:
    def __init__(self, screen, network, scene):
        self.screen = screen
        self.network = network
        self.scene = scene

    def run(self, clock):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            dx, dy = get_movement()
            self.network.send(make_move(dx, dy))

            state = self.network.receive()
            self.scene.update_state(state)

            self.screen.fill((30, 30, 30))
            self.scene.draw(self.screen)
            pygame.display.flip()

            clock.tick(60)

        self.network.close()
