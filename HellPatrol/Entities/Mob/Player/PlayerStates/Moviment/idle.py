from Entities.Mob.StateMachine.States.state import State
import pygame

class Idle(State):

    def __init__(self,objRef):

        super().__init__(objRef,"idle")
    
    def start(self):
        self.objRef.images[0][0].switchTo("idleB")
        self.objRef.images[2][0].switchTo("idleH")
        pass
    
    def update(self,group, dt):
        self.objRef.images[0][0].current.play(dt)
        self.objRef.images[2][0].current.play(dt)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r] and self.objRef.canSwitch(dt):
            self.objRef.switchWeapon()
        if keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_w] or keys[pygame.K_s]:
            group.switchTo("moving")
    def quit(self):
        pass