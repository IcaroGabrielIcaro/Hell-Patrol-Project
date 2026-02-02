ACTION_MOVE = "move"

def make_move(dx, dy, angle):
    return {
        "action": ACTION_MOVE,
        "dx": dx,
        "dy": dy,
        "angle": angle
    }
