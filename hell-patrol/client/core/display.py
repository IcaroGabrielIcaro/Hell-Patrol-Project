#inicia do pygame e configura a tela

import pygame


class Display:
    @staticmethod
    def init_fullscreen():
        pygame.init()
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        screen_width, screen_height = screen.get_size()
        return screen, screen_width, screen_height
