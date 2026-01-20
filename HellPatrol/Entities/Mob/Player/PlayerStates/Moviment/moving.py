from Entities.Mob.StateMachine.States.state import State
from pygame.math import Vector2
import pygame

class Moving(State):

    def __init__(self,objRef):
        super().__init__(objRef,"moving")

    def start(self):
        self.objRef.animationmovimentb.switchTo("walkB")
        self.objRef.animationmovimenth.switchTo("walkH")
        pass
    def update(self,group,dt):
        self.objRef.animationmovimentb.playCurrent(dt)
        self.objRef.animationmovimenth.playCurrent(dt)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r] and self.objRef.canSwitch():
            self.objRef.switchWeapon()
        if not(keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_w] or keys[pygame.K_s]):
            group.switchTo("idle")
        if keys[pygame.K_a]:
            self.objRef.direction.x -= 1
        if keys[pygame.K_d]:
            self.objRef.direction.x += 1
        if keys[pygame.K_w]:
            self.objRef.direction.y -= 1
        if keys[pygame.K_s]:
            self.objRef.direction.y +=1
        self.objRef.move(dt)
        self.objRef.screen.updateCamera(self.objRef.x,self.objRef.y)

    def quit(self):
        pass
