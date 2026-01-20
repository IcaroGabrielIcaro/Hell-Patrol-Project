from Entities.Mob.Player.Weapons.weapon import Weapon
from Entities.Mob.Bullets.PlayerBullet.playershortbullet import PlayerShortBullet
import random


class MachineGun(Weapon):
    
    def __init__(self, user):
        super().__init__(user,20,10,0.025,"MG")
    
    def update(self,dt,camera):
        super().update(40, 5,camera, dt)

    def shoot(self):
        super().shoot()
        self.user.entities["playerbullets"].append(PlayerShortBullet(self.bulletposX,self.bulletposY,self.shootdirection.rotate(random.uniform(-self.precision,self.precision)),self.user.entities))
             
    def adjustWeapon(self):
        tempv=self.user.aimdirection*20
        adjustInX=tempv.x
        adjustInY=tempv.y
        return (self.user.x+adjustInX,self.user.y+adjustInY)
