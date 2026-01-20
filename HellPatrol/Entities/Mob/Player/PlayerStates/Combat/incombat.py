from Entities.Mob.StateMachine.States.state import State
from pygame.math import Vector2
import pygame

class InCombat(State):

    def __init__(self,objRef):
        super().__init__(objRef,"incombat")

    def start(self):
        self.objRef.animationcombat.switchTo("incombat")
        self.objRef.attack()        

    def update(self,group,dt):
        self.objRef.animationcombat.playCurrent(dt)
        self.objRef.adjustAim()
        buttons = pygame.mouse.get_pressed()
        if (not buttons[0] and not self.objRef.isAttacking()) or (not self.objRef.canAttack() and not self.objRef.isAttacking()):
            group.switchTo("notincombat")

        elif buttons[0] and self.objRef.canAttack():
            self.objRef.attack()
        for weapon in self.objRef.weapon:
            weapon.update(dt,self.objRef.screen.camera)  
    def quit(self):
        pass
