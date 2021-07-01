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
        self.silver = 0
        self.stone = 0
        self.wood = 0
        self.ore = 0
        self.peas = 0
        self.mead = 0
        self.flax = 0
        self.stockfish = 0
        self.beans = 0
        self.milk = 0
        self.grain = 0
        self.saltMeat = 0
        self.cabbage = 0
        self.gameMeat = 0
        self.fruits = 0
        self.whaleMeat = 0
        self.oil = 0
        self.runeStone = 0
        self.hide = 0
        self.silverware = 0
        self.wool = 0
        self.chest = 0
        self.linen = 0
        self.silk = 0
        self.skinAndBones = 0
        self.spices = 0
        self.fur = 0
        self.jewelry = 0
        self.robe = 0
        self.treasureChest = 0
        self.clothing = 0
        self.silverHoard = 0
        self.sheep = 0
        self.pregnantSheep = 0
        self.cattle = 0
        self.pregnantCattle = 0
        self.vikings = 6
        self.whalingBoat = 0
        self.knarr = 0
        self.longship = 0
        self.penalty = 0
        self.hand = Hand()
        self.expBoards = []
        self.houses = []
        
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
    
   
class Action():
    def __init__(self, player, cost, reward):
        self.cost = cost
        self.reward = reward
        
        
class BuildShed(Action):
    def __init__(self, player, cost, reward:
        super(BuildShed, self).__init__(self, player, cost, reward)
        