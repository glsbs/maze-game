import pygame
import sys
import random
from maze import Maze
from maze_solver import MazeSolver
from single_player import SinglePlayer
from client import NetworkPlayer
from settings import *

pygame.init()

screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Maze Game")

clock=pygame.time.Clock()




wall_img=pygame.image.load("assets/wall.png")
wall_img=pygame.transform.scale(wall_img,(TILE_SIZE,TILE_SIZE))
player_img1 = pygame.image.load("assets/player1.png")
player_img1=pygame.transform.scale(player_img1,(TILE_SIZE,TILE_SIZE))
player_img2 = pygame.image.load("assets/player2.png")
player_img2=pygame.transform.scale(player_img2,(TILE_SIZE,TILE_SIZE))
treasure_img = pygame.image.load("assets/treasure.png")
treasure_img=pygame.transform.scale(treasure_img,(TILE_SIZE,TILE_SIZE))


maze=Maze("maze.txt")

def draw_text(text,y):
    font=pygame.font.SysFont("Arial",32)
    surf=font.render(text,True,(255,255,255))
    rect=surf.get_rect(center=(SCREEN_WIDTH//2,y))
    screen.blit(surf,rect)

def menu():
    while True:
        screen.fill((20,20,20))
        draw_text("Maze Game",150)
        draw_text("1- Tek Kişi",300)
        draw_text("2- Bilgisayar Oynasın",350) 
        draw_text("3- İki Kişi ",400)
        draw_text("Çık",500)

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type==pygame.QUIT:
                pygame.quit()
                sys.exit()

            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_1:
                    start_single_player()
                if e.key==pygame.K_2:
                    start_bfs_solver()
                if e.key==pygame.K_3:
                    start_multiplayer()
                if e.key==pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()



def start_single_player():
    player=SinglePlayer(1,1,player_img1,maze)
    steps = 0  # kaç adım

    while True:
        screen.fill((30,30,30))
        maze.draw(screen,wall_img)
        screen.blit(treasure_img, (TREASURE_POS[0]*TILE_SIZE, TREASURE_POS[1]*TILE_SIZE))
        player.draw(screen)

        if (player.x, player.y) == TREASURE_POS:
            win_screen(f"Tek Kişi: {steps} adımda kazandın!")
            return

        for e in pygame.event.get():
            if e.type==pygame.QUIT:
                return
            
            if e.type == pygame.KEYDOWN:
                dx = dy = 0
                if e.key == pygame.K_UP: dy = -1
                if e.key == pygame.K_DOWN: dy = 1
                if e.key == pygame.K_LEFT: dx = -1
                if e.key == pygame.K_RIGHT: dx = 1
                if e.key == pygame.K_ESCAPE: return


                nx, ny = player.x + dx, player.y + dy
                if not maze.is_wall(nx, ny):
                    player.move(dx, dy)
                    steps += 1

        pygame.display.flip()
        clock.tick(FPS)




def start_bfs_solver():
    solver=MazeSolver(maze,screen,player_img1)    
    start=(1,1)
    goal=TREASURE_POS

    screen.fill((0,0,0))
    maze.draw(screen,wall_img)
    screen.blit(treasure_img,(goal[0]*TILE_SIZE,goal[1]*TILE_SIZE))
    pygame.display.flip()

    path=solver.bfs(start,goal)

    solver.animate_path(path, wall_img, treasure_img)

    win_screen(f"Bilgisayar: {len(path)-1} adımda çözdü!")




def start_multiplayer():
    net = NetworkPlayer("127.0.0.1", 5000)
    player_img = player_img1 if net.player_id == 1 else player_img2

    # Her oyuncu kendi steps değerini sadece kendi bilgisayarında tutar
    steps = 0

    # Başlangıç konumu
    x = net.start_x
    y = net.start_y



    while True:
        screen.fill((20, 20, 20))
        maze.draw(screen, wall_img)

        # Treasure çiz
        screen.blit(treasure_img, (TREASURE_POS[0] * TILE_SIZE, TREASURE_POS[1] * TILE_SIZE))

        # Kendi oyuncunu çiz
        screen.blit(player_img, (x * TILE_SIZE, y * TILE_SIZE))

        # Diğer oyuncular
        others = net.get_other_players()


        for pid, pos in others.items():
            
            pid = int(pid)

            if pid == net.player_id:
                continue  # kendi oyuncunu tekrar çizme

            ox, oy = pos["x"], pos["y"]

            # Diğer oyuncunun resmi
            img = player_img1 if pid == 1 else player_img2

            screen.blit(img, (ox * TILE_SIZE, oy * TILE_SIZE))

            # Diğeri kazandı mı?
            if (ox, oy) == TREASURE_POS:
                win_screen(f"Player {pid} kazandı!")
                return

        # KONTROL
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return

            if e.type == pygame.KEYDOWN:
                dx = dy = 0
                if e.key == pygame.K_UP: dy = -1
                if e.key == pygame.K_DOWN: dy = 1
                if e.key == pygame.K_LEFT: dx = -1
                if e.key == pygame.K_RIGHT: dx = 1
                if e.key == pygame.K_ESCAPE:
                    return

                nx, ny = x + dx, y + dy

                if not maze.is_wall(nx, ny):
                    x, y = nx, ny
                    steps += 1

                    # Sunucuya sadece pozisyon gönderiyoruz
                    net.send_position(x, y)

                    # Sen kazandın mı? 
                    if (x, y) == TREASURE_POS:
                        win_screen(f"Player {net.player_id}--{steps} adımda kazandı!")
                        return

        pygame.display.flip()
        clock.tick(FPS)




def win_screen(text):
    while True:
        screen.fill((0,120,0))
        draw_text(text,SCREEN_HEIGHT//2)
        draw_text("Devam etmek için ESC", SCREEN_HEIGHT//2 + 60)
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_ESCAPE:
                    return    
menu()



