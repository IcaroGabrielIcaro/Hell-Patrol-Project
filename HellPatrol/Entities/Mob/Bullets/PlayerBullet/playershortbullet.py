from Entities.Mob.Bullets.bullet import Bullet
from Assets.assets import Assets

class PlayerShortBullet(Bullet):

    def __init__(self,x,y,direction,entities):
        super().__init__(x, y, 10, 10, "playershortbullet", 800,1500, direction,entities)
        self.images=((Assets.images["playershortbullet"],self.x,self.y,self.getRotation()),)

    def adjustImage(self):
        self.images=(
                    ((Assets.images["playershortbullet"], self.x, self.y, self.getRotation())),
                )
