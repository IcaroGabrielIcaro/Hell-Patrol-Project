import pygame
from world import *
from pygame.math import Vector2
from Assets.assets import Assets

class Screen:
    def __init__(self,initialPosX, initialPosY):
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.screenWidth,self.screenHeight= self.screen.get_size()
        self.camera=(max(0,min(initialPosX-self.screenWidth//2,WORLD_WIDTH-self.screenWidth)), 
                     max(0,min(initialPosY-self.screenHeight//2,WORLD_HEIGHT-self.screenHeight)))
    
    def updateCamera(self,newPosX,newPosY):
        self.camera=(max(0,min(newPosX-self.screenWidth//2,WORLD_WIDTH-self.screenWidth)), 
                     max(0,min(newPosY-self.screenHeight//2,WORLD_HEIGHT-self.screenHeight)))
        
    def drawBackground(self,tileMap):
        self.screen.fill((0, 0, 0))
        for i in range (22):
            for j in range (30):
                self.screen.blit(tileMap[i][j], (j*96 - self.camera[0], i*96-self.camera[1]))
                
    def drawSprite(self,sprite,posX,posY,rotation):
        if not sprite:
            return
        rotated = pygame.transform.rotate(sprite, rotation)
        rect = rotated.get_rect(center=(posX - self.camera[0], posY - self.camera[1]))
        self.screen.blit(rotated,rect)

    def updateScreen(self):
        pygame.display.flip()

    def drawAimLine(self,direction,playerx,playery):
        start = Vector2(playerx-self.camera[0],playery-self.camera[1])
        length = 100000

        end = start + direction * length

        pygame.draw.line(self.screen, (255, 0, 0), start, end, 1)

    def drawReticle(self):
        xmouse=pygame.mouse.get_pos()[0]+self.camera[0]
        ymouse=pygame.mouse.get_pos()[1]+self.camera[1]
        self.drawSprite(Assets.images["crosshair1"],xmouse,ymouse,0)