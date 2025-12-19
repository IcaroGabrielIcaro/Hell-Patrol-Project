import socket
import threading
from rooms.room import Room
from core.client_handler import handle_client

class GameServer:
    def __init__(self, host, port):
        self.room = Room()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()

    def start(self):
        print("Servidor rodando...")
        while True:
            conn, addr = self.server.accept()
            threading.Thread(
                target=handle_client,
                args=(conn, addr, self.room),
                daemon=True
            ).start()
