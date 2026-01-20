from Entities.Mob.mob import Mob
from Entities.Wall.wall import Wall 
from Entities.Mob.StateMachine.stateMachine import StateMachine
from Entities.Mob.Bullets.BulletStates.onair import OnAir

class Bullet(Mob):

    def __init__(self, x, y, width, height, type, vel,range,direction,entities):

        super().__init__(x, y, width, height, type, vel,direction,entities)
        self.range=range
        self.states=(StateMachine((OnAir(self),)),)
    
    def move(self, dt):
        pos=(self.x,self.y)
        pos += self.direction * self.vel * dt
        self.range -= (self.direction*self.vel*dt).length()
        self.x,self.y=pos
        self.collider.center = pos

        if self.collider.x > 2880 or self.collider.x < 0 or self.collider.y >2112 or self.collider.y<0 or self.range<=0:
            self.dead=True
        for e in self.entities["walls"]:
            if self.collider.colliderect(e.collider):
                self.dead = True
                return
