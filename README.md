# Hell-Patrol-Project

Jogo para a atividade de socket da matéria de Desenvolvimento de Sistemas Distribuídos

## 🎮 Sistema Multiplayer

O jogo agora possui um **sistema de rede multiplayer completo** com:

- ✅ **TCP para comunicação** (mantém padrão original do projeto)
- ✅ **Descoberta automática de salas** via broadcast UDP
- ✅ **Menu com navegação por teclado** (setas + Enter)
- ✅ **Suporte a singleplayer e multiplayer**
- ✅ **Compatível com código original** (não quebra implementação existente)

## 📚 Documentação Completa

**👉 [Índice da Documentação (DOC_INDEX.md)](hell-patrol/DOC_INDEX.md)** - Navegue por toda a documentação

### Guias Principais

- **[OVERVIEW.md](hell-patrol/OVERVIEW.md)** - **COMECE AQUI** - Visão geral completa
- **[MULTIPLAYER_README.md](hell-patrol/MULTIPLAYER_README.md)** - Guia de uso completo
- **[USAGE_EXAMPLES.md](hell-patrol/USAGE_EXAMPLES.md)** - Exemplos práticos e troubleshooting
- **[NETWORK_FLOW.md](hell-patrol/NETWORK_FLOW.md)** - Diagramas técnicos e fluxo de rede
- **[IMPLEMENTATION_SUMMARY.md](hell-patrol/IMPLEMENTATION_SUMMARY.md)** - Sumário técnico detalhado

### 🚀 Como Executar

#### Cliente com Menu Multiplayer (Recomendado)
```bash
cd hell-patrol
./run_client.sh
# ou
python client/main_multiplayer.py
```

#### Servidor Dedicado (Opcional)
```bash
cd hell-patrol
./run_server.sh
# ou
python server/main.py
```

#### Validar Sistema
```bash
cd hell-patrol
./validate_system.sh
```

### 🎯 Fluxo de Uso

1. **Menu Principal**: Escolha entre Jogar Sozinho, Entrar em Sala ou Sair
2. **Descoberta de Salas**: Veja salas abertas na rede local automaticamente
3. **Criar ou Entrar**: Crie sua própria sala ou conecte-se a uma existente
4. **Gameplay**: Jogue com outros jogadores em tempo real

### 🔧 Arquitetura Técnica

```
┌──────────────────────────────────────────────────────────────┐
│  DESCOBERTA (UDP Broadcast) - Porta 12345                   │
│  Servidor anuncia sala → Clientes detectam automaticamente  │
└──────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────┐
│  CONEXÃO E GAMEPLAY (TCP) - Porta 5555                      │
│  Cliente conecta → Recebe player_id → Envia input/estado    │
│  (Mantém padrão TCP original do projeto)                    │
└──────────────────────────────────────────────────────────────┘
```

### 📦 Novos Arquivos

```
hell-patrol/
├── client/
│   ├── main_multiplayer.py         # Novo ponto de entrada com menu
│   ├── core/
│   │   └── network_manager.py      # Cliente TCP+UDP
│   └── scenes/
│       ├── menu.py                 # Menu principal
│       └── lobby.py                # Descoberta de salas
├── server/
│   └── core/ (compatível com original)
│   └── scenes/
│       ├── menu.py                 # Menu principal
│       └── lobby.py                # Descoberta de salas
├── server/
│   ├── main.py                     # Atualizado com discovery
│   └── core/
│       └── discovery.py            # Serviço de descoberta UDP
└── docs/
    ├── DOC_INDEX.md                # Índice de toda documentação
    ├── OVERVIEW.md                 # Visão geral (COMECE AQUI)
    ├── MULTIPLAYER_README.md       # Guia completo
    ├── NETWORK_FLOW.md             # Diagramas técnicos
    ├── USAGE_EXAMPLES.md           # Exemplos práticos
    └── IMPLEMENTATION_SUMMARY.md   # Sumário técnico
```

### 🌐 Requisitos de Rede

- **Rede Local**: Todos os dispositivos devem estar na mesma rede
- **Portas**:
  - 12345 (UDP) -Conexão e gandshake inicial
  - 5556 (UDP) - Gameplay
- **Firewall**: Certifique-se de que as portas estão abertas

### 🎨 Controles

**Menu/Lobby:**
- Setas ↑/↓: Navegar
- Enter: Selecionar
- ESC: Voltar

**Gameplay:**
- WASD: Movimentação
- Mouse: Mira
- Botão Esquerdo: Atirar
- R: Recarregar
- ESC: Voltar ao menu

### 🧪 Testes

Execute os testes automatizados para validar o sistema:

```bash
cd hell-patrol
python test_network.py
```

Testes incluem:
- ✓ JSON Serialization
- ✓ Local IP Detection
- ✓ UDP Broadcast
- ✓ TCP Connection
- ✓ UDP Communication

### 🎓 Para Demonstração

**Setup rápido com 2 computadores:**

**Computador 1 (Host)**:
```bash
cd hell-patrol
./run_client.sh
# Selecionar "Entrar em Sala" → "Criar Nova Sala"
```

**Computador 2 (Cliente)**:
```bash
cd hell-patrol
./run_client.sh
# Selecionar "Entrar em Sala" → Selecionar sala do IP do Computador 1
```

---

**Desenvolvido para a disciplina de Sistemas Distribuídos**


