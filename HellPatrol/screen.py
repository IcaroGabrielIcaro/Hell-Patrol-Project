import pygame
from world import *
from pygame.math import Vector2
from Assets.assets import Assets

class Screen:
    def __init__(self,initialPosX, initialPosY):
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        screenWidth,screenHeight= self.screen.get_size()
        self.camera=(max(0,min(initialPosX-screenWidth//2,WORLD_WIDTH-screenWidth)), 
                     max(0,min(initialPosY-screenHeight//2,WORLD_HEIGHT-screenHeight)))
    
    def update_camera(self,newPosX,newPosY):
        screenWidth,screenHeight= self.screen.get_size()
        self.camera=(max(0,min(newPosX-screenWidth//2,WORLD_WIDTH-screenWidth)), 
                     max(0,min(newPosY-screenHeight//2,WORLD_HEIGHT-screenHeight)))
        
    def draw_background(self,tileMap):
        self.screen.fill((0, 0, 0))
        for i in range (22):
            for j in range (30):
                self.screen.blit(tileMap[i][j], (j*96 - self.camera[0], i*96-self.camera[1]))
                
    def draw_sprite(self,sprite,posX,posY,rotation):
        if not sprite:
            return
        rotated = pygame.transform.rotate(sprite, rotation)
        rect = rotated.get_rect(center=(posX - self.camera[0], posY - self.camera[1]))
        self.screen.blit(rotated,rect)

    def update_screen(self):
        pygame.display.flip()

    def drawAimLine(self,direction,playerx,playery):
        start = Vector2(playerx-self.camera[0],playery-self.camera[1])
        length = 100000

        end = start + direction * length

        pygame.draw.line(self.screen, (255, 0, 0), start, end, 1)

    def drawReticle(self):
        xmouse=pygame.mouse.get_pos()[0]+self.camera[0]
        ymouse=pygame.mouse.get_pos()[1]+self.camera[1]
        self.draw_sprite(Assets.images["crosshair1"],xmouse,ymouse,0)