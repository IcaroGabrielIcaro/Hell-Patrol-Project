from Assets.assets import Assets
import pygame
import random
from world import *

class TileMap:

    def __init__(self):
        tile11 = pygame.transform.scale(Assets.images["hellTile11"], (96, 96))
        tile12 = pygame.transform.scale(Assets.images["hellTile12"], (96, 96))
        tile13 = pygame.transform.scale(Assets.images["hellTile13"], (96, 96))
        tile21 = pygame.transform.scale(Assets.images["hellTile21"], (96, 96))
        tile31 = pygame.transform.scale(Assets.images["hellTile31"], (96, 96))
        tileG1 = pygame.transform.scale(Assets.images["hellGrateS1"], (96, 96))
        tileV1 = pygame.transform.scale(Assets.images["hellVent1"], (96, 96))
        tileV2 = pygame.transform.scale(Assets.images["hellVent2"], (96, 96))
        self.tiles = [tile11, tile12, tile13, tile21, tile31, tileG1, tileV1, tileV2]
        prob = [10, 3, 2, 1, 1, 0, 0, 0]
        
        self.tileMap = []
        for i in range(WORLD_HEIGHT // 96):
            row = []
            for j in range(WORLD_WIDTH // 96):
                prob = self.get_region(i, j)
                tile = random.choices(self.tiles, weights=prob, k=1)[0]
                row.append(tile)
            self.tileMap.append(row)

    def get_region(self, i, j):
        GRATE_AREA=[((12,10),(24,45)),((60,60),(75,92))]
        def in_area(point,r1,r2):
            return r1[0]<=point[0] and point[0] <= r2[0] and r1[1]<=point[1] and point[1] <= r2[1]
        
        for area in GRATE_AREA:
            if in_area((i,j),area[0],area[1]):
                return [10, 3, 2, 1, 1, 0, 0, 0]
        return [0, 0, 0, 1, 1, 10, 3, 1]
