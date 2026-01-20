from Entities.Mob.StateMachine.States.state import State
from Entities.Mob.Player.player import Player
from Entities.Mob.Player.player import Player
from Entities.Mob.Enemies.FindPath.findpath import *
from pygame.math import Vector2
import pygame

class Agressive(State):
    def __init__(self,objRef):
        super().__init__(objRef,"agressive")

    def start(self):
        pass
    def update(self,group,dt):
        for e in self.objRef.entities["player"]:
            if isinstance(e,Player):
                playerreference=e
            if has_line_of_sight(Vector2(self.objRef.x,self.objRef.y),Vector2(playerreference.x,playerreference.y),self.objRef,self.objRef.entities["walls"]):
                self.objRef.direction=Vector2(playerreference.x-self.objRef.x,playerreference.y-self.objRef.y)
                self.objRef.move(dt)
            else:
                self.objRef.direction=Vector2(playerreference.x-self.objRef.x,playerreference.y-self.objRef.y)
                self.objRef.path=findpath(self.objRef,playerreference,self.objRef.entities["walls"])
                self.objRef.path_index=0
                if(len(self.objRef.path)>1):
                    self.objRef.move_along_path(dt)

    def quit(self):
        pass