"""
Aplicação principal que gerencia o fluxo entre menu, lobby e gameplay.
"""
import pygame
from client.config import FPS, SERVER_HOST, SERVER_PORT
from client.core.network import NetworkClient
from client.core.game import Game
from client.scenes.gameplay import GameplayScene
from client.scenes.menu import MenuScene
from client.scenes.lobby import LobbyScene
from client.assets.loader import TileLoader


class GameApplication:
    """Aplicação principal que gerencia o fluxo entre menu, lobby e gameplay"""

    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "MENU"  # MENU, LOBBY, GAMEPLAY
        self.screen_width, self.screen_height = screen.get_size()

        # Carrega tiles
        self.tiles, self.tile_ids, self.weights = TileLoader.load_tiles()

        # Inicializa menu
        self.menu = MenuScene(self.screen_width, self.screen_height)
        self.lobby = None
        self.game = None

    def run(self):
        """Loop principal da aplicação"""
        while self.running:
            if self.state == "MENU":
                self._run_menu()
            elif self.state == "LOBBY":
                self._run_lobby()
            elif self.state == "GAMEPLAY":
                self._run_game()

        pygame.quit()

    def _create_game(self, host, port):
        """
        Cria uma instância do jogo conectada ao servidor.
        Retorna o objeto Game ou None em caso de erro.
        """
        try:
            network = NetworkClient(host, port)
            scene = GameplayScene(
                self.screen_width,
                self.screen_height,
                self.tiles,
                self.tile_ids,
                self.weights,
                network.player_id
            )
            return Game(self.screen, network, scene)
        except Exception as e:
            print(f"Erro ao conectar ao servidor: {e}")
            return None

    def _run_menu(self):
        """Executa o menu principal"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            self.menu.handle_input(event)

        # Verifica se houve escolha
        choice = self.menu.get_choice()

        if choice == "Jogar Sozinho":
            self.game = self._create_game(SERVER_HOST, SERVER_PORT)
            if self.game:
                self.state = "GAMEPLAY"
            else:
                print("Certifique-se de que o servidor está rodando: python -m server.main")

        elif choice == "Entrar em Sala":
            self.lobby = LobbyScene(self.screen_width, self.screen_height)
            self.state = "LOBBY"

        elif choice == "Sair":
            self.running = False
            return

        # Renderiza menu
        self.menu.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(FPS)

    def _run_lobby(self):
        """Executa a tela de lobby"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                if self.lobby:
                    self.lobby.cleanup()
                return

            self.lobby.handle_input(event)

        # Verifica se houve escolha
        choice = self.lobby.get_choice()

        if choice:
            action, data = choice

            if action == "back":
                self.lobby.cleanup()
                self.lobby = None
                self.state = "MENU"

            elif action == "create":
                self.lobby.cleanup()
                self.game = self._create_game(SERVER_HOST, SERVER_PORT)
                if self.game:
                    self.state = "GAMEPLAY"
                else:
                    self.lobby = LobbyScene(self.screen_width, self.screen_height)

            elif action == "join":
                room_info = data
                self.lobby.cleanup()
                self.game = self._create_game(room_info["host"], room_info["port"])
                if self.game:
                    self.state = "GAMEPLAY"
                else:
                    self.lobby = LobbyScene(self.screen_width, self.screen_height)

        # Renderiza lobby
        if self.lobby:
            self.lobby.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(FPS)

    def _run_game(self):
        """Executa o jogo"""
        dt = self.clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                if self.game:
                    self.game.network.close()
                return

            # ESC para voltar ao menu
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if self.game:
                    self.game.network.close()
                self.state = "MENU"
                self.game = None
                return

        # Atualiza e desenha o jogo
        if self.game:
            if not self.game.update_and_draw(dt):
                # Jogo retornou False, volta para o menu
                self.game.network.close()
                self.state = "MENU"
                self.game = None
