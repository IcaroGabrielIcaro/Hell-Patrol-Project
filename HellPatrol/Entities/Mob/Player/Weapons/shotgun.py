from Entities.Mob.Player.Weapons.weapon import Weapon
from Entities.Mob.Bullets.PlayerBullet.playersquaredbullet import PlayerSquaredBullet


class Shotgun(Weapon):

    def __init__(self, user):
        super().__init__(user,1,2,0.025,"SG")
    
    def update(self,dt,camera):
        super().update(32, 4,camera, dt)
        
    def shoot(self):
        super().shoot()
        self.user.entities["playerbullets"].append(PlayerSquaredBullet(self.bulletposX,self.bulletposY,self.shootdirection,self.user.entities))
        self.user.entities["playerbullets"].append(PlayerSquaredBullet(self.bulletposX,self.bulletposY,self.shootdirection.rotate(-10.0),self.user.entities))
        self.user.entities["playerbullets"].append(PlayerSquaredBullet(self.bulletposX,self.bulletposY,self.shootdirection.rotate(10.0),self.user.entities))
        self.user.entities["playerbullets"].append(PlayerSquaredBullet(self.bulletposX,self.bulletposY,self.shootdirection.rotate(-20.0),self.user.entities))
        self.user.entities["playerbullets"].append(PlayerSquaredBullet(self.bulletposX,self.bulletposY,self.shootdirection.rotate(20.0),self.user.entities))

    def adjustWeapon(self):
        tempv=self.user.aimdirection*20
        adjustInX=tempv.x
        adjustInY=tempv.y
        return (self.user.x+adjustInX,self.user.y+adjustInY)