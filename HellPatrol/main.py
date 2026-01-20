import pygame
from Entities.Mob.Player.player import  Player
from Entities.Wall.wall import  Wall
from screen import Screen
from Assets.assets import Assets
from Entities.Mob.Enemies.enemy import Enemy
from TileMap.tileMap import TileMap
from world import *

pygame.init()
entities = {
    "player":[],
    "enemies": [],
    "playerbullets": [],
    "enemiesbullets": [],
    "walls": []
}
pygame.mouse.set_visible(False)
screen=Screen(80,80)
Assets.loadImages()
Assets.loadAnimations()
player=Player(80,80,entities,screen)
clock = pygame.time.Clock()

enemy=Enemy(20,20,entities)
enemy=Enemy(200,800,entities)
wall= Wall(600,200,20,400)
wall2= Wall(250,390,500,20)
wall3= Wall(300,230,20,350)
tileMap=TileMap()
entities["player"].append(player)
#entities["walls"].append(wall)
entities["walls"].append(wall2)
#entities["walls"].append(wall3)
entities["enemies"].append(enemy)


running=True
while running:

    dt = clock.tick(60) / 1000

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            runnig = False
    screen.draw_background(tileMap.tileMap)
    for key,group in entities.items():
        for entity in group:
            entity.update(dt)
            entity.draw(screen.screen,screen.camera)
            for image in entity.getImages():
                screen.draw_sprite(*(image))
            group[:] = [e for e in group if not e.dead]
    screen.drawAimLine(player.weapon[player.actualweapon].shootdirection,player.weapon[player.actualweapon].bulletposX,player.weapon[player.actualweapon].bulletposY)
    screen.drawReticle()
    screen.update_screen()

pygame.quit()

