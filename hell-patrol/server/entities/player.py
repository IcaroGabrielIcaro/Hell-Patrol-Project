class Player:
    def __init__(self):
        self.x = 100
        self.y = 100

    def move(self, dx, dy):
        self.x += dx * 5
        self.y += dy * 5

    def to_dict(self):
        return {"x": self.x, "y": self.y}
