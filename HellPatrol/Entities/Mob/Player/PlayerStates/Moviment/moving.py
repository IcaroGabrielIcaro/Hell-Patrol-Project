from Entities.Mob.StateMachine.States.state import State
from pygame.math import Vector2
import pygame

class Moving(State):

    def __init__(self,objRef):
        super().__init__(objRef,"moving")

    def start(self):
        self.objRef.images[0][0].switchTo("walkB")
        self.objRef.images[2][0].switchTo("walkH")
        pass
    def update(self,group,dt):
        self.objRef.images[0][0].current.play(dt)
        self.objRef.images[2][0].current.play(dt)
        keys = pygame.key.get_pressed()
        if not(keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_w] or keys[pygame.K_s]):
            group.switchTo("idle")
        self.objRef.direction= Vector2(0,0)
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_a]:
            self.objRef.direction.x -= 1
        if teclas[pygame.K_d]:
            self.objRef.direction.x += 1
        if teclas[pygame.K_w]:
            self.objRef.direction.y -= 1
        if teclas[pygame.K_s]:
            self.objRef.direction.y +=1
        if keys[pygame.K_r] and self.objRef.canSwitch(dt):
            self.objRef.switchWeapon()
        self.objRef.move(dt)
        self.objRef.camera.update_camera(self.objRef.x,self.objRef.y)

    def quit(self):
        pass
