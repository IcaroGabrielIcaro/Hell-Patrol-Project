from Entities.Mob.Bullets.bullet import Bullet
from Assets.assets import Assets

class PlayerSquaredBullet(Bullet):

    def __init__(self,x,y,direction,entities):
        super().__init__(x, y, 10, 10, "playersquaredbullet", 800,1000, direction,entities)
        self.images=((Assets.images["playersquaredbullet"],self.x,self.y,self.getRotation()),)

    def adjustImage(self):
        self.images=(
                    ((Assets.images["playersquaredbullet"], self.x, self.y, self.getRotation())),
                )
