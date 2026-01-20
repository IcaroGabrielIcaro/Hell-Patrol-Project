from abc import ABC, abstractmethod
from Entities.entity import Entity
from Entities.Wall.wall import Wall
from pygame.math import Vector2

import pygame

class Mob(Entity):
    def __init__(self, x, y, width, height, type, vel, direction, entities):
        super().__init__(x, y, width, height, type)
        self.vel=vel
        self.direction=direction
        self.entities=entities
        self.states=[]
    def update(self,dt):

        for statemachine in self.states:
            statemachine.currentState.update(statemachine,dt)
        self.adjustImage()
        
    def move(self, dt):
        if self.direction.length()>0:
            self.direction=self.direction.normalize()
        dx=self.direction.x * self.vel* dt
        dy=self.direction.y * self.vel* dt
        self.move2(dx,0)
        self.move2(0,dy)

        
    def move2(self,dx, dy):

        self.collider.x += dx
        self.collider.y += dy

        for e in self.entities["walls"]:
            if isinstance(e,Wall) and self.collider.colliderect(e.collider):
                if dx > 0:
                    self.collider.right=e.collider.left
                if dx < 0:
                    self.collider.left=e.collider.right
                if dy > 0:
                    self.collider.bottom=e.collider.top
                if dy < 0:
                    self.collider.top=e.collider.bottom
        self.collider.x = max(0, min(2880 - self.width, self.collider.x))
        self.collider.y = max(0, min(2112 - self.height, self.collider.y))
        self.x=self.collider.x+self.width//2
        self.y=self.collider.y+self.height//2