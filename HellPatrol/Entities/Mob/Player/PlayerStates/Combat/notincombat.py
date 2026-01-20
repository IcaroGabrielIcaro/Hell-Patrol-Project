from Entities.Mob.StateMachine.States.state import State
from pygame.math import Vector2
import pygame

class NotInCombat(State):

    def __init__(self,objRef):
        super().__init__(objRef,"notincombat")    

    def start(self):
        self.objRef.animationcombat.switchTo("notincombat")
        pass

    def update(self,group,dt):
        self.objRef.animationcombat.playCurrent(dt)
        self.objRef.adjustAim()
        self.objRef.updateSwitchWeaponTime(dt)
        self.objRef.updateArsenal(dt) 
        buttons = pygame.mouse.get_pressed()
        if buttons[0] and self.objRef.canAttack():
            group.switchTo("incombat")
           

        
    def quit(self):
        pass