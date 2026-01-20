WORLD_WIDTH,WORLD_HEIGHT=2880, 2112

import heapq
import pygame
from pygame.math import Vector2
from world import *


COUNT=0
STEP_SIZE=16

class Node:
    def __init__(self, posX, posY, father=None):
        self.x = posX
        self.y = posY
        self.father = father
        self.g = father.g + 1 if father else 0 

    def f(self,target):
        return self.g + ((self.x - target.x)**2 + (self.y - target.y)**2)**0.5 

def findpath(enemy,target,walls):
    global COUNT
    x_cell = int(enemy.x // STEP_SIZE)
    y_cell = int(enemy.y // STEP_SIZE)
    target_x = int(target.x // STEP_SIZE)
    target_y = int(target.y // STEP_SIZE)

    origin= Node(x_cell,y_cell)
    goal= Node(target_x,target_y)
    print(target_x,target_y)
    if isBlocked(target_x,target_y,enemy,walls):
        print("ferrou")

    openHeap=[]
    closedSet=set()
    openLookup={}
    openLookup[(x_cell, y_cell)] = 0
    heapq.heappush(openHeap,(origin.f(goal),COUNT, origin))    
    while openHeap:

        _, _, node = heapq.heappop(openHeap)
        if isOnTarget(node,goal):
            COUNT=0
            return finalPath(node,enemy,walls)
        closedSet.add((node.x,node.y))
        searchNgbhd(node,openLookup,closedSet,openHeap,goal,enemy,walls)    
    return []

def searchNgbhd(node,openLookup,closedSet,openHeap,goal,enemy,walls):
    global COUNT
    for pair in [(1,0),(0,1),(-1,0),(0,-1)]:
        searchnode=(node.x+pair[0],node.y+pair[1])
        if searchnode[0] <0 or searchnode[0] >= WORLD_WIDTH//STEP_SIZE or searchnode[1] < 0 or searchnode[1] >= WORLD_HEIGHT//STEP_SIZE or searchnode in closedSet or isBlocked(*(searchnode),enemy,walls):
            continue
        if not( searchnode in openLookup):
            COUNT+=1
            openLookup[searchnode]= node.g+1
            neighbor=Node(*(searchnode),node)
            heapq.heappush(openHeap,(neighbor.f(goal),COUNT, neighbor))

        elif openLookup[searchnode] > node.g+1:
            COUNT+=1
            openLookup[searchnode]= node.g+1
            neighbor=Node(*(searchnode),node)
            heapq.heappush(openHeap,(neighbor.f(goal),COUNT, neighbor))
    
    for pair in [(1,1),(1,-1),(-1,1),(-1,-1)]:
        searchnode=(node.x+pair[0],node.y+pair[1])
        tempxsearchnode=(node.x+pair[0],node.y)
        tempysearchnode=(node.x,node.y+pair[1])
        if searchnode[0] < 0 or searchnode[0] >= WORLD_WIDTH//STEP_SIZE or searchnode[1] < 0 or searchnode[1] >= WORLD_HEIGHT//STEP_SIZE or searchnode in closedSet or isBlocked(*(searchnode),enemy,walls) or isBlocked(*(tempxsearchnode),enemy,walls) or isBlocked(*(tempysearchnode),enemy,walls):
            continue
        if not( searchnode in openLookup):
            COUNT+=1
            openLookup[searchnode]= node.g+1
            neighbor=Node(*(searchnode),node)
            heapq.heappush(openHeap,(neighbor.f(goal),COUNT, neighbor))

        elif openLookup[searchnode] > node.g+1 :
            COUNT+=1
            openLookup[searchnode]= node.g+1
            neighbor=Node(*(searchnode),node)
            heapq.heappush(openHeap,(neighbor.f(goal),COUNT, neighbor))

def isBlocked(posX,posY,enemy,walls):
    cell_center_x = posX * STEP_SIZE + STEP_SIZE // 2
    cell_center_y = posY * STEP_SIZE + STEP_SIZE // 2
    next_rect = pygame.Rect(cell_center_x - enemy.width // 2,
                            cell_center_y - enemy.height // 2,
                            enemy.width, enemy.height)
    for wall in walls:
        if next_rect.colliderect(wall.collider):
            return True
    return False

def isOnTarget(node,target):
    
    return node.x==target.x and node.y==target.y

def finalPath(node,enemy,walls):
    path=[]
    while node:
        px=node.x*STEP_SIZE + STEP_SIZE//2
        py=node.y*STEP_SIZE + STEP_SIZE//2
        path.append((px,py))
        node=node.father
    path.reverse()
    return smooth_path(path,enemy,walls)

def smooth_path(path, enemy, walls):
    if len(path) <= 2:
        return path

    smooth = [path[0]]
    i = 0

    while i < len(path) - 1:
        j = len(path) - 1
        while j > i + 1:
            if has_line_of_sight(
                Vector2(smooth[-1]),
                Vector2(path[j]),
                enemy,
                walls
            ):
                break
            j -= 1
        smooth.append(path[j])
        i = j

    return smooth

def has_line_of_sight(p1, p2, enemy, walls):
    if p1==p2:
        return True
    steps = int((p2 - p1).length() / 4) 
    direction = (p2 - p1).normalize()

    for i in range(steps):
        pos = p1 + direction * i * 4
        rect = pygame.Rect(
            pos.x - enemy.width / 2,
            pos.y - enemy.height / 2,
            enemy.width,
            enemy.height
        )
        for wall in walls:
            if rect.colliderect(wall.collider):
                return False
    return True
