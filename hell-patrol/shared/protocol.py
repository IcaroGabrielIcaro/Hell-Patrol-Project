"""
Define o protocolo de comunicação entre cliente e servidor.
"""

# Tipos de ações
ACTION_MOVE = "move"
ACTION_INIT = "init"
ACTION_STATE = "state"

# Mensagens do cliente

def make_move(dx, dy):
    """
    Cria uma mensagem de movimento do jogador.

    Args:
        dx (float): Delta X do movimento
        dy (float): Delta Y do movimento

    Returns:
        dict: Mensagem de movimento
    """
    return {
        "action": ACTION_MOVE,
        "dx": dx,
        "dy": dy
    }


# Mensagens do servidor

def make_init(player_id):
    """
    Cria uma mensagem de inicialização do cliente.

    Args:
        player_id (str): ID do jogador atribuído pelo servidor

    Returns:
        dict: Mensagem de inicialização
    """
    return {
        "action": ACTION_INIT,
        "player_id": player_id
    }


def make_state(state):
    """
    Cria uma mensagem com o estado atual do jogo.

    Args:
        state (dict): Estado do jogo (players, enemies, etc)

    Returns:
        dict: Mensagem de estado
    """
    return {
        "action": ACTION_STATE,
        **state
    }
