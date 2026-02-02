import json
from shared.protocol import make_init, make_state

def handle_client(conn, addr, room):
    player_id = str(addr)
    room.add_player(player_id)

    conn.sendall((json.dumps(make_init(player_id)) + "\n").encode())

    try:
        buffer = ""
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break

            buffer += data
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                if line:
                    msg = json.loads(line)
                    room.handle_action(player_id, msg)

            conn.sendall((json.dumps(make_state(room.get_state())) + "\n").encode())

    except Exception as e:
        print(e)

    room.remove_player(player_id)
    conn.close()
