#!/usr/bin/env python3
"""
Script de teste rápido para validar componentes do sistema multiplayer.
Execute este script para verificar se tudo está funcionando corretamente.
"""

import sys
import socket
import json
import time
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent))

def test_udp_broadcast():
    """Testa envio e recepção de broadcast UDP."""
    print("\n[TEST 1] Testando UDP Broadcast...")

    try:
        # Cria socket de broadcast
        send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        send_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        # Cria socket de recepção
        recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        recv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        recv_socket.bind(('', 12345))
        recv_socket.settimeout(2.0)

        # Envia broadcast
        message = {"type": "test_broadcast", "data": "hello"}
        send_socket.sendto(json.dumps(message).encode(), ('<broadcast>', 12345))
        print("  ✓ Broadcast enviado")

        # Tenta receber
        data, addr = recv_socket.recvfrom(1024)
        received = json.loads(data.decode())

        if received.get('type') == 'test_broadcast':
            print(f"  ✓ Broadcast recebido de {addr}")
            print("  ✓ UDP Broadcast: OK")
            return True
        else:
            print("  ✗ Mensagem incorreta recebida")
            return False

    except socket.timeout:
        print("  ✗ Timeout ao receber broadcast")
        return False
    except Exception as e:
        print(f"  ✗ Erro: {e}")
        return False
    finally:
        send_socket.close()
        recv_socket.close()


def test_tcp_connection():
    """Testa criação de servidor TCP e conexão."""
    print("\n[TEST 2] Testando TCP Connection...")

    import threading

    server_ready = threading.Event()
    connection_success = [False]

    def tcp_server():
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind(('127.0.0.1', 15555))
            server.listen(1)
            server.settimeout(3.0)
            server_ready.set()

            conn, addr = server.accept()
            data = conn.recv(1024).decode()
            message = json.loads(data)

            if message.get('type') == 'test_handshake':
                response = {"type": "test_ok", "status": "success"}
                conn.sendall(json.dumps(response).encode())
                connection_success[0] = True

            conn.close()
            server.close()
        except Exception as e:
            print(f"  ✗ Erro no servidor: {e}")

    # Inicia servidor em thread
    server_thread = threading.Thread(target=tcp_server, daemon=True)
    server_thread.start()

    # Aguarda servidor estar pronto
    if not server_ready.wait(timeout=2.0):
        print("  ✗ Servidor não iniciou a tempo")
        return False

    time.sleep(0.1)

    try:
        # Cliente conecta
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(2.0)
        client.connect(('127.0.0.1', 15555))
        print("  ✓ Conexão TCP estabelecida")

        # Envia mensagem
        message = {"type": "test_handshake"}
        client.sendall(json.dumps(message).encode())
        print("  ✓ Mensagem enviada")

        # Recebe resposta
        data = client.recv(1024).decode()
        response = json.loads(data)

        if response.get('type') == 'test_ok':
            print("  ✓ Resposta recebida")
            print("  ✓ TCP Connection: OK")
            client.close()
            return True
        else:
            print("  ✗ Resposta incorreta")
            return False

    except Exception as e:
        print(f"  ✗ Erro no cliente: {e}")
        return False


