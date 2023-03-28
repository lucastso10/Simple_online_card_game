import socket
import threading
from classes import Card, Player, HostGame, ClientGame

PORT = 5050

def createPlayer():
  print("Please insert your name: ")
  name = input()
  player = Player(name)
  return player

def readyStage(server, game):
  while True:
    conn, addr = server.accept()
    print(f"Player connected! ({conn}, {addr})")
    game.players.append((conn, addr))

def server():
  # grabs the local ip of the machine
  SERVER_IP = socket.gethostbyname(socket.gethostname())

  # starting server
  server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server.bind((SERVER_IP, PORT))

  # creates a player and a game
  player = createPlayer()
  game = HostGame(player)

  # starts the ready stage
  server.listen()
  thread = threading.Thread(target=readyStage, args=(server, game))
  thread.start()
  
  print(f"Tell your friends to connect to {SERVER_IP}")
  print("Press enter when all of them connected!")
  input()
  thread.stop()
  return

def client():
  print("Please type the server IP: ")
  SERVER_IP = input()
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client.connect((SERVER_IP, PORT))
  return

def main():
  print("Please select if you are a client or a server:\n1.Server\n2.Client\n0.Exit")
  x = ""
  while (x != "0"):
    x = input()
    if x == "1":
      server()
      return
    elif x == "2":
      client()
      return
    elif x == "0":
      print("Thank you for playing!")
    else:
      print("Please type a valid number!")
      
  return


if __name__ == "__main__":
    main()
