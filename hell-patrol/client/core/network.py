import socket
import json

class NetworkClient:
    def __init__(self, host, port):
        # TCP: apenas handshake inicial
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.connect((host, port))
        self.buffer = ""

        # UDP: gameplay em tempo real
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_addr = (host, port)

        self.host = host
        self.port = port
        self.player_id = None
        self.udp_port = None  # porta UDP atribuída pelo servidor

        # recebe mensagem inicial do servidor (via TCP)
        init_msg = self.receive_tcp()
        if init_msg.get("action") == "init":
            self.player_id = init_msg["player_id"]
            self.udp_port = init_msg.get("udp_port", port)  # servidor informa porta UDP
            self.server_addr = (host, self.udp_port)
            print(f"[NETWORK] Player ID: {self.player_id}, UDP Port: {self.udp_port}")

    def send(self, data):
        """Envia dados via UDP (gameplay em tempo real)"""
        message = json.dumps(data).encode()
        self.udp_socket.sendto(message, self.server_addr)

    def send_tcp(self, data):
        """Envia dados via TCP (mensagens críticas)"""
        self.tcp_socket.sendall((json.dumps(data) + "\n").encode())

    def receive(self):
        """Recebe estado do jogo via UDP"""
        try:
            self.udp_socket.settimeout(0.1)  # timeout rápido
            data, _ = self.udp_socket.recvfrom(4096)
            return json.loads(data.decode())
        except socket.timeout:
            return {"action": "state", "players": {}, "projectiles": []}
        except Exception as e:
            print(f"[NETWORK] Erro UDP receive: {e}")
            return {"action": "state", "players": {}, "projectiles": []}

    def receive_tcp(self):
        """Recebe dados via TCP (handshake, mensagens críticas)"""
        while "\n" not in self.buffer:
            data = self.tcp_socket.recv(4096).decode()
            if not data:
                raise ConnectionError("Conexão fechada")
            self.buffer += data

        line, self.buffer = self.buffer.split("\n", 1)
        return json.loads(line)

    def close(self):
        self.udp_socket.close()
        self.tcp_socket.close()
