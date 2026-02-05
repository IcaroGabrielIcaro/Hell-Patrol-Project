"""
Tela de lobby para listar e selecionar salas abertas.
Escaneia salas via broadcast UDP e exibe lista navegável.
"""
import pygame
import threading
import socket
import json
import time


class LobbyScene:
    """
    Cena de lobby para descoberta e seleção de salas multiplayer.
    Escaneia rede local via UDP broadcast para encontrar salas abertas.
    """

    DISCOVERY_PORT = 12345  # Porta para discovery de salas

    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Lista de salas descobertas: {(ip, port): {"host": ip, "port": port, "last_seen": timestamp}}
        self.rooms = {}
        self.room_list = []  # Lista ordenada para navegação
        self.selected_index = 0

        # Fontes
        self.title_font = pygame.font.Font(None, 70)
        self.option_font = pygame.font.Font(None, 45)
        self.small_font = pygame.font.Font(None, 30)

        # Cores
        self.bg_color = (20, 20, 30)
        self.title_color = (100, 200, 255)
        self.selected_color = (255, 200, 0)
        self.normal_color = (200, 200, 200)

        # Estado
        self.choice = None
        self.scanning = True
        self.scan_thread = None

        # Socket UDP para escaneamento
        self.udp_socket = None
        self.setup_udp_socket()

        # Inicia thread de escaneamento
        self.start_scanning()

        # Adiciona opção "Criar Nova Sala"
        self.create_room_option = ">> Criar Nova Sala <<"

    def setup_udp_socket(self):
        """Configura socket UDP para receber broadcasts de salas."""
        try:
            self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.udp_socket.bind(('', self.DISCOVERY_PORT))
            self.udp_socket.settimeout(0.5)  # Timeout curto para não bloquear
            print(f"[LOBBY] Socket UDP configurado na porta {self.DISCOVERY_PORT}")
        except Exception as e:
            print(f"[LOBBY] Erro ao configurar socket UDP: {e}")

    def start_scanning(self):
        """Inicia thread para escaneamento contínuo de salas."""
        self.scanning = True
        self.scan_thread = threading.Thread(target=self._scan_loop, daemon=True)
        self.scan_thread.start()

    def _scan_loop(self):
        """Loop de escaneamento de salas (roda em thread separada)."""
        while self.scanning:
            try:
                # Verifica se socket ainda está válido
                if not self.udp_socket:
                    break

                # Recebe broadcasts de salas
                data, addr = self.udp_socket.recvfrom(1024)
                message = json.loads(data.decode('utf-8'))

                if message.get('type') == 'room_announcement':
                    room_key = (addr[0], message['port'])
                    self.rooms[room_key] = {
                        'host': addr[0],
                        'port': message['port'],
                        'players': message.get('players', 0),
                        'last_seen': time.time()
                    }
                    # Atualiza lista ordenada
                    self._update_room_list()

            except socket.timeout:
                # Timeout é normal, continua escaneando
                pass
            except OSError:
                # Socket foi fechado, para o loop
                break
            except Exception as e:
                if self.scanning:  # Só mostra erro se ainda deveria estar escaneando
                    print(f"[LOBBY] Erro no escaneamento: {e}")
                break

            # Remove salas que não foram vistas há mais de 5 segundos
            self._cleanup_old_rooms()

            time.sleep(0.1)  # Pequeno delay para não consumir CPU

    def _update_room_list(self):
        """Atualiza lista ordenada de salas para navegação."""
        self.room_list = [
            f"Sala de {room['host']}:{room['port']} ({room.get('players', '?')} jogadores)"
            for room in self.rooms.values()
        ]
        # Mantém índice válido
        if self.selected_index >= len(self.room_list) + 1:
            self.selected_index = 0

    def _cleanup_old_rooms(self):
        """Remove salas que não enviaram broadcast recentemente."""
        current_time = time.time()
        expired_rooms = [
            key for key, room in self.rooms.items()
            if current_time - room['last_seen'] > 5.0
        ]
        for key in expired_rooms:
            del self.rooms[key]
        if expired_rooms:
            self._update_room_list()

    def handle_input(self, event):
        """
        Processa input do usuário.
        Retorna True se uma escolha foi feita.
        """
        if event.type == pygame.KEYDOWN:
            total_options = len(self.room_list) + 2  # Salas + Criar + Voltar

            if event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % total_options

            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % total_options

            elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                # Opção "Criar Nova Sala"
                if self.selected_index == len(self.room_list):
                    self.choice = ('create', None)
                    return True
                # Opção "Voltar"
                elif self.selected_index == len(self.room_list) + 1:
                    self.choice = ('back', None)
                    return True
                # Sala selecionada
                elif self.selected_index < len(self.room_list):
                    room_info = list(self.rooms.values())[self.selected_index]
                    self.choice = ('join', room_info)
                    return True

            elif event.key == pygame.K_ESCAPE:
                self.choice = ('back', None)
                return True

        return False

    def draw(self, screen):
        """Desenha a tela de lobby."""
        screen.fill(self.bg_color)

        # Título
        title_text = self.title_font.render("SALAS DISPONÍVEIS", True, self.title_color)
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 80))
        screen.blit(title_text, title_rect)

        # Informação de escaneamento
        scan_text = self.small_font.render(
            f"Salas encontradas: {len(self.room_list)} | Escaneando...",
            True, (150, 150, 150)
        )
        scan_rect = scan_text.get_rect(center=(self.screen_width // 2, 140))
        screen.blit(scan_text, scan_rect)

        # Lista de salas
        y_start = 200
        y_spacing = 60

        for i, room_name in enumerate(self.room_list):
            color = self.selected_color if i == self.selected_index else self.normal_color
            text = self.option_font.render(room_name, True, color)
            rect = text.get_rect(center=(self.screen_width // 2, y_start + i * y_spacing))

            if i == self.selected_index:
                arrow = self.option_font.render(">", True, self.selected_color)
                arrow_rect = arrow.get_rect(right=rect.left - 20, centery=rect.centery)
                screen.blit(arrow, arrow_rect)

            screen.blit(text, rect)

        # Opção "Criar Nova Sala"
        create_index = len(self.room_list)
        color = self.selected_color if self.selected_index == create_index else self.normal_color
        create_text = self.option_font.render(self.create_room_option, True, color)
        create_rect = create_text.get_rect(
            center=(self.screen_width // 2, y_start + create_index * y_spacing + 40)
        )
        if self.selected_index == create_index:
            arrow = self.option_font.render(">", True, self.selected_color)
            arrow_rect = arrow.get_rect(right=create_rect.left - 20, centery=create_rect.centery)
            screen.blit(arrow, arrow_rect)
        screen.blit(create_text, create_rect)

        # Opção "Voltar"
        back_index = len(self.room_list) + 1
        color = self.selected_color if self.selected_index == back_index else self.normal_color
        back_text = self.option_font.render("Voltar ao Menu", True, color)
        back_rect = back_text.get_rect(
            center=(self.screen_width // 2, y_start + back_index * y_spacing + 40)
        )
        if self.selected_index == back_index:
            arrow = self.option_font.render(">", True, self.selected_color)
            arrow_rect = arrow.get_rect(right=back_rect.left - 20, centery=back_rect.centery)
            screen.blit(arrow, arrow_rect)
        screen.blit(back_text, back_rect)

        # Instruções
        hint_text = self.small_font.render(
            "SETAS: Navegar | ENTER: Selecionar | ESC: Voltar",
            True, (150, 150, 150)
        )
        hint_rect = hint_text.get_rect(center=(self.screen_width // 2, self.screen_height - 50))
        screen.blit(hint_text, hint_rect)

    def get_choice(self):
        """Retorna a escolha do usuário e reseta."""
        choice = self.choice
        self.choice = None
        return choice

    def cleanup(self):
        """Limpa recursos ao sair da cena."""
        # Para o flag de escaneamento primeiro
        self.scanning = False

        # Fecha o socket (isso fará a thread sair do recvfrom)
        if self.udp_socket:
            try:
                self.udp_socket.close()
            except:
                pass
            self.udp_socket = None

        # Aguarda a thread terminar
        if self.scan_thread and self.scan_thread.is_alive():
            self.scan_thread.join(timeout=1.0)
