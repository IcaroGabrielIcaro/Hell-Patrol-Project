import json
from shared.protocol import make_init, make_state

def handle_client(conn, addr, room, server):
    """
    Gerencia handshake TCP inicial.
    Após handshake, o gameplay usa UDP.
    """
    player_id = str(addr)
    room.add_player(player_id)

    # Envia mensagem inicial via TCP
    init_response = make_init(player_id)
    init_response["udp_port"] = server.port  # informa porta UDP
    conn.sendall((json.dumps(init_response) + "\n").encode())

    print(f"[TCP] Cliente {player_id} conectado - handshake completo")

    try:
        # Mantém conexão TCP aberta para mensagens críticas (futuro)
        # Por enquanto, apenas aguarda desconexão
        buffer = ""
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break

            # Pode processar mensagens TCP críticas aqui se necessário
            buffer += data

    except Exception as e:
        print(f"[CLIENT_HANDLER] Erro com {player_id}: {e}")

    # Cliente desconectou
    room.remove_player(player_id)

    # Remove endereço UDP do mapa
    if player_id in server.client_addrs:
        del server.client_addrs[player_id]

    conn.close()
    print(f"[TCP] Cliente {player_id} desconectado")
