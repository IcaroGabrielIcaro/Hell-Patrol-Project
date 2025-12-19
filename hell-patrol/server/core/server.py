import time
import socket
import threading
from server.rooms.room import Room
from server.core.client_handler import handle_client

class GameServer:
    def __init__(self, host, port):
        self.room = Room()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()
        self.running = True

    def start(self):
        print("Servidor rodando...")

        threading.Thread(
            target=self.game_loop,
            daemon=True
        ).start()

        while True:
            conn, addr = self.server.accept()
            threading.Thread(
                target=handle_client,
                args=(conn, addr, self.room),
                daemon=True
            ).start()

    def game_loop(self):
        last_time = time.perf_counter()

        while self.running:
            now = time.perf_counter()
            dt = now - last_time
            last_time = now

            dt = min(dt, 0.05)  # segurança

            self.room.update(dt)

            time.sleep(1 / 60)  # tick fixo (60hz)