# Mesclagem de Funcionalidades - Hell Patrol

## Resumo das Mudanças

Esta documentação descreve as funcionalidades mescladas da implementação `hell-patrol-icaro` para `hell-patrol`.

## Funcionalidades Adicionadas

### 1. Sistema de Tiro e Munição
- **Projéteis**: Adicionada classe `Projectile` (cliente e servidor)
- **Munição**: Sistema com 10 balas, cooldown de 0.35s entre tiros
- **Recarga**: Sistema de recarga com botão esquerdo do mouse
- **Atirar**: Botão direito do mouse para disparar

### 2. Sistema de Sprites Animados
- **Player animado**: Sprites de cabeça e corpo separados com animação de caminhada
- **Arma visual**: Shotgun renderizada com o jogador
- **Rotação**: Player rotaciona seguindo a posição do mouse
- **Escala configurável**: Player renderizado em 2.7x (configurável)

### 3. Sistema de Mira
- **Crosshair**: Mira customizada que segue o mouse
- **Estado visual**: Mira muda quando munição acaba
- **Mouse invisível**: Cursor padrão do sistema oculto

### 4. Melhorias no Protocolo
- **Ângulo de rotação**: Adicionado ao movimento do player
- **Ações de tiro**: `ACTION_SHOOT` e `ACTION_RELOAD`
- **Estado de recarga**: Servidor notifica cliente quando recarga completa

### 5. Melhorias na Camera
- **apply_pos()**: Novo método para aplicar offset da câmera em posições (x, y)
- Necessário para renderizar projéteis corretamente

## Arquivos Modificados

### Cliente (`hell-patrol/client/`)
- `main.py` - Inicialização com pygame.init() e carregamento da mira
- `core/game.py` - Loop principal com sistema de tiro e rotação
- `core/camera.py` - Adicionado método `apply_pos()`
- `entities/player.py` - Player com sprites animados e arma
- `entities/projectile.py` - Nova classe para projéteis
- `scenes/gameplay.py` - Suporte a projéteis e animações

### Servidor (`hell-patrol/server/`)
- `entities/player.py` - Lógica de tiro, munição e recarga
- `entities/projectile.py` - Nova classe para projéteis do servidor
- `rooms/room.py` - Gerenciamento de projéteis e ações de tiro

### Compartilhado (`hell-patrol/shared/`)
- `protocol.py` - Novos tipos de ação e funções para tiro/recarga

## Assets Copiados

Estrutura de sprites copiada de `hell-patrol-icaro`:

```
client/assets/sprites/
├── player/
│   └── centralizado/
│       ├── cabeca/          # 3 frames de animação da cabeça
│       └── corpo/           # 3 frames de animação do corpo
├── arma/
│   └── shotgun-1.png       # Sprite da shotgun
├── mira/
│   ├── crosshairSquare.png        # Mira normal
│   └── crosshairSquare-empty.png  # Mira vazia
└── tiros/
    └── quadrado/           # Sprites de projétil
```

## Controles

- **WASD**: Movimento do jogador
- **Mouse**: Rotação do jogador
- **Botão Direito**: Atirar (quando há munição)
- **Botão Esquerdo**: Recarregar (quando munição = 0)

## Configurações Ajustáveis

### Cliente
- `CROSSHAIR_SCALE = 2.3` em `main.py` - Tamanho da mira
- `scale=2.7` em `gameplay.py` - Tamanho do player
- `anim_speed=0.12` em `gameplay.py` - Velocidade da animação
- `shoot_cooldown = 0.35` em `game.py` - Tempo entre tiros
- `max_ammo = 10` em `game.py` - Munição máxima

### Servidor
- `SPEED = 1000` em `entities/player.py` - Velocidade do jogador
- `MAX_AMMO = 10` em `entities/player.py` - Munição máxima
- `FIRE_COOLDOWN = 0.28` em `entities/player.py` - Cooldown de tiro
- `SPEED = 1400` em `entities/projectile.py` - Velocidade do projétil
- `MAX_DISTANCE = 900` em `entities/projectile.py` - Alcance máximo

## Compatibilidade

✅ Mantida a estrutura e organização original de `hell-patrol`
✅ Documentação em português seguindo o padrão
✅ Fallbacks para quando sprites não existem
✅ Retrocompatível com código anterior (parâmetro `size` mantido em Player)

## Próximos Passos Sugeridos

1. Adicionar colisão de projéteis com inimigos
2. Implementar sistema de dano
3. Adicionar efeitos sonoros para tiro
4. Criar HUD para mostrar munição na tela
5. Adicionar mais tipos de armas
6. Implementar sistema de reload automático

## Testes Recomendados

1. Iniciar o servidor: `python -m server.main`
2. Iniciar o cliente: `python -m client.main`
3. Testar movimento com WASD
4. Testar rotação com mouse
5. Testar tiro com botão direito
6. Testar recarga com botão esquerdo
7. Verificar animações do player
8. Verificar que projéteis aparecem e se movem
