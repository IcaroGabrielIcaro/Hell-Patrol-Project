"""
Servidor para Hell Patrol.
Mantém compatibilidade com código original + adiciona discovery de salas.
"""
from server.config import *
from server.core.server import GameServer
from server.core.discovery import RoomDiscovery, get_local_ip


if __name__ == "__main__":
    # Detecta IP local
    local_ip = get_local_ip()

    print(f"[MAIN] Iniciando servidor Hell Patrol...")
    print(f"[MAIN] IP Local: {local_ip}")
    print(f"[MAIN] Porta: {PORT}")

    # Cria e inicia servidor principal (código original)
    server = GameServer(HOST, PORT)

    # Adiciona serviço de descoberta (passa referência da room para verificar jogadores)
    discovery = RoomDiscovery(local_ip, PORT, server.room)
    discovery.start()

    print(f"[MAIN] Servidor rodando em {local_ip}:{PORT}")
    print(f"[MAIN] Sala só aparecerá no lobby com 2+ jogadores")
    print(f"[MAIN] Pressione Ctrl+C para parar")

    try:
        server.start()
    except KeyboardInterrupt:
        print("\n[MAIN] Parando servidor...")
        discovery.stop()
