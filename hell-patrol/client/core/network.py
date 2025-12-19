import socket
import json

class NetworkClient:
    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))

        self.player_id = None  # 🔥 guarda o id do player local

        # recebe mensagem inicial do servidor
        init_msg = self.receive()
        if init_msg.get("action") == "init":
            self.player_id = init_msg["player_id"]
            print(f"[NETWORK] Player ID recebido: {self.player_id}")

    def send(self, data):
        self.socket.sendall(json.dumps(data).encode())

    def receive(self):
        data = self.socket.recv(4096).decode()
        return json.loads(data)

    def close(self):
        self.socket.close()
