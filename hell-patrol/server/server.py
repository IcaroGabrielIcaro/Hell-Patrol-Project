import socket
import threading
import json

HOST = 'localhost'
PORT = 5555

rooms = {
    "sala1": {}
}

def handle_client(conn, addr):
    print(f"Conectado: {addr}")

    player_id = str(addr)
    room = "sala1"

    rooms[room][player_id] = {"x": 100, "y": 100}

    try:
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break

            msg = json.loads(data)

            if msg["action"] == "move":
                rooms[room][player_id]["x"] += msg["dx"] * 5
                rooms[room][player_id]["y"] += msg["dy"] * 5

            response = {
                "players": rooms[room]
            }

            conn.sendall(json.dumps(response).encode())

    except Exception as e:
        print(e)

    del rooms[room][player_id]
    conn.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("Servidor rodando...")

while True:
    conn, addr = server.accept()
    threading.Thread(target=handle_client, args=(conn, addr)).start()
