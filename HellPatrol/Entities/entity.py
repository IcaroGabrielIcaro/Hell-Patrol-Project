from abc import ABC, abstractmethod
import pygame
from pygame.math import Vector2

class Entity(ABC):

    def __init__ (self, x, y, width, height, type):
        self.width = width
        self.height = height
        self.collider = pygame.Rect(x-self.width//2,y-self.height//2,self.width,self.height)
        self.x=x
        self.y=y
        self.direction=Vector2(1,0)
        self.images=()
        self.type= type
        self.dead=False

    @abstractmethod
    def update(self,dt):
        pass

    @abstractmethod
    def adjustImage(self):
        pass
    
    def getImages(self):
        self.adjustImage()
        return self.images
    def drawCollider(self,tela,camera=(0,0)):
        pygame.draw.rect(tela, (255,0,0), pygame.Rect(self.collider.x-camera[0],self.collider.y-camera[1],self.width,self.height))

    def getRotation(self):
        return self.direction.angle_to(Vector2(1, 0))+90