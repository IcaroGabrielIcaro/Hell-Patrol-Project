import socket
import json

class NetworkClient:
    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))

    def send(self, data):
        self.socket.sendall(json.dumps(data).encode())

    def receive(self):
        data = self.socket.recv(4096).decode()
        return json.loads(data)

    def close(self):
        self.socket.close()
