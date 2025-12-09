import pygame
from settings import TILE_SIZE

class Maze:
    def __init__(self, filename):
        self.grid = []
        self.walls = []
        self.load_maze(filename)

    def load_maze(self, filename):
        with open(filename, "r") as f:
            for row in f.readlines():
                row = row.strip("\n")
                self.grid.append(list(row))

    def draw(self, screen, wall_img):
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell == "X":
                    screen.blit(wall_img, (x * TILE_SIZE, y * TILE_SIZE))
                    

    def is_wall(self, x, y):
        grid_x = x 
        grid_y = y 

        if grid_y < 0 or grid_y >= len(self.grid):
            return True
        if grid_x < 0 or grid_x >= len(self.grid[0]):
            return True

        return self.grid[grid_y][grid_x] == "X"
