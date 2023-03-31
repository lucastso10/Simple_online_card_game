import socket
import threading
import time
from classes import Card, Player, Client, HostGame, ClientGame

PORT = 5050
BUFFER_SIZE = 1024

# stage where players connect to game
def readyStage(server, game):
  while not game.started:
    try:
      conn, addr = server.accept()
    except TimeoutError:
      continue

    name = None
    while not name:
      name = conn.recv(BUFFER_SIZE)
      if name:
        message = f"You've connected succesfully {name.decode('UTF-8')}!"
        conn.send(message.encode('UTF-8'))
        
    player = Client(name.decode('UTF-8'), (conn, addr))
    print(f"\nPlayer connected! {player.name}")
    game.players.append(player)

  # multicasts players list
  players_string = ""
  for player in game.players:
    players_string += player.name + ";"
  for player in game.players:
    if type(player) == Player:
      continue
    player.addr[0].send(players_string[:-1].encode('UTF-8'))

  time.sleep(0.5)
  # multicasts first card of the game
  card = str(game.currentCard.cardType) + ";" + str(game.currentCard.attribute)
  for player in game.players:
    if type(player) == Player:
      continue
    player.addr[0].send(card.encode('UTF-8'))
    

def server():
  # grabs the local ip of the machine
  SERVER_IP = socket.gethostbyname(socket.gethostname())

  # starting server
  server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server.bind((SERVER_IP, PORT))

  # creates a player and a game
  print("Please insert your name: ")
  name = input()
  player = Player(name)
  game = HostGame(player)

  # starts the ready stage
  server.settimeout(0.2)
  server.listen()
  thread = threading.Thread(target=readyStage, args=(server, game))
  thread.start()
  
  print(f"Tell your friends to connect to {SERVER_IP}")
  print("Press enter when all of them connected!")
  input()
  game.started = True
  if len(game.players) == 0:
    print("Sorry but you need some friends to play!")
    return
  
  server.settimeout(0)

  time.sleep(1)

  while game.started:
    game.runRound()
  
  return

def client():
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  
  print("Please type the server IP: ")
  valid = False
  while not valid:
    SERVER_IP = input()
    try:
      client.connect((SERVER_IP, PORT))
      valid = True
    except:
      print("Please type a valid ip addres!")
    
  print("please type your name:")
  name = input()
  client.send(name.encode('UTF-8'))
  data, addr = client.recvfrom(BUFFER_SIZE)
  print(f"{data.decode('UTF-8')}")

  time.sleep(0.5)
  
  # wait to receive player list
  players_list, addr = client.recvfrom(BUFFER_SIZE)
  player = Player(name)
  players_list = players_list.decode('UTF-8').split(";")

  # receives the first card of the game
  current_card, addr = client.recvfrom(BUFFER_SIZE)
  current_card = current_card.decode('UTF-8').split(";")
  current_card = Card(current_card[0], current_card[1])
  game = ClientGame(client, player, players_list, current_card)

  # Game
  while data[0] != "0":
    data, addr = game.client.recvfrom(BUFFER_SIZE)
    data = data.decode('UTF-8').split(";")
    game.interpreter(data)
  client.close()
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
