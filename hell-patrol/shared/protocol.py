# Tipos de ações
ACTION_MOVE = "move"
ACTION_SHOOT = "shoot"
ACTION_RELOAD = "reload"
ACTION_INIT = "init"
ACTION_STATE = "state"

# Mensagens do cliente

def make_move(dx, dy, angle=0):
    return {
        "action": ACTION_MOVE,
        "dx": dx,
        "dy": dy,
        "angle": angle
    }

def make_shoot(angle):
    return {
        "action": ACTION_SHOOT,
        "angle": angle
    }

def make_reload():
    return {
        "action": ACTION_RELOAD
    }

# Mensagens do servidor

def make_init(player_id):
    return {
        "action": ACTION_INIT,
        "player_id": player_id
    }

def make_state(state):
    return {
        "action": ACTION_STATE,
        **state
    }
