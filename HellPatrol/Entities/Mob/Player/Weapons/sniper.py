from Entities.Mob.Player.Weapons.weapon import Weapon
from Entities.Mob.Bullets.PlayerBullet.playerlongbluebullet import PlayerLongBlueBullet
import random

class Sniper(Weapon):

    def __init__(self, user):
        super().__init__(user,1,0,0.025,"SP")
    
    def update(self,dt,camera):
        super().update(45, 7,camera, dt)

    def shoot(self):
        super().shoot()
        self.user.entities["playerbullets"].append(PlayerLongBlueBullet(self.bulletposX,self.bulletposY,self.shootdirection.rotate(random.uniform(-self.precision,self.precision)),self.user.entities))

    def adjustWeapon(self):
        tempv=self.user.aimdirection*20
        adjustInX=tempv.x
        adjustInY=tempv.y
        return (self.user.x+adjustInX,self.user.y+adjustInY)