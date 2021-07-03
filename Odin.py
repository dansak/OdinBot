import numpy as np
import pandas as pd
import random

class Game():
    def __init__(self, nHumanPlayers = 1, nBotPlayers = 0, occupationSet = ['A']):
        # Available exploration boards and stored silver
        self.availableExplorationBoards = {'Shetland':0,'FaroeIslands':0,'Iceland':0,'Greenland':0} 
        
        # Available houses
        self.houses = []
        
        # Available Sepcial Tiles
        self.availableSpecialTiles = ['GlassBeads','Helmet','Cloakpin','Belt','Crucifix','DrinkingHorn','AmberFigure','Horesshoe','GoldBrooch','ForgeHammer','Fibula','ThrowingAxe','Chalice','RoundShield','EnglishCrown'] # Available special tiles
        
        # Available mountains
        self.availableMountains = [['W','W','W','W','S','S','S2'],
                                   ['W','W','S','S','O','O','S2'],
                                   ['W','W','W','S','O','O','S2'],
                                   ['W','W','S','O','O','S2','S2'],
                                   ['W','W','W','S','S','O','S2'],
                                   ['W','W','W','W','S','O','S2'],
                                   ['W','W','W','S','S','S','S2'],
                                   ['W','W','S','S','S','O','S2']] 
        
        # Current Mountains in play
        self.mountains = [] 
        
        # Available Weapons
        self.availableWeapons = ['Sword'] * 11 + ['Bow'] * 12 + ['Spear'] * 12 + ['Snare'] * 12
        
        # Available Houses
        self.availableHouses = ['Shed'] * 3 + ['StoneHouse'] * 3 + ['LongHouse'] * 5
        
        # Available action spaces
        self.availableActions = ['BuildShed','BuildStoneHouse','BuildLongHouse']
        
        # Available anytime actions
        self.availableAnytimeActions = ['PlaceFeast','PlaceTile','BuyBoat','Arming']

        # Current round
        self.round = 1
        
        # Populate players in game
        self.players = []
        for i in range(nHumanPlayers + nBotPlayers):
            self.players.append(Player(i))
            
        # Determine who goes first
        self.turn = random.randint(0, nHumanPlayers + nBotPlayers - 1)
        
        # Initialize starting player token which will be assigned when the first person passes
        self.startingPlayer = None
        
        # Draw first two mountains
        self.drawMountain() 
        self.drawMountain() 
        
        # Available occupations to draw
        self.availableStartingOccupations = []
        self.availableOccupations = []
        
        # Populate occupations set
        for i in occupationSet:
            if i == 'A':
                self.availableStartingOccupations += ['Farmhand','Sheapherd','Catapulter','RefugeeHelper','ProficientHunter',
                                                      'ApprenticeCraftsman','BosporusTraveler','Forester','Tanner','Slowpoke',
                                                      'SoberMan','MeleeFighter','Woodcutter','Tutor','CraftLeader']
                self.availableOccupations += ['ForeignTrader','Steersman','Helmsman','LinenWeaver','Tradesman','ShipBuilder',
                                              'Builder','ShipsCook','Homecomer','Miner','WeaponsSupplier','Follower','Dragonslayer',
                                              'YieldFarmer','Shipowner','Fisherman','OreBoatman','Digger','Farmer','Merchant','Nobleman',
                                              'WhalingEquipper','HideBuyer','VillageLeader','Chief','SheepShearer','SpiceMerchant',
                                              'Miller','Drunkard','RuneEngraver','LinseedOilPresser','Peacemaker','Wanderer','Wholesaler',
                                              'CattleBreeder','OrientShipper','Barbarian','ArmedFighter','Cowherd','Custodian','BlubberCook',
                                              'MeatMerchant','MountainGuard','Priest','Trapper','Preacher','Breeder','ArmsDealer',
                                              'WeaponSupplier','Tutor2','Furrier','Milker','PeaFlourBaker','FruitPicker','FlaxBaker','Peddler']
            elif i == 'B':
                self.availableStartingOccupations += ['DisheartenedWarrior','Collector','Undertaker','Barkeep','Steward','Princess','FineBlacksmith',
                                                      'MeatCurer','Angler','BeanFarmer','Cooper','Milkman','Middleman','FarmShopOwner','Berserker']
                self.availableOccupations += ['CodliverOilPresser','HarborGuard','FestiveHunter','WeaponsWarden','WhalingAssistant','Judge',
                                              'Warmonger','TravelingMerchant','MeatTrader','MasterMason','Earl','WhaleCatcher','CutterOperator',
                                              'SilkMerchant','PeaCounter','Seafarer','Deerstalker','Courier','Maid','Locksmith','StoneCrusher',
                                              'LanceBearer','EtiquetteTeacher','MasterTailor','KnarrBuilder','MasterJoiner','SheapherdBoy','LongshipBuilder',
                                              'FurMerchant','Aventurer','BoatBuilder','BosporusMerchant','Carpenter','Punchcutter','DorestadTraveller',
                                              'Chronicler','Laborer','AntlersSeller','Stonecarver','Archer','Taster','ShipArchitect','MeatPreserver','MasterCount']
            elif i == 'C':
                self.availableStartingOccupations += ['Hunter','Robber','MeatInspector','TridentHunter','Raider','ThingSpokesman','Messenger','Latecomer',
                                                      'MasterBricklayer','Scribe','IvorySculptor','Ironsmith','MeatBuyer','EquipmentSupplier','BaitLayer']
                self.availableOccupations += ['PrivateChef','Skinner','Sponsor','Modifier','Artist','Inspector','Sower','Pirate','Metasmith',
                                              'ShipOwner','Cottager','Innkeeper','Plower','Treasurer','FishCook','BoneCollector','HelperInNeedOfTime',
                                              'SwordFighter','Captain','Hornturner','SilkSticher','BeachRaider','HerbGardener','GrainDeliveryman',
                                              'BirkaSettler','Storeman','SpiceMerchant2','Clerk','Quartermaster','ForestBlacksmith','Sledger',
                                              'SympatheticSoul','Patron','SailPatcher','LootHunter','OilSeller','EarlofLade','FlaxFarmer','SnareSpecialist',
                                              'WharfOwner','Host','Hornblower','Mineworker','Fighter']
                
        # Draw each player a starting occupation card and starting weapons
        for i in self.players:
            i.occupations.append(self.availableStartingOccupations.pop(random.randint(0, len(self.availableStartingOccupations) - 1)))
            
            i.resources['Bow'] += 1
            i.resources['Spear'] += 1
            i.resources['Snare'] += 1
            
            self.availableWeapons.remove('Bow')
            self.availableWeapons.remove('Spear')
            self.availableWeapons.remove('Snare')
            
            i.resources[self.availableWeapons.pop(random.randint(0, len(self.availableWeapons) - 1))] += 1

                
                

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
    
    # Pass the turn to the next player
    def passTurn(self, player):
        if player.madeAction:
            self.turn += 1
            if self.turn > len(self.players) - 1:
                self.turn = 0
        else:
            print('You need to make an action before passing!')
        
     # Completely end turn for the round          
    def endTurn(self, player):
        if self.startingPlayer == None:
            self.startingPlayer = player.ID
        player.endedTurn = True
        
    # Take an action or anytime action
    def takeAction(self, player, action):
        if player.endedTurn:
            print('Player already ended their turn!')
        elif player.madeAction:
            print('Player already made an action this turn!')
        elif action not in self.availableActions + self.availableAnytimeActions:
            print('Action has already been taken this round!')
        elif self.turn == player.ID:
            print('Take Action')
        else:
            print('It is player ' + str(self.turn) + '\'s turn, not player ' + str(self.playerID) + '\'s!')
    
    def determineValidActions(self, player, action):
        player.validActions = []
        if player.resources['Wood'] >= 2 and 'Shed' in self.availableHouses:
            player.validActions += 'BuildShed'
         
    # Returns list of possible board (main and exploration) placements
