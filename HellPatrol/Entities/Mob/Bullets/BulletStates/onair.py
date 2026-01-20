from Entities.Mob.StateMachine.States.state import State
from pygame.math import Vector2
import pygame

class OnAir(State):

    def __init__(self,objRef):
        super().__init__(objRef,"onair")
    
    def start(self):
        #self.objRef.setAnimation("incombat")
        pass     

    def update(self,group,dt):
        
        self.objRef.move(dt)

    def quit(self):
        pass
