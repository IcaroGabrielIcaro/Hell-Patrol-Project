import socket
import json

class NetworkClient:
    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        self.buffer = ""

        self.player_id = None  # 🔥 guarda o id do player local

        # recebe mensagem inicial do servidor
        init_msg = self.receive()
        if init_msg.get("action") == "init":
            self.player_id = init_msg["player_id"]
            print(f"[NETWORK] Player ID recebido: {self.player_id}")

    def send(self, data):
        self.socket.sendall((json.dumps(data) + "\n").encode())

    def receive(self):
        while "\n" not in self.buffer:
            data = self.socket.recv(4096).decode()
            if not data:
                raise ConnectionError("Conex\u00e3o fechada")
            self.buffer += data

        line, self.buffer = self.buffer.split("\n", 1)
        return json.loads(line)

    def close(self):
        self.socket.close()