#    def determineValidBoardPlacement(self, player):
#        tileTemplate
    
    def determineValidHousePlacement(self, player):
        # Name possible tiles: contains info on length; width; missing spots; rotations hor, vert, left, or right(H, V, L, or R); flipped (True or False); and colors (O, R, G, or B)
        tileTemplate = [['Peas',2,1,[],'H',False,'O'],
                        ['Peas',1,2,[],'V',False,'O'],
                        ['Flax',3,1,[],'H',False,'O'],
                        ['Flax',1,3,[],'V',False,'O'],
                        ['Grain',4,1,[],'H',False,'O'],
                        ['Grain',1,4,[],'V',False,'O'],
                        ['Cabbage',3,2,[],'H',False,'O'],
                        ['Cabbage',2,3,[],'V',False,'O'],
                        ['Beans',2,2,[],'H',False,'O'],
                        ['Fruits',3,3,[],'H',False,'O'],
                        ['Mead',2,1,[],'H',False,'R'],
                        ['Mead',1,2,[],'V',False,'R'],
                        ['Stockfish',3,1,[],'H',False,'R'],
                        ['Stockfish',1,3,[],'V',False,'R'],
                        ['SaltMeat',4,1,[],'H',False,'R'],
                        ['SaltMeat',1,4,[],'V',False,'R'],
                        ['GameMeat',3,2,[],'H',False,'R'],
                        ['GameMeat',2,3,[],'V',False,'R'],
                        ['Milk',2,2,[],'H',False,'R'],
                        ['WhaleMeat',3,3,[],'H',False,'R'],
                        ['Oil',2,1,[],'H',False,'G'],
                        ['Oil',1,2,[],'V',False,'G'],
                        ['Hide',3,1,[],'H',False,'G'],
                        ['Hide',1,3,[],'V',False,'G'],
                        ['Linen',4,1,[],'H',False,'G'],
                        ['Linen',1,4,[],'V',False,'G'],
                        ['SkinAndBones',3,2,[],'H',False,'G'],
                        ['SkinAndBones',2,3,[],'V',False,'G'],
                        ['Wool',2,2,[],'H',False,'G'],
                        ['Robe',3,3,[],'H',False,'G'],
                        ['Runestone',2,1,[],'H',False,'B'],
                        ['Runestone',1,2,[],'V',False,'B'],
                        ['Silverware',3,1,[],'H',False,'B'],
                        ['Silverware',1,3,[],'V',False,'B'],
                        ['Silk',4,1,[],'H',False,'B'],
                        ['Silk',1,4,[],'V',False,'B'],
                        ['Spices',3,2,[],'H',False,'B'],
                        ['Spices',2,3,[],'V',False,'B'],
                        ['Chest',2,2,[],'H',False,'B'],
                        ['TreasureChest',3,3,[],'H',False,'B'],
                        ['Silver',1,1,[],'H',False,'B']]      
                    
        tile = []
        
        # Only keep tile the player has
        for i in tileTemplate:
            if player.resources[i[0]] > 0:
                tile.append(i)

#        possiblePlacements = []
        print(tile)
        
        
    # Returns list of possible feast placements
    def determineValidFeastPlacement(self, player):
        # Name possible feast tiles: contains info on length, rotation(H, V, or B), and color (O, R, or B)
        tileTemplate = [['Peas',2,'H','O'],
                ['Flax',3,'H','O'],
                ['Grain',4,'H','O'],
                ['Cabbage',3,'H','O'],
                ['Mead',2,'H','R'],
                ['Stockfish',3,'H','R'],
                ['SaltMeat',4,'H','R'],
                ['GameMeat',3,'H','R'],
                ['Sheep',4,'H','R'],
                ['PregnantSheep',4,'H','R'],
                ['Cattle',4,'H','R'],
                ['PregnantCattle',4,'H','R'],
                ['Peas',1,'V','O'],
                ['Flax',1,'V','O'],
                ['Grain',1,'V','O'],
                ['Cabbage',2,'V','O'],
                ['Mead',1,'V','R'],
                ['Stockfish',1,'V','R'],
                ['SaltMeat',1,'V','R'],
                ['GameMeat',2,'V','R'],
                ['Sheep',2,'V','R'],
                ['PregnantSheep',2,'V','R'],
                ['Cattle',3,'V','R'],
                ['PregnantCattle',3,'V','R'],
                ['Beans',2,'B','O'],
                ['Fruits',3,'B','O'],
                ['Milk',2,'B','R'],
                ['WhaleMeat',3,'B','R'],
                ['Silver',1,'B','B']]
        
        tile = []
        
        # Only keep tile the player has
        for i in tileTemplate:
            if player.resources[i[0]] > 0:
                tile.append(i)

        possiblePlacements = []
            
        # Loop through possible orange and red tiles (each rotation inlucded) and loop through each spot
        for i in range(len(player.feastTable)):                                
            # First check free feast slots
            if player.feastTable[i][0] == 'F':                    
                # Loop through tiles
                for j in range(len(tile)):
                    validPlacement = True
                    # Check if there is space. If end of table reached or another tile reached, returns False
                    for k in range(tile[j][1] - 1):
                        if player.feastTable[i][1] + k + 1 > len(player.feastTable):
                            validPlacement = False
                            continue
                        elif player.feastTable[i + k + 1][0] != 'F':
                            validPlacement = False
                            continue

                    
                    # Next check if either end is same color. First make sure not at either end of table. Don't do to silver (color = B)
                    if tile[j][3] != 'B':
                        if player.feastTable[i][1] != 1:
                            if player.feastTable[i - 1][3] == tile[j][3]:
                                validPlacement = False
                                continue
                            
                        if player.feastTable[i][1] < len(player.feastTable) - tile[j][1]:
                            if player.feastTable[i + tile[j][1]][3] == tile[j][3]:
                                validPlacement = False
                                continue
                           
                    # Next check if using horizontal rotaion, if that tile has already been used
                    if tile[j][2] == 'H':
                        # Loop through each Feast Table slot
                        for k in range(len(player.feastTable)):
                            if player.feastTable[k][0] == tile[j][0]:
                                validPlacement = False
                                continue
                            
                    if validPlacement == True:
                        possiblePlacements.append([tile[j][0], player.feastTable[i][1], tile[j][2]])
            
        return possiblePlacements
                

    def buildShed(self, player):
        if player.endedTurn:
            print('Player already ended their turn!')
        elif player.madeAction:
            print('Player already made an action this turn!')
        elif self.turn == player.ID:
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
        self.endedTurn = False
        self.madeAction = False
        self.whalingBoats = []
        self.knarrs = []
        self.longships = []
        self.penalty = 0
        self.occupations = []
        self.expBoards = []
        self.houses = []
        self.bonuses = []
        self.playerBoard = PlayerBoard()
        self.validActions = []
      
        self.resources = {'Silver':0, 'Stone':0, 'Wood':0, 'Ore':0, 'Peas':1, 'Mead':1, 'Flax':1, 'Stockfish':0, 'Beans':1, 'Milk':0, 
                          'Grain':0, 'SaltMeat':0, 'Cabbage':0, 'GameMeat':0, 'Fruits':0, 'WhaleMeat':0, 'Oil':0, 'Runestone':0, 'Hide':0, 'Silverware':0, 'Wool':0, 
                          'Chest':0, 'Linen':0, 'Silk':0, 'SkinAndBones':0, 'Spices':0, 'Fur':0, 'Jewelry':0, 'Robe':0, 'TreasureChest':0, 'Clothing':0, 'SilverHoard':0, 
                          'Sheep':0, 'PregnantSheep':0, 'Cattle':0, 'PregnantCattle':0, 'Sword':0, 'Bow':0, 'Spear':0, 'Snare':0}

        # FeastTable slot have Free (F) or occupied (name of tile); slot number; rotation horizontal (H), vertical (V), or both (B); and color Red (R), Orange (O), or Blue (B)
        self.feastTable = [['F',1,'B','B'],
                           ['F',2,'B','B'],
                           ['F',3,'B','B'],
                           ['F',4,'B','B'],
                           ['F',5,'B','B'],
                           ['F',6,'B','B']]
        
class PlayerBoard():
    def __init__(self):
        self.income = 0
        self.bonuses = []
        # Tile definitions: X = not placable, F = free, P = free -1 point, B<resource> = bonus resource, I<number> = income added from occupying, O<color> = occupied by color
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
        