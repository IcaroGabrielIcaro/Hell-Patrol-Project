from Entities.Mob.StateMachine.States.state import State
import pygame

class Idle(State):

    def __init__(self,objRef):

        super().__init__(objRef,"idle")
    
    def start(self):
        self.objRef.animationmovimentb.switchTo("idleB")
        self.objRef.animationmovimenth.switchTo("idleH")
        pass
    
    def update(self,group, dt):
        self.objRef.animationmovimentb.playCurrent(dt)
        self.objRef.animationmovimenth.playCurrent(dt)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r] and self.objRef.canSwitch():
            self.objRef.switchWeapon()
        if keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_w] or keys[pygame.K_s]:
            group.switchTo("moving")
    def quit(self):
        pass