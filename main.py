import socket
import game.py

PORT = 5050


def server():
  # grabs the local ip of the machine
  SERVER_IP = socket.gethostbyname(socket.gethostname())

  # starting server
  server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server.bind((SERVER_IP, PORT))

  
  
  print(f"Tell your friends to connect to {SERVER_IP}")
  return

def main():
  print("Please select if you are a client or a server:\n1.Server\n2.Client\n0.Exit")
  x = ""
  while (x != "0"):
    x = input()
    if x == "1":
      server()
    elif x == "2":
      return
    elif x == "0":
      print("Thank you for playing!")
    else:
      print("Please type a valid number!")
      
  return


if __name__ == "__main__":
    main()
