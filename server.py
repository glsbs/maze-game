import socket
import threading
import json

HOST="0.0.0.0"
PORT=5000

players={
    1: { "x":1,"y":1},
    2: {"x":1,"y":2}
}

connections={}

def handle_player(conn, player_id):
    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break

            msg = json.loads(data)
            players[player_id]["x"] = msg["x"]
            players[player_id]["y"] = msg["y"]

            # TÜM OYUNCULARA GÖNDER
            for c in connections.values():
                try:
                    c.send((json.dumps(players) + "\n").encode())
                except:
                    pass

        except:
            break

    conn.close()

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((HOST,PORT))
server.listen(2)

print("Server hazır... Oyuncular bekleniyor...")

player_id=1

while player_id<=2:
    conn,addr=server.accept()
    print("Bağlanan:",addr)

    connections[player_id]=conn

    conn.send(json.dumps({
        "player_id": player_id,
        "start_x": players[player_id]["x"],
        "start_y": players[player_id]["y"]
    }).encode()+ b"\n")
    
    threading.Thread(target=handle_player,args=(conn,player_id)).start()
    player_id+=1
