import numpy as np
import pandas as pd

class Board():
    def __init(self, players, turn):
        self.players = players # List of players in Game
        self.turn = turn # Who's turn
        self.expBoards = [] # List of available exploration boards
        self.houses = [] # List of available houses
        self.specialTiles = [] # List of available special tiles
        self.mountains = drawFirstMountains() # List of available mountains
        self.actions = [] # List of available actions
        
        def drawFirstMountains(self):
            return None 

class Player():
    def __init__(self):
        self.resources = [] # List of resources
        self.hand = Hand()
        
    def playAction(self, Action):
        Action.play()
        
    
class Hand():
    def __init__(self):
        self.cards = []
        
    def add(self, card):
        self.cards.append(card)
        
class Card():
    def __init__(self):
        print("Card")

class Occupation(Card):
    def __init__(self):
        print("Occ")
    
class Weapon(Card):
    def __init__(self, wepType):
        self.wepType = wepType
    
class Resource():
    print("Res")
    
class Action():
    def __init__(self, player, cost, reward):
        self.cost = cost
        self.reward = reward
        
    def play(self):
        print("Play")
        
class BuildShed(Action):
    def __init__(self, player, cost, reward:
        super(BuildShed, self).__init__(self, player, cost, reward)
        