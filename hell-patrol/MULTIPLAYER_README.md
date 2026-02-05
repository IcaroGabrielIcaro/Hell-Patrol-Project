# Hell Patrol - Sistema Multiplayer

Sistema de rede multiplayer com **TCP para comunicação** e **UDP para descoberta de salas**.

## 🎮 Características

- **Menu Principal** com navegação por setas (↑/↓) e Enter para selecionar
- **Descoberta Automática de Salas** via UDP broadcast na rede local
- **Três Modos de Jogo**:
  - Jogar Sozinho (conecta ao servidor local)
  - Entrar em Sala (conecta a sala existente)
  - Criar Nova Sala (inicia servidor próprio)

## 🚀 Como Usar

### 1. Iniciar Servidor (Necessário)

```bash
cd hell-patrol
python -m server.main
```

O servidor irá:
- Escutar conexões TCP na porta 5555
- Fazer broadcast UDP na porta 12345 anunciando a sala

### 2. Iniciar Cliente

```bash
python -m client.main
```

### Menu - Opções:

**Jogar Sozinho**
- Conecta ao servidor local (localhost:5555)
- Requer servidor rodando

**Entrar em Sala**
- Abre lobby com detecção automática de salas na rede
- Selecione uma sala disponível e pressione Enter
- Ou pressione ESC para voltar ao menu

**Criar Nova Sala** (via lobby)
- No lobby, selecione ">> Criar Nova Sala <<"
- Conecta ao servidor local configurado

**Sair**
- Fecha o jogo

## 🔧 Arquitetura

### Protocolo de Comunicação

1. **Discovery de Salas (UDP Broadcast)**:
   - Porta: `12345`
   - Servidores anunciam presença a cada 2 segundos
   - Clientes escaneiam continuamente

2. **Gameplay (TCP)**:
   - Porta: `5555` (padrão)
   - Conexão TCP persistente com buffer de newline
   - Cliente envia: movimentos, ações, tiros
   - Servidor envia: estado completo do jogo
   - Formato: JSON + `\n` delimiter

### Estrutura de Arquivos

```
client/
  ├── main.py                      # Ponto de entrada único
  ├── core/
  │   ├── application.py           # GameApplication (menu + lobby + gameplay)
  │   ├── network.py               # NetworkClient TCP original
  │   └── game.py                  # Game loop
  └── scenes/
      ├── menu.py                  # Menu principal
      ├── lobby.py                 # Descoberta de salas
      └── gameplay.py              # Gameplay scene

server/
  ├── main.py                      # Ponto de entrada simples
  ├── core/
  │   ├── server.py                # GameServer TCP original
  │   └── discovery.py             # RoomDiscovery UDP broadcast
  └── rooms/
      └── room.py                  # Room management
```

## 🎯 Controles

### Menu e Lobby
- **Setas ↑/↓**: Navegar
- **Enter**: Selecionar
- **ESC**: Voltar (no lobby)

### Gameplay
- **WASD**: Movimentação
- **Mouse**: Mira
- **Botão Esquerdo**: Atirar
- **R**: Recarregar
- **ESC**: Voltar ao menu

## 🌐 Configuração de Rede

### Portas Utilizadas
- **5555**: TCP (gameplay, configurável em config.py)
- **12345**: UDP (discovery broadcast)

### Firewall
Certifique-se de que as portas estão abertas na rede local.

## 🐛 Solução de Problemas

### "Erro ao iniciar jogo"
- **Causa**: Servidor não está rodando
- **Solução**: Execute `python -m server.main` primeiro

### Salas não aparecem no lobby
- Verifique se está na mesma rede local
- Aguarde alguns segundos (broadcast a cada 2s)
- Confirme porta 12345 UDP não está bloqueada

### Conexão recusada
- Servidor precisa estar rodando primeiro
- Verifique porta 5555 TCP disponível
- Confirme firewall não está bloqueando

## 📝 Padrão do Projeto

O sistema **mantém 100% de compatibilidade** com o código original:

✅ TCP com buffer de newline (`\n`)
✅ `client/main.py` minimalista (apenas chama `GameApplication`)
✅ Toda lógica em módulos separados
✅ Servidor original `GameServer` não modificado
✅ NetworkClient compatível com interface original

## 🎨 Estrutura Modular

- **Menu**: `client/scenes/menu.py`
- **Lobby**: `client/scenes/lobby.py`
- **Aplicação**: `client/core/application.py`
- **Discovery**: `server/core/discovery.py`

---

**Sistema multiplayer para Hell Patrol Project**
