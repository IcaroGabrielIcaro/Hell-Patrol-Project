from Entities.Mob.Bullets.bullet import Bullet
from Assets.assets import Assets
import pygame

class PlayerLongBlueBullet(Bullet):

    def __init__(self,x,y,direction,entities):
        super().__init__(x, y, 10, 10, "playerlongbluebullet", 1600,10000, direction,entities)
        self.images=((Assets.images["playerlongbluebullet"],self.x,self.y,self.getRotation()),)

    def adjustImage(self):
        self.images=(
                    ((pygame.transform.scale(Assets.images["playerlongbluebullet"],(100,100)), self.x, self.y, self.getRotation())),
                )
