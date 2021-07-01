import numpy as np
import pandas as pd
import random

class Game():
    def __init__(self, nPlayers, occupationSet = ['A']):
        # Available exploration boards and stored silver
        self.availableExplorationBoards = {'Shetland':0,'FaroeIslands':0,'Iceland':0,'Greenland':0} 
        
        # Available houses
        self.houses = []
        self.availableSpecialTiles = ['GlassBeads','Helmet','Cloakpin','Belt','Crucifix','DrinkingHorn','AmberFigure','Horesshoe','GoldBrooch','ForgeHammer','Fibula','ThrowingAxe','Chalice','RoundShield','EnglishCrown'] # Available special tiles
        self.availableMountains = [['W','W','W','W','S','S','S2'],
                                   ['W','W','S','S','O','O','S2'],
                                   ['W','W','W','S','O','O','S2'],
                                   ['W','W','S','O','O','S2','S2'],
                                   ['W','W','W','S','S','O','S2'],
                                   ['W','W','W','W','S','O','S2'],
                                   ['W','W','W','S','S','S','S2'],
                                   ['W','W','S','S','S','O','S2']] # Available mountains
        self.mountains = [] # Current Mountains
        self.availableWeapons = ['Sword'] * 11 + ['Bow'] * 12 + ['Spear'] * 12 + ['Snare'] * 12
        self.availableHouses = ['Shed'] * 3 + ['StoneHouse'] * 3 + ['LongHouse'] * 5

        self.round = 1
        self.actions = [] # List of available actions
        self.players = []
        
        for i in range(nPlayers):
            self.players.append(Player(i))
            
        self.turn = random.randint(0, nPlayers - 1)
        self.startingPlayer = None
        
        # Draw first two mountains
        self.drawMountain() 
        self.drawMountain() 
        
        self.availableStartingOccupations = []
        self.availableOccupations = []
        
        # Populate occupations set
        for i in occupationSet:
            if i == 'A':
                self.availableStartingOccupations += ['Farmhand','Sheapherd','Catapulter','Refugee Helper','Proficient Hunter',
                                                      'Apprentice Craftsman','Bosporus Traveler','Forester','Tanner','Slowpoke',
                                                      'Sober Man','Melee Fighter','Woodcutter','Tutor','Craft Leader']
                self.availableOccupations += ['Foreign Trader','Steersman','Helmsman','Linen Weaver','Tradesman','Ship Builder',
                                              'Builder','Ships Cook','Homecomer','Miner','Weapons Supplier','Follower','Dragonslayer',
                                              'Yield Farmer','Shipowner','Fisherman','Ore Boatman','Digger','Farmer','Merchant','Nobleman',
                                              'Whaling Equipper','Hide Buyer','Village Leader','Chief','Sheep Shearer','Spice Merchant',
                                              'Miller','Drunkard','Rune Engraver','Linseed Oil Presser','Peacemaker','Wanderer','Wholesaler',
                                              'Cattle Breeder','Orient Shipper','Barbarian','Armed Fighter','Cowherd','Custodian','Blubber Cook',
                                              'Meat Merchant','Mountain Guard','Priest','Trapper','Preacher','Breeder','Arms Dealer',
                                              'Weapon Supplier','Tutor2','Furrier','Milker','Pea Flour Baker','Fruit Picker','Flax Baker','Peddler']
