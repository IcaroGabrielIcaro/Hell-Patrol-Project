import time
import socket
import threading
import json
from server.rooms.room import Room
from server.core.client_handler import handle_client

class GameServer:
    def __init__(self, host, port):
        self.room = Room()
        self.host = host
        self.port = port

        # TCP: handshake inicial
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.bind((host, port))
        self.tcp_socket.listen()

        # UDP: gameplay em tempo real
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.bind((host, port))

        # Mapa de endereços UDP dos clientes: {player_id: (ip, port)}
        self.client_addrs = {}

        self.running = True

    def start(self):
        print("Servidor rodando...")

        # Thread para game loop
        threading.Thread(
            target=self.game_loop,
            daemon=True
        ).start()

        # Thread para UDP listener (gameplay)
        threading.Thread(
            target=self.udp_loop,
            daemon=True
        ).start()

        # Loop principal: aceita conexões TCP (handshake)
        while True:
            conn, addr = self.tcp_socket.accept()
            threading.Thread(
                target=handle_client,
                args=(conn, addr, self.room, self),
                daemon=True
            ).start()

    def udp_loop(self):
        """Recebe ações dos clientes via UDP e envia estado de volta"""
        print("[UDP] Listener iniciado")

        while self.running:
            try:
                data, client_addr = self.udp_socket.recvfrom(1024)
                msg = json.loads(data.decode())

                # Identifica o player pelo endereço UDP
                player_id = None
                for pid, addr in self.client_addrs.items():
                    if addr == client_addr:
                        player_id = pid
                        break

                # Se não encontrou, pode ser primeira mensagem UDP - registra
                if not player_id and "player_id" in msg:
                    player_id = msg["player_id"]
                    self.client_addrs[player_id] = client_addr
                    print(f"[UDP] Cliente {player_id} registrado em {client_addr}")

                if player_id:
                    # Processa ação do jogador
                    self.room.handle_action(player_id, msg)

                    # Envia estado atualizado via UDP
                    state = self.room.get_state()
                    state_msg = {"action": "state", **state}
                    self.udp_socket.sendto(
                        json.dumps(state_msg).encode(),
                        client_addr
                    )

            except Exception as e:
                if self.running:
                    print(f"[UDP] Erro: {e}")

    def game_loop(self):
        last_time = time.perf_counter()

        while self.running:
            now = time.perf_counter()
            dt = now - last_time
            last_time = now

            dt = min(dt, 0.05)  # segurança

            self.room.update(dt)

            time.sleep(1 / 60)  # tick fixo (60hz)
