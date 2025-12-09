import pygame
from settings import TILE_SIZE

class SinglePlayer:
    def __init__(self,x,y,img,maze):
        self.x=x
        self.y=y
        self.img=img
        self.maze=maze

    def move(self,dx,dy):    
        nx,ny=self.x+dx, self.y+dy
        if not self.maze.is_wall(nx,ny):
            self.x=nx
            self.y=ny

    def draw(self,screen):
        screen.blit(self.img,(self.x*TILE_SIZE, self.y*TILE_SIZE))        