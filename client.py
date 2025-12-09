import socket
import json
import threading
import pygame
from settings import TILE_SIZE

class NetworkPlayer:
    def __init__(self,host,port):
        self.socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.connect((host,port))
    
        data=json.loads(self.socket.recv(1024).decode())

        self.player_id=data["player_id"]
        self.start_x = data["start_x"]
        self.start_y = data["start_y"]

        print("ID:",self.player_id)

        self.other_players = {}   # diğer oyuncuların konumu

        threading.Thread(target=self.listen_server, daemon=True).start()

    def send_position(self,x,y):
        msg=json.dumps({"x": x,"y": y})
        self.socket.send(msg.encode())


    def listen_server(self):
     buffer = ""
     while True:
        try:
            data = self.socket.recv(1024).decode()
            if not data:
                break

            buffer += data

            while "\n" in buffer:
                packet, buffer = buffer.split("\n", 1)
                if packet.strip():
                    data = json.loads(packet)
                   # kendi oyuncunu listeden çıkar
                    if str(self.player_id) in data:
                        data.pop(str(self.player_id))

                    self.other_players = data

        except:
            break
    
        
    def get_other_players(self):
        return self.other_players   