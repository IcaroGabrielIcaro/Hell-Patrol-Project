from abc import ABC, abstractmethod
import pygame
from pygame.math import Vector2

class Weapon(ABC):

    def __init__(self,user,cadence,precision,animationtime,name):
        self.animationtime=animationtime
        self.animationrunning=0
        self.waittime=0
        self.user=user
        self.cadence=cadence
        self.precision=precision
        self.name=name
        self.shootdirection=Vector2(1,0)
        self.bulletposX=self.user.x
        self.bulletposY=self.user.y

    def update(self,a,b,camera,dt):
        self.animationrunning = max(0, self.animationrunning - dt)
        self.waittime = max(0, self.waittime - dt)
        self.adjustToWeapon(a,b)
        self.adjustShootDirection(camera)

    def adjustToWeapon(self,a,b):
        tempv=self.user.direction.rotate(-90)*b
        tempv2=self.user.direction*a
        tempv3=tempv+tempv2
        adjustInX=tempv3.x
        adjustInY=tempv3.y
        self.bulletposX=self.user.x+adjustInX
        self.bulletposY=self.user.y+adjustInY
    
    def canShoot(self):
        return self.waittime<=0
    
    def isShooting(self):
        return self.animationrunning>0
    
    def adjustShootDirection(self,camera):
        xcam=self.bulletposX-camera[0]
        ycam=self.bulletposY-camera[1]
        xmouse,ymouse=pygame.mouse.get_pos()
        self.shootdirection= Vector2(xmouse-xcam,ymouse-ycam)
        self.shootdirection = self.shootdirection.normalize()
        
    def shoot(self):
        self.animationrunning=self.animationtime
        self.waittime=1/self.cadence

    @abstractmethod
    def adjustWeapon(self):
        pass
   
