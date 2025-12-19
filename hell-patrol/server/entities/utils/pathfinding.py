
from shared.world import WORLD_TILES_X, WORLD_TILES_Y, TILE_SIZE
import heapq

class Pathfinder:
    def __init__(self, obstacles=None):
        self.cols = WORLD_TILES_X
        self.rows = WORLD_TILES_Y
        self.grid = [[0]*self.cols for _ in range(self.rows)]
        if obstacles:
            for x, y in obstacles:
                self.grid[y][x] = 1

    def neighbors(self, x, y):
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x+dx, y+dy
            if 0 <= nx < self.cols and 0 <= ny < self.rows:
                if self.grid[ny][nx] == 0:
                    yield nx, ny

    def heuristic(self, a, b):
        # Manhattan
        return abs(a[0]-b[0]) + abs(a[1]-b[1])

    def a_star(self, start, goal):
        if start == goal:
            return []
        pq = [(0, start)]
        g_score = {start:0}
        f_score = {start:self.heuristic(start, goal)}
        came_from = {}

        while pq:
            _, current = heapq.heappop(pq)
            if current == goal:
                break
            for n in self.neighbors(*current):
                tentative_g = g_score[current] + 1
                if n not in g_score or tentative_g < g_score[n]:
                    came_from[n] = current
                    g_score[n] = tentative_g
                    f_score[n] = tentative_g + self.heuristic(n, goal)
                    heapq.heappush(pq, (f_score[n], n))

        path = []
        cur = goal
        while cur in came_from:
            path.append(cur)
            cur = came_from[cur]
        path.reverse()
        return path
