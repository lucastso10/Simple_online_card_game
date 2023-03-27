
class Card:
    def __init__(self, cardType, attribute):
        self.cardType = cardType
        self.attribute = attribute
        
    def __str__(self):
        return f"{self.cardType} {self.attribute}"


class Player:
    def __init__(self, name):
        self.name = name
        self.cards = []
        
    def __str__(self):
        return f"{self.name}"
