
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

    
