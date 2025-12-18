ACTION_MOVE = "move"

def make_move(dx, dy):
    return {
        "action": ACTION_MOVE,
        "dx": dx,
        "dy": dy
    }
