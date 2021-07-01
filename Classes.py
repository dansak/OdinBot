import numpy as np
import pandas as pd

class Game():
    def __init__(self, players):
        self.players = players # List of players in Game
        self.expBoards = [] # List of available exploration boards
        self.houses = [] # List of available houses
        self.specialTiles = [] # List of available special tiles
        self.mountains = self.drawFirstMountains() # List of available mountains
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
        self.gameBoard = GameBoard()
        self.game = None
        
    def playAction(self, Action):
        Action.play()
        
class GameBoard():
    def __init__(self):
        # Tile definitions: X = not placable, F = free, P = free -1 point, O = occupied, B<resource> = bonus resource, I<number> = income added from occupying
        # Tiles are arranged by rows from bottom to top 
        self.income = 0
        self.bonuses = []
        self.tiles = [['I1','F','F','F','F','F','F','P','X','X','X','X','X'],
                      ['F','I1','F','F','F','Bstone','F','P','P','P','P','P','X'],
                      ['F','Bmead','F','F','F','F','F','P','P','P','P','P','X'],
                      ['F','F','F','I1','F','F','F','P','P','P','P','P','X'],
                      ['F','F','Bwood','F','I1','F','Brunestone','P','P','P','P','P'],
                      ['F','F','F','F','F','I1','F','P','P','P','P','P','X'],
                      ['Bore','F','F','F','F','F','I1','P','P','P','P','P','X'],
                      ['P','P','P','P','P','P','P','I1','P','P','P','P','X'],
                      ['P','P','P','P','P','P','P','P','I2','P','P','P','X'],
                      ['P','P','P','P','P','P','P','P','P','I3','P','P','F'],
                      ['P','P','P','P','P','P','P','P','P','P','I3','P','F'],
                      ['P','P','P','P','P','P','P','P','P','P','P','I3','F']]
        
class ExpBoard():
    def __init__(self, expType):
        # Tile definitions: X = not placable, F = free, P = free -1 point, O = occupied, B<resource> = bonus resource, I<number> = income added from occupying
        # Tiles are arranged by rows from bottom to top
        if expType == "Shetland":
            self.income = 0
            self.points = 6
            self.bonuses = []
            self.tiles = [['X','F','F','X','X','X','P','P','F'],
                          ['I1','F','Bbeans','X','X','X','P','P','P'],
                          ['F','I1','F','X','F','P','P','P','F','F','F'],
                          ['F','F','I1','X','P','P','F','Bcabbage','F'],
                          ['X','X','X','X','P','P','F','F','F'],
                          ['P','P','P','P','F','F','F','Boil','F'],
                          ['P','BgameMeat','P','P','F','F','P','P','F'],
                          ['P','P','P','P','F','Bsilverware','F','X','X'],
                          ['X','X','X','X','F','F','F','X','X']]
        
    
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
    def __init__(self, player, cost, reward):
        super(BuildShed, self).__init__(self, player, cost, reward)
        print("Shed")