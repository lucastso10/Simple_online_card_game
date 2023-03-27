import card.py

class Player:
    def __init__(self, name):
        self.name = name
        self.cards = []
        
    def __str__(self):
        return f"{self.name}"
