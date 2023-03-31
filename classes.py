import socket
from random import choice

# R = Red
# G = Green
# B = Blue
# Y = Yellow
# S = Special
card_types = ["R", "G", "B", "Y", "S"]

# R = Reverse
# B = Block
card_attribute = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "R", "B", "+2"]

# CC = Change Color
special_cards = ["+4", "CC"]

class Card:
  def __init__(self, type, attribute):
    self.cardType = type
    self.attribute = attribute
      
  def __str__(self):
    return f"{self.cardType};{self.attribute}"

  def playable(self, card):
    if self.cardType == "S":
      return True
    elif self.cardType == card.cardType:
      return True
    elif self.attribute == card.attribute:
      return True
    else:
      return False

# ========================================================================
      
# every client and the server has its own unique player
class Player:
  def __init__(self, name):
    self.name = name
    self.cards = []
    # every player starts with 7 cards
    for i in range(0,6):
      self.buyCard()
      
  def __str__(self):
    return f"{self.name}"

  # I wanna alter this in the future to mess with the probability of getting a special card
  def buyCard(self):
    type = choice(card_types)

    if type == "S":
      attribute = choice(special_cards)
    else:
      attribute = choice(card_attribute)
      
    self.cards.append(Card(type, attribute))

  def cardsToString(self):
    cards_string = ""
    for card in self.cards:
      cards_string += f"{card} |"
    return cards_string[:-2]

  def cardsToList(self):
    card_string = ""
    card_list = []
    for card in self.cards:
      card_string = f"{card}"
      card_list.append(card_string)
      
    return card_list

# ========================================================================

class Client:
  def __init__(self, name, addr):
    self.name = name
    self.addr = addr
    self.cardQnt = 7
      
  def __str__(self):
    return f"{self.name} ({self.addr})"


# ========================================================================
    
# this class only exists in the server and it dictates how the game will play out
# every round it's gonna tell its state to every client letting them adapt accordingly
class HostGame:
  # players is a list of ips from other players
  def __init__(self, host : Player):
    self.host = host
    self.players  = []
    self.currentCard = Card(choice(card_types[0:3]), choice(card_attribute))
    # since the Client and Player are different classes I decided to not include the host on the players list
    # having their round be played when currentPlayer is set to -1
    self.currentPlayer = -1
    self.direction = 1
    self.started = False
  
  def printRound(self):
    players_list = self.host.name + " | "
    for player in self.players:
      players_list += player.name + " " + player.cardQnt +" | "
      
    if self.currentPlayer >= 0:
      return f"{players_list}\n\nIt is {self.players[self.currentPlayer]}'s turn:\n{self.currentCard}"
    else:
      return f"{players_list}\n\nIt is your turn, {self.host.name}!:\n{self.currentCard}"

  # Function to play a card in the game.
  # It treats every type of card calling functions for them
  # if necessary
  def playCard(self, card : Card):
    self.currentCard = card
    
    if card.attribute == "B":
      self.block()
      
    elif card.attribute == "R":
      if self.direction == 1:
        self.direction = -1
      else:
        self.direction = 1
        
    elif card.attribute == "+2" or card.attribute == "+4":
      self.nextPlayerBuyCard(card.attribute)
      pass
      
    self.nextTurn()

  # it changes to the next turn by moving the currentPlayer
  # depeding on the direction of the game
  def nextTurn(self):
    self.currentPlayer += self.direction
    if self.currentPlayer == len(self.currentPlayer):
      self.currentPlayer = 0
    elif self.currentPlayer == -1:
      self.currentPlayer = len(self.currentPlayer) - 1

  # it does the same as nextTurn, it is just to clarify
  def block(self):
    self.nextTurn()

# ========================================================================

class ClientGame:
  def __init__(self, client : socket, player : Player, players, card : Card):
    self.client = client
    self.clientPlayer = player
    self.nextPlayer = 1
    self.players = players
    self.currentCard = card
    self.playersQtdCards = []
    for i in range (1, len(self.players)):
      self.playersQtdCards.append(7)
    return

  # print the round and if it is the player turn calls clientPlay
  def printRound(self, round):
    players_list = self.clientPlayer.name + " | "
    for i in range(0, len(self.players) - 1):
      players_list += self.players[i] + " " + self.playersQtdCards[i] +" | "
      
    if self.players[int(round)] >= self.clientPlayer.name :
      print(f"{players_list}\nNext player is {self.players[self.nextPlayer]}\n\nIt is {self.players[int(round)]}'s turn:\n{self.currentCard}\n\nYour cards: {self.clientPlayer.cardsToString()}")
      self.clientPlay()
    else:
      print(f"{players_list}\nNext player is {self.players[self.nextPlayer]}\n\nIt is your turn, {self.clientPlayer.name}!:\n{self.currentCard}\n\nYour cards: {self.clientPlayer.cardsToString()}")

  # client buys card
  def clientBuyCard(self):
    self.clientPlayer.buyCard()
    print(f"\n{self.currentCard}\n\nYour cards: {self.clientPlayer.cardsToString()}")

  # Client play cards
  def clientPlay(self):
    valid = False
    while valid:
      print("Type the card you want to play (type;attribute example: R;+2) (if you want to buy a card type B):")
      card = input()

      card.upper()

      if card == "B":
        self.clientBuyCard()
        continue

      if card not in self.players.cardsToList():
        print("Please type a card that you have!")
        continue

      card = card.split(";")

      card = Card(card[0], card[1])

      if not card.isPlayable(self.currentCard):
        print("This card is not playable")
        continue

      valid = True
    message = str(len(self.clientPlayer.cards)) + ";" + card.cardType + ";" + card.attribute
    self.client.send(message.enconde('UTF-8'))

  # interpretes messages sent by the server and does what is needed
  # for a reference for every message please refer to messages.txt
  def interpreter(self, message):
    if message[0] == "1":
      self.playersQtdCards[int(message[1])] = int(message[2])
      self.nextPlayer = int(message[3])
      self.currentCard = Card(message[5], message[6])

      self.printRound(message[4])
        
    elif message[0] == "2":
      if self.players[int(message[1])] == self.clientPlayer.name:
        print("you have been blocked!")
      else:
        print(f"{self.players[self.nextPlayer]} has been blocked!")
    elif message[0] == "3":
      if self.players[int(message[1])] == self.clientPlayer.name:
        for i in range(1,message[2]):
          self.clientPlayer.buyCard()
        print(f"You've bought {message[2]} cards!")
      else:
        print(f"{self.players[self.nextPlayer]} bought {message[2]} cards!")
    elif message[0] == "0":
      if self.players[int(message[1])] == self.clientPlayer.name:
        print("You have won!")
      else:
        print(f"{self.players[int(message[1])]} won the game!")
    