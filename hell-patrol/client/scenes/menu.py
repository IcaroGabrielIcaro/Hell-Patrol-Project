import pygame


class MenuScene:
    """
    Cena do menu principal.
    Navegação: Setas cima/baixo, Enter para selecionar.
    """

    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Opções do menu
        self.options = [
            "Jogar Sozinho",
            "Entrar em Sala",
            "Sair"
        ]
        self.selected_index = 0

        # Fonte para renderizar texto
        self.title_font = pygame.font.Font(None, 80)
        self.option_font = pygame.font.Font(None, 50)

        # Cores
        self.bg_color = (20, 20, 30)
        self.title_color = (255, 100, 100)
        self.selected_color = (255, 200, 0)
        self.normal_color = (200, 200, 200)

        self.choice = None  # Armazena a escolha do usuário

    def handle_input(self, event):
        """
        Processa input do usuário (teclado).
        Retorna True se uma escolha foi feita.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.options)

            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.options)

            elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                self.choice = self.options[self.selected_index]
                return True

        return False

    def draw(self, screen):
        """Desenha o menu na tela."""
        screen.fill(self.bg_color)

        # Título
        title_text = self.title_font.render("HELL PATROL", True, self.title_color)
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 150))
        screen.blit(title_text, title_rect)

        # Opções
        y_start = 300
        y_spacing = 80

        for i, option in enumerate(self.options):
            color = self.selected_color if i == self.selected_index else self.normal_color
            text = self.option_font.render(option, True, color)
            rect = text.get_rect(center=(self.screen_width // 2, y_start + i * y_spacing))

            # Desenha seta ao lado da opção selecionada
            if i == self.selected_index:
                arrow = self.option_font.render(">", True, self.selected_color)
                arrow_rect = arrow.get_rect(right=rect.left - 20, centery=rect.centery)
                screen.blit(arrow, arrow_rect)

            screen.blit(text, rect)

        # Instruções
        hint_font = pygame.font.Font(None, 30)
        hint_text = hint_font.render("Use SETAS para navegar | ENTER para selecionar", True, (150, 150, 150))
        hint_rect = hint_text.get_rect(center=(self.screen_width // 2, self.screen_height - 50))
        screen.blit(hint_text, hint_rect)

    def get_choice(self):
        """Retorna a escolha do usuário e reseta."""
        choice = self.choice
        self.choice = None
        return choice