def test_udp_communication():
    """Testa comunicação UDP bidirecional."""
    print("\n[TEST 3] Testando UDP Communication...")

    import threading

    server_ready = threading.Event()
    test_success = [False]

    def udp_server():
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            server.bind(('127.0.0.1', 15556))
            server.settimeout(3.0)
            server_ready.set()

            # Recebe mensagem do cliente
            data, addr = server.recvfrom(1024)
            message = json.loads(data.decode())

            if message.get('type') == 'test_udp':
                # Responde ao cliente
                response = {"type": "test_response", "status": "ok"}
                server.sendto(json.dumps(response).encode(), addr)
                test_success[0] = True

            server.close()
        except Exception as e:
            print(f"  ✗ Erro no servidor UDP: {e}")

    # Inicia servidor
    server_thread = threading.Thread(target=udp_server, daemon=True)
    server_thread.start()

    if not server_ready.wait(timeout=2.0):
        print("  ✗ Servidor UDP não iniciou")
        return False

    time.sleep(0.1)

    try:
        # Cliente envia mensagem
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client.settimeout(2.0)

        message = {"type": "test_udp", "data": "hello"}
        client.sendto(json.dumps(message).encode(), ('127.0.0.1', 15556))
        print("  ✓ Mensagem UDP enviada")

        # Recebe resposta
        data, addr = client.recvfrom(1024)
        response = json.loads(data.decode())

        if response.get('type') == 'test_response':
            print("  ✓ Resposta UDP recebida")
            print("  ✓ UDP Communication: OK")
            client.close()
            return True
        else:
            print("  ✗ Resposta incorreta")
            return False

    except Exception as e:
        print(f"  ✗ Erro no cliente UDP: {e}")
        return False


def test_json_serialization():
    """Testa serialização de mensagens JSON."""
    print("\n[TEST 4] Testando JSON Serialization...")

    try:
        # Testa mensagem simples
        msg1 = {"type": "move", "dx": 1, "dy": 0, "angle": 45.5}
        serialized = json.dumps(msg1)
        deserialized = json.loads(serialized)

        if msg1 == deserialized:
            print("  ✓ Mensagem simples: OK")
        else:
            print("  ✗ Mensagem simples: FALHOU")
            return False

        # Testa mensagem complexa
        msg2 = {
            "type": "state",
            "players": {
                "p1": {"x": 100, "y": 200, "angle": 0},
                "p2": {"x": 300, "y": 400, "angle": 90}
            },
            "enemies": [{"x": 500, "y": 600}]
        }
        serialized = json.dumps(msg2)
        deserialized = json.loads(serialized)

        if msg2 == deserialized:
            print("  ✓ Mensagem complexa: OK")
        else:
            print("  ✗ Mensagem complexa: FALHOU")
            return False

        print("  ✓ JSON Serialization: OK")
        return True

    except Exception as e:
        print(f"  ✗ Erro: {e}")
        return False


def test_local_ip_detection():
    """Testa detecção de IP local."""
    print("\n[TEST 5] Testando Local IP Detection...")

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()

        print(f"  ✓ IP Local detectado: {local_ip}")

        # Valida formato do IP
        parts = local_ip.split('.')
        if len(parts) == 4 and all(p.isdigit() and 0 <= int(p) <= 255 for p in parts):
            print("  ✓ Local IP Detection: OK")
            return True
        else:
            print("  ✗ IP inválido detectado")
            return False

    except Exception as e:
        print(f"  ✗ Erro: {e}")
        return False


def main():
    """Executa todos os testes."""
    print("="*60)
    print("  HELL PATROL - TESTE DE COMPONENTES MULTIPLAYER")
    print("="*60)

    results = []

    # Executa testes
    results.append(("JSON Serialization", test_json_serialization()))
    results.append(("Local IP Detection", test_local_ip_detection()))
    results.append(("UDP Broadcast", test_udp_broadcast()))
    results.append(("TCP Connection", test_tcp_connection()))
    results.append(("UDP Communication", test_udp_communication()))

    # Sumário
    print("\n" + "="*60)
    print("  SUMÁRIO DOS TESTES")
    print("="*60)

    for test_name, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{test_name:.<40} {status}")

    total = len(results)
    passed = sum(1 for _, s in results if s)

    print("="*60)
    print(f"  Resultado: {passed}/{total} testes passaram")
    print("="*60)

    if passed == total:
        print("\n✓ Todos os testes passaram! Sistema pronto para uso.")
        return 0
    else:
        print(f"\n✗ {total - passed} teste(s) falharam. Verifique os logs acima.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