#            elif i == 'B':
#            elif i == 'C':
                
                

    def harvestPhase(self):
        for i in self.players:           
            if self.round == 2:
                i.peas += 1
                i.flax += 1
                i.beans += 1
                i.grain += 1
            elif self.round == 4:
                i.peas += 1
                i.flax += 1
                i.beans += 1
                i.grain += 1
                i.cabbage += 1
            elif self.round == 6:
                i.peas += 1
                i.flax += 1
                i.beans += 1
                i.grain += 1
                i.cabbage += 1
                i.fruits += 1
                
    def explorationPhase(self):
        if self.round == 3:
            for i in self.availableExplorationBoards:
                self.availableExplorationBoards[i] += 2
            if 'Shetland' in self.availableExplorationBoards:
                del self.availableExplorationBoards['Shetland']
                self.availableExplorationBoards['BearIsland'] = 0
        elif self.round == 4:
            for i in self.availableExplorationBoards:
                self.availableExplorationBoards[i] += 2
            if 'FaroeIslands' in self.availableExplorationBoards:
                del self.availableExplorationBoards['FaroeIslands']
                self.availableExplorationBoards['BaffinIsland'] = 0
        elif self.round == 5:
            for i in self.availableExplorationBoards:
                self.availableExplorationBoards[i] += 2
            if 'Iceland' in self.availableExplorationBoards:
                del self.availableExplorationBoards['Iceland']
                self.availableExplorationBoards['Labrador'] = 0
        elif self.round == 6:
            for i in self.availableExplorationBoards:
                self.availableExplorationBoards[i] += 2
            if 'Greenland' in self.availableExplorationBoards:
                del self.availableExplorationBoards['Greenland']
                self.availableExplorationBoards['Newfoundland'] = 0            
                
    def drawWeaponPhase(self):
        for i in self.players:
            self.drawWeapon(i, 1)
            
    def determineStartingPlayerPhase(self):
        self.turn = self.startingPlayer
            
    def incomePhase(self):
        for i in self.players:
            i.resources['Silver'] += i.income
        
    def breedingPhase(self):
        for i in self.players:
            if i.resources['PregnantSheep'] > 0:
                i.resources['Sheep'] += i.resources['PregnantSheep'] + 1
                i.resources['PregnantSheep'] = 0
            elif i.resources['Sheep'] >= 2:
                i.resources['PregnantSheep'] += 1
                i.resources['Sheep'] -= 1
            if i.resources['PregnantCattle'] > 0:
                i.resources['Cattle'] += i.resources['PregnantCattle'] + 1
                i.resources['PregnantCattle'] = 0
            elif i.resources['Cattle'] >= 2:
                i.resources['PregnantCattle'] += 1
                i.resources['Cattle'] -= 1   
            
    def feastPhase(self):
        for i in self.players:
            # Check feast logic
            print('Feast Logic')
                
    def bonusPhase(self):
        for i in self.players:
            for j in i.bonuses:
                if j == 'StoneHouse':
                    i.houses.append(House('StoneHouse'))
                elif j == 'Cloakpin':
                    if j in self.availableSpecialTiles:
                        self.availableSpecialTiles.remove(j)
                        i.resources[j] += 1
                else:
                    i.resources[j] += 1
    
    def mountainPhase(self):
        for i in self.mountains:
            if len(i) > 0:
                i.pop(0)
        self.drawMountain   

    def returnVikingsPhase(self):
        for i in self.players:
            i.vikings = self.round + 6    
        self.round += 1            
                        
            
    def drawWeapon(self, player, nWeapons):
        for i in range(nWeapons):
            # If no weapons available, refresh weapon deck with default deck removing weapons already in players' supply
            if len(self.availableWeapons) == 0:                
                usedSwords = 0
                usedBows = 0
                usedSpears = 0
                usedSnares = 0
                for j in self.players:
                    usedSwords += j.Swords
                    usedBows += j.Bows
                    usedSpears += j.Spears
                    usedSnares += j.Snares
                    
                self.availableWeapons = ['Sword'] * (11 - usedSwords) + ['Bow'] * (12 - usedBows) + ['Spear'] * (12 - usedSpears) + ['Snare'] * (12 - usedSnares)
                                                       
            weapon = self.availableWeapons.pop(random.randint(0, len(self.availableWeapons) - 1))
            if weapon == 'Sword':
                player.Sword += 1
            elif weapon == 'Bow':
                player.Bow += 1
            elif weapon == 'Spear':
                player.Spear += 1
            elif weapon == 'Snare':
                player.Snare += 1          
                        
    def drawMountain(self):
        self.mountains.append(self.availableMountains.pop(random.randint(0, len(self.availableMountains) - 1)))
    
                
    def passTurn(self, player):
        if self.startingPlayer == None:
            self.startingPlayer = player.ID
        player.passed = True

    def buildShed(self, player):
        if player.passed == True:
            print('Player already passed!')
        if self.turn == player.ID:
            if 'Shed' in self.availableHouses:
                self.availableHouses.remove('Shed')
                player.houses.append(House('Shed'))
            else:
                print('No Shed\'s Available!')
        else:
            print('It is player ' + str(self.turn) + '\'s turn, not player ' + str(self.playerID) + '\'s!')
            
                       
    
class Player():
    def __init__(self, ID):
        self.ID = ID
        self.vikings = 6
        self.passed = False
        self.whalingBoats = []
        self.knarrs = []
        self.longships = []
        self.penalty = 0
        self.occupations = []
        self.expBoards = []
        self.houses = []
        self.bonuses = []
        self.feastTable = dict()
        self.playerBoard = PlayerBoard()
      
        self.resources = {'Silver':0, 'Stone':0, 'Wood':0, 'Ore':0, 'Peas':1, 'Mead':1, 'Flax':1, 'Stockfish':0, 'Beans':1, 'Milk':0, 
                          'Grain':0, 'SaltMeat':0, 'Cabbage':0, 'GameMeat':0, 'Fruits':0, 'WhaleMeat':0, 'Oil':0, 'RuneStone':0, 'Hide':0, 'Silverware':0, 'Wool':0, 
                          'Chest':0, 'Linen':0, 'Silk':0, 'SkinAndBones':0, 'Spices':0, 'Fur':0, 'Jewelry':0, 'Robe':0, 'TreasureChest':0, 'Clothing':0, 'SilverHoard':0, 
                          'Sheep':0, 'PregnantSheep':0, 'Cattle':0, 'PregnantCattle':0, 'Swords':0, 'Bows':0, 'Spears':0, 'Snares':0}
    
        
class PlayerBoard():
    def __init__(self):
        self.income = 0
        self.bonuses = []
        # Tile definitions: X = not placable, F = free, P = free -1 point, O = occupied, B<resource> = bonus resource, I<number> = income added from occupying
        # Tiles are arranged by rows from bottom to top 
        self.tiles = [['I1','F','F','F','F','F','F','P','X','X','X','X','X'],
                      ['F','I1','F','F','F','BStone','F','P','P','P','P','P','X'],
                      ['F','BMead','F','F','F','F','F','P','P','P','P','P','X'],
                      ['F','F','F','I1','F','F','F','P','P','P','P','P','X'],
                      ['F','F','BWood','F','I1','F','BRuneStone','P','P','P','P','P'],
                      ['F','F','F','F','F','I1','F','P','P','P','P','P','X'],
                      ['BOre','F','F','F','F','F','I1','P','P','P','P','P','X'],
                      ['P','P','P','P','P','P','P','I1','P','P','P','P','X'],
                      ['P','P','P','P','P','P','P','P','I2','P','P','P','X'],
                      ['P','P','P','P','P','P','P','P','P','I3','P','P','F'],
                      ['P','P','P','P','P','P','P','P','P','P','I3','P','F'],
                      ['P','P','P','P','P','P','P','P','P','P','P','I3','F']]
        
class ExpBoard():
    def __init__(self, expType):
        self.storedSilver = 0
        # Tile definitions: X = not placable, F = free, P = free -1 point, O = occupied, B<resource> = bonus resource, I<number> = income added from occupying
        # Tiles are arranged by rows from bottom to top
        if expType == 'Shetland':
            self.income = 0
            self.points = 6
            self.tiles = [['X','F','F','X','X','X','P','P','F'],
                          ['I1','F','BBeans','X','X','X','P','P','P'],
                          ['F','I1','F','X','F','P','P','P','F','F','F'],
                          ['F','F','I1','X','P','P','F','BCabbage','F'],
                          ['X','X','X','X','P','P','F','F','F'],
                          ['P','P','P','P','F','F','F','Boil','F'],
                          ['P','BGameMeat','P','P','F','F','P','P','F'],
                          ['P','P','P','P','F','BSilverware','F','X','X'],
                          ['X','X','X','X','F','F','F','X','X']]
        elif expType == 'FaroeIslands':
            self.income = 0
            self.points = 4
            self.tiles = [['X','X','X','X','X','F','F','P'],
                          ['F','F','F','F','X','F','BHide','P'],
                          ['BPeas','I1','F','F','X','F','F','P'],
                          ['F','F','F','X','F','BFlax','P','P','X'],
                          ['X','X','X','I1','F','F','P','X','F'],
                          ['X','F','F','F','F','P','P','P','P'],
                          ['X','P','BOil','F','F','F','X','F','BMilk'],
                          ['X','X','P','P','X','X','I1','F','P'],
                          ['X','X','X','X','X','P','BSheep','I1','P']]
        elif expType == 'Iceland':
            self.income = 1
            self.points = 16
            self.tiles = [['X','X','P','P','F','X','X','X'],
                          ['F','I1','P','P','F','BOreStone','F','X'],
                          ['F','F','I1','P','F','F','F','P'],
                          ['BOil','F','F','I1','P','P','P','P'],
                          ['F','F','F','F','I1','P','P','P','P'],
                          ['X','F','BStockfish','F','P','I1','P','P'],
                          ['P','F','X','F','P','P','I1','P'],
                          ['F','P','X','P','F','P','P','I1']]
        elif expType == 'Greenland':
            self.income = 0
            self.points = 12
            self.tiles = [['X','X','X','X','F','F','F','X'],
                          ['X','X','F','I1','F','F','F','X'],
                          ['X','P','P','P','I1','X','F','BStockfish'],
                          ['F','P','F','P','P','I1','F','F'],
                          ['F','F','F','P','P','P','I1','X'],
                          ['F','bWhaleMeat','F','I1','P','P','P','I1'],
                          ['F','F','F','X','I1','P','P','P'],
                          ['P','P','P','F','F','I1','P','P']]
        elif expType == 'BearIsland':
            self.income = 1
            self.points = 12
            self.tiles = [['X','X','X','X','P','P','X','X'],
                          ['X','X','X','F','P','F','F','X'],
                          ['X','F','F','F','F','F','BRuneStoneStone','X'],
                          ['X','F','F','F','F','F','P','P','X'],
                          ['X','I2','X','F','F','P','F','BStockfish'],
                          ['F','F','I1','F','BGameMeat','F','P','F'],
                          ['P','P','P','I1','F','P','F','P'],
                          ['X','P','P','P','X','P','P','P'],
                          ['X','X','X','P','P','P','P','X']]
        elif expType == 'BaffinIsland':
            self.income = 0
            self.points = 12
            self.tiles = [['F','F','F','X','P','F','BSkinAndBones','F','P'],
                          ['F','I1','F','F','P','F','F','X','X'],
                          ['X','F','F','F','P','P','X','X','X'],
                          ['F','F','F','I2','P','P','P','Boil','P'],
                          ['X','F','F','F','I2','P','P','X','X'],
                          ['X','P','X','P','F','X','X','X','F'],
                          ['X','F','P','F','P','P','F','BWhaleMeat','F'],
                          ['P','P','F','P','P','P','F','F','F'],
                          ['P','F','P','P','BOre','X','X','X','X']]
        elif expType == 'Labrador':
            self.income = 0
            self.points = 36
            self.tiles = [['X','P','X','P','F','P','BStockfish','P','P'],
                          ['P','BLinen','P','F','P','F','P','P','P','P'],
                          ['F','P','F','P','BChest','P','X','P','X'],
                          ['P','P','P','F','P','P','P','P','P'],
                          ['X','X','P','P','P','P','P','P','P'],
                          ['X','X','X','BGameMeat','P','P','F','P','X'],
                          ['X','X','X','P','F','P','X','X','X'],
                          ['X','X','X','P','P','P','X','X','X'],
                          ['X','X','X','P','P','X','X','X','X']]
        elif expType == 'Newfoundland':
            self.income = 0
            self.points = 38
            self.tiles = [['X','X','X','X','X','P','X','P','P'],
                          ['P','P','P','F','P','P','P','P','P'],
                          ['F','P','F','P','P','P','BStoneHouse','P','X'],
                          ['P','BCloakpin','P','F','P','F','P','P','P'],
                          ['X','F','P','F','P','P','P','X','X'],
                          ['X','P','BSkinAndBones','P','X','P','P','X','X'],
                          ['X','X','P','P','X','X','X','X','X'],
                          ['X','X','P','P','P','X','X','X','X']]

            
class House():
    def __init__(self, houseType):
        # Tile definitions: X = not placable, F = free, P = free -1 point, O = occupied, B<resource> = bonus resource, I<number> = income added from occupying
        # Tiles are arranged by rows from bottom to top 
        if houseType == 'Shed':
            self.points = 8            
            self.tiles = [['X']]
            self.WoodSlots = 3
            self.StoneSlots = 3
        elif houseType == 'StoneHouse':
            self.points = 10
            self.tiles = [['X','F','P','X','X'],
                          ['P','F','BHide','P','X'],
                          ['X','P','F','F','P'],
                          ['X','X','P','F','P']]
            self.WoodSlots = 1
            self.StoneSlots = 1
        elif houseType == 'LongHouse':
            self.ponts = 17
            self.tiles = [['F','P','F','P','F','P','F','P','F','P','BPeas'],
                          ['P','BOil','P','X','P','F','P','X','P','F','P'],
                          ['F','P','F','P','F','BBeans','F','P','F','P','X']]
            self.WoodSlots = 0
            self.StoneSlots = 0        

class Boat():
    def __init__(self, boatType):
        self.ore = 0
        if boatType == 'WhalingBoat':
            self.points = 3
            self.maxOre = 1
        elif boatType == 'Knarr':
            self.points = 5
            self.maxOre = 0
        elif boatType == 'Longship':
            self.points = 8
            self.maxOre = 3
        