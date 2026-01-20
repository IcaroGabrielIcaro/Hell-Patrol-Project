from Entities.Mob.Bullets.bullet import Bullet
from Assets.assets import Assets
import pygame

class PlayerFireBullet(Bullet):

    def __init__(self,x,y,direction,entities):
        super().__init__(x, y, 10, 10, "playerfirebullet", 500,500, direction,entities)
        self.images=((Assets.images["playerfirebullet"],self.x,self.y,self.getRotation()),)

    def adjustImage(self):
        self.images=(
                    (Assets.images["playerfirebullet"], self.x, self.y, self.getRotation()),
                )
