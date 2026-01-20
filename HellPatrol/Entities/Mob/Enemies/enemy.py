from Entities.Mob.mob import Mob
from Assets.assets import Assets
from Entities.Mob.StateMachine.stateMachine import StateMachine
from Entities.Mob.Enemies.EnemyStates.agressive import Agressive
from pygame.math import Vector2

import pygame

class Enemy(Mob):
    def __init__(self, x, y,entities):
        super().__init__(x, y, 40, 40, "enemy",500, Vector2(0,0),entities)
        self.images=(
                    ((Assets.images["playersquaredbullet"], self.x, self.y, self.getRotation())),
                )
        self.states=(StateMachine((Agressive(self),)),)
        self.path=[]
        self.path_index=1
    
    def adjustImage(self):
        self.images=(
                    ((Assets.images["playersquaredbullet"], self.x, self.y, self.getRotation())),
                )
            
    def move_along_path(self,dt):
        totaldistance=self.vel*dt
        targetposition=Vector2(self.path[self.path_index][0]-self.x,self.path[self.path_index][1]-self.y)
        if targetposition.length() == 0:
            return
        elif targetposition.length() < totaldistance and len(self.path)>self.path_index+1:
            self.path_index+=1
            return self.move_along_path(dt)
        else:
            self.direction=targetposition.normalize()
            self.move(dt)

    def move_along_path(self,dt):
        return self.move_along_path2(0,dt)

    def move_along_path2(self,distancep,dt):
        totaldistance=self.vel*dt
        if len(self.path)<=self.path_index+1:
            return self.move(dt)
        else:
            p1=self.path[self.path_index]
            p2=self.path[self.path_index+1]
            dp1p2=Vector2(p2[0]-p1[0],p2[1]-p1[1])
            if totaldistance == min(totaldistance,distancep+dp1p2.length()):
                self.direction=dp1p2.normalize()*(totaldistance-distancep)
                return self.move(dt)
            else:
                self.path_index+=1
                distancep+=dp1p2.length()
                return self.move_along_path2(distancep,dt)

