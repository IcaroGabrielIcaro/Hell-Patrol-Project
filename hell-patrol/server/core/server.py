import socket
import threading
import time
from server.rooms.room import Room
from server.core.client_handler import handle_client

class GameServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.room = Room()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()
        self.running = True

    def start(self):
        threading.Thread(target=self.accept_clients, daemon=True).start()
        threading.Thread(target=self.display_status, daemon=True).start()

        print(f"Servidor iniciado em: {self.host}:{self.port}! Pressione Ctrl+C para parar.")
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nServidor encerrado.")
            self.running = False
            self.server.close()

    def accept_clients(self):
        while self.running:
            try:
                conn, addr = self.server.accept()
                threading.Thread(
                    target=handle_client,
                    args=(conn, addr, self.room),
                    daemon=True
                ).start()
            except OSError:
                break

    def display_status(self):
        while self.running:
            time.sleep(30)
            num_players = len(self.room.players)
            print(f"[STATUS] Jogadores conectados: {num_players}")
