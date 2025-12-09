import sys
import pygame
from collections import deque
from settings import TILE_SIZE,FPS, TREASURE_POS
import time

class MazeSolver:
    def __init__(self,maze,screen,player_img):
        self.maze=maze
        self.screen=screen
        self.player_img=player_img


    def bfs(self,start,goal):
        queue=deque()
        queue.append([start])
        visited=set()
        visited.add(start)

        while queue:
            path=queue.popleft()
            x,y=path[-1]

            if(x,y)==goal:
                return path
            
            for dx,dy in [(0,-1),(0,1),(-1,0),(1,0)]:
                nx,ny= x+dx, y+dy

                if (nx,ny) not in visited and not self.maze.is_wall(nx,ny):
                 visited.add((nx, ny))
                 new_path = path + [(nx, ny)]
                 queue.append(new_path)
        return []  # yol yoksa
    
    def animate_path(self,path,wall_img,treasure_img):
        clock=pygame.time.Clock()
        for(x,y) in path:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.screen.fill((30,30,30))

            self.maze.draw(self.screen, wall_img)  
            tx,ty=TREASURE_POS
            self.screen.blit(treasure_img, (tx * TILE_SIZE, ty * TILE_SIZE))
            self.screen.blit(self.player_img,(x*TILE_SIZE,y*TILE_SIZE))

            pygame.display.flip()
            #clock.tick(FPS // 2)
            time.sleep(0.03)   

             