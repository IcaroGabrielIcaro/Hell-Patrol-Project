from Entities.Mob.StateMachine.States.state import State
from pygame.math import Vector2
import pygame

class NotInCombat(State):

    def __init__(self,objRef):
        super().__init__(objRef,"notincombat")    

    def start(self):
        self.objRef.images[1][0].switchTo("notincombat")
        pass

    def update(self,group,dt):
        self.objRef.images[1][0].current.play(dt)
        self.objRef.adjustAim()
        buttons = pygame.mouse.get_pressed()
        if buttons[0] and self.objRef.canAttack():
            group.switchTo("incombat")
        for weapon in self.objRef.weapon:
            weapon.update(dt,self.objRef.camera.camera)       

        
    def quit(self):
        pass