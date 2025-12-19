import json

def handle_client(conn, addr, room):
    player_id = str(addr)
    room.add_player(player_id)

    conn.sendall(json.dumps({
        "action": "init",
        "player_id": player_id
    }).encode())

    try:
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break

            msg = json.loads(data)
            room.handle_action(player_id, msg)

            conn.sendall(json.dumps(room.get_state()).encode())

    except Exception as e:
        print(e)

    room.remove_player(player_id)
    conn.close()
