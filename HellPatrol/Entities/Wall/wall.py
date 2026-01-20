from Entities.entity import Entity
from Assets.assets import Assets
import pygame

class Wall(Entity):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "wall")
        self.images=((Assets.images["playerfirebullet"],self.x,self.y,self.getRotation()),)

    def update(self, dt):
        pass

    def adjustImage(self):
        pass