from Entities.Mob.mob import Mob
from Entities.Mob.Player.Weapons.machinegun import MachineGun
from Entities.Mob.Player.Weapons.sniper import Sniper
from Entities.Mob.Player.Weapons.shotgun import Shotgun
from Entities.Mob.StateMachine.stateMachine import StateMachine
from Entities.Mob.Player.PlayerStates.Combat.incombat import InCombat
from Entities.Mob.Player.PlayerStates.Combat.notincombat import NotInCombat
from Entities.Mob.Player.PlayerStates.Moviment.idle import Idle
from Entities.Mob.Player.PlayerStates.Moviment.moving import Moving
from Entities.ControlAnimation.controlanimation import ControlAnimation
from Entities.ControlAnimation.Animation.animation import Animation
from Assets.assets import Assets
from pygame.math import Vector2
import math

import pygame

class Player(Mob):

    def __init__(self, x, y,entities,screen):
        super().__init__(x, y, 40, 40, "player", 500,Vector2(0,0),entities)
        self.arsenal=(MachineGun(self),Sniper(self),Shotgun(self))
        self.actualweapon=0
        self.animationmovimentb=ControlAnimation((Animation("idleB",2,Assets.animations["playerIdleB"]),Animation("walkB",2,Assets.animations["playerWalkB"])))
        self.animationcombat=ControlAnimation((Animation("notincombat",80,Assets.animations["playerMGNotInCombat"]),Animation("incombat",1/(self.getActualWeapon().animationtime/2),Assets.animations["playerMGInCombat"])))
        self.animationmovimenth=ControlAnimation((Animation("idleH",2,Assets.animations["playerIdleH"]),Animation("walkH",2,Assets.animations["playerWalkH"])))
        self.images=(
                    (self.animationmovimentb.currentImage(), self.x, self.y, self.getRotation()),
                    (self.animationcombat.currentImage(),self.x,self.y,self.getRotation()),
                    (self.animationmovimenth.currentImage(),self.x,self.y,self.getRotation())
                    )
                
        self.entities=entities
        self.screen=screen
        self.states=(
                     StateMachine((Idle(self),Moving(self))),
                     StateMachine((NotInCombat(self),InCombat(self))),
                    )
        self.switchtime=0

    def update(self, dt):

        super().update(dt)

    def attack(self):
        self.getActualWeapon().shoot()
    
    def adjustImage(self):
        weaponX,weaponY=self.getActualWeapon().adjustWeapon()
        self.images=(
                        (pygame.transform.scale(self.animationmovimentb.currentImage(),(100,100)), self.x, self.y, self.getRotation()),
                        (pygame.transform.scale(self.animationcombat.currentImage(),(100,100)),weaponX,weaponY,self.getRotation()),
                        (pygame.transform.scale(self.animationmovimenth.currentImage(),(100,100)),self.x,self.y,self.getRotation())
                    )
    
    def adjustAim(self):
        camera=self.screen.camera
        xcam=self.x-camera[0]
        ycam=self.y-camera[1]
        xmouse,ymouse=pygame.mouse.get_pos()
        self.direction= Vector2(xmouse-xcam,ymouse-ycam)
        if self.direction.length()>0:
            self.direction=self.direction.normalize()
    
    def switchWeapon(self):
        self.actualweapon=(self.actualweapon+1)%len(self.arsenal)
        self.animationcombat=ControlAnimation((Animation("notincombat",80,Assets.animations["player"+self.getActualWeapon().name+"NotInCombat"]),Animation("incombat",1/(self.getActualWeapon().animationtime/2),Assets.animations["player"+self.getActualWeapon().name+"InCombat"])))
    
    def canSwitch(self,dt):
        if self.switchtime<=0:
            self.switchtime=0.5
            return True
        else:
            self.switchtime-=dt
            return False
    
    def canAttack(self):
        return self.getActualWeapon().canShoot()
    
    def getRotation(self):
        return self.direction.angle_to(Vector2(1, 0))+90
    
    def isAttacking(self):
        return self.getActualWeapon().isShooting()
    
    def getActualWeapon(self):
        return self.arsenal[self.actualweapon]
    
    def updateArsenal(self,dt):
        for weapon in self.arsenal:
            weapon.update(dt,self.screen.camera)