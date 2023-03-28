from random import choice, randint

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
  def __init__(self, cardType, attribute):
    self.cardType = cardType
    self.attribute = attribute
      
  def __str__(self):
    return f"{self.cardType} {self.attribute}"

  def playable(self, card):
    if self.cardType == "S":
      return True
    elif self.cardType == card.cardType:
      return True
    elif self.attribute == card.attribute:
      return True
    else:
      return False


class Player:
  def __init__(self, name):
    self.name = name
    self.cards = []
      
  def __str__(self):
    return f"{self.name}"

# essa classe só vai existir no servidor e não nos clientes
class HostGame:
  # players is a list of ips from other players
  def __init__(self, host : Player):
    self.host = host
    self.players  = []
    self.currentCard = Card(choice(card_types), choice(card_attribute))
    self.currentPlayer = 0
    self.direction = 1
  
  def __str__(self):
    return f"{self.name}"

  # Function to play a card in the game.
  # It treats every type of card calling functions for them
  # if necessary
  def playCard(self, player : Player, card : Card):
    if card.playable():
      self.currentCard = card
      if card.attribute == "B":
        self.block()
      elif card.attribute == "R":
        if self.direction == 1:
          self.direction = -1
        else:
          self.direction = 1
      # combo cards
      elif card.attribute == "+2" or card.attribute == "+4":
        self.nextPlayerBuyCard(card.attribute)
        self.playerChangeColor()
        self.block()
      elif card.attribute == "CC":
        self.playerChangeColor()
      self.nextTurn
    else:
      print("That Card is not playable")

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

  # function for the player to change the current color being played.
  # If a special card changes the color that means it does not have a
  # number, that's why it has a -1 attribute
  def playerChangeColor(self):
    #add a way for the player to input the color they want
    color = "R"
    self.currentCard = Card(color, "-1")

class ClientGame:
  def __init__(self, player : Player):
    self.player  = player
    return
    
