"""
Servidor de descoberta de salas via UDP broadcast.
Complementa o GameServer original sem modificá-lo.
"""
import socket
import threading
import json
import time


class RoomDiscovery:
    """
    Serviço de descoberta de salas via UDP broadcast.
    Roda em paralelo ao GameServer principal.
    Só anuncia quando há jogadores conectados.
    """

    DISCOVERY_PORT = 12345

    def __init__(self, server_host, server_port, room):
        self.server_host = server_host
        self.server_port = server_port
        self.room = room  # Referência à Room para verificar jogadores
        self.running = False
        self.broadcast_socket = None

    def start(self):
        """Inicia broadcast de anúncio da sala."""
        self.running = True
        self.broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        threading.Thread(target=self._broadcast_loop, daemon=True).start()
        print(f"[DISCOVERY] Anunciando sala em broadcast (porta {self.DISCOVERY_PORT})")

    def _broadcast_loop(self):
        """Loop de broadcast periódico - só anuncia se houver jogadores."""
        while self.running:
            try:
                # Só anuncia se houver pelo menos 1 jogador conectado
                player_count = len(self.room.players)

                if player_count >= 1:
                    message = {
                        'type': 'room_announcement',
                        'host': self.server_host,
                        'port': self.server_port,
                        'players': player_count
                    }
                    data = json.dumps(message).encode('utf-8')
                    self.broadcast_socket.sendto(data, ('<broadcast>', self.DISCOVERY_PORT))
            except Exception as e:
                if self.running:
                    print(f"[DISCOVERY] Erro ao enviar broadcast: {e}")

            time.sleep(2.0)  # Verifica a cada 2 segundos

    def stop(self):
        """Para o serviço de descoberta."""
        self.running = False
        if self.broadcast_socket:
            self.broadcast_socket.close()
        print("[DISCOVERY] Serviço de descoberta parado")


def get_local_ip():
    """
    Detecta o IP local da máquina.
    Útil para exibir ao usuário qual IP usar para conectar.
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        print(f"[DISCOVERY] Erro ao detectar IP local: {e}")
        return "127.0.0.1"
