ACTION_MOVE = "move"
ACTION_SHOOT = "shoot"
ACTION_RELOAD = "reload"

def make_move(dx, dy, angle):
    return {"action": ACTION_MOVE, "dx": dx, "dy": dy, "angle": angle}

def make_shoot(angle):
    return {"action": ACTION_SHOOT, "angle": angle}

def make_reload():
    return {"action": ACTION_RELOAD}
