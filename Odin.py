import random
import itertools
from AI import *

class Game():
    def __init__(self, nHumanPlayers = 1, nBotPlayers = 0, ai = [], occupationSet = ['A']):
        # Available exploration boards and stored silver
        self.availableExplorationBoards = {'Shetland':0,'FaroeIslands':0,'Iceland':0,'Greenland':0} 
        
        # Available Special Tiles and their silver cost
        self.availableSpecialTiles = {'GlassBeads':0,'Helmet':1,'Cloakpin':1,'Belt':2,'Crucifix':2,'DrinkingHorn':2,'AmberFigure':2,
                                      'Horseshoe':2,'GoldBrooch':3,'ForgeHammer':4,'Fibula':4,'ThrowingAxe':4,'Chalice':5,'RoundShield':6,'EnglishCrown':9999}
        
        # Sword tiles and their sword costs
        self.swordTiles = {'Runestone':6,'Silverware':7,'Chest':8,'Silk':8,'Spices':9,'Jewelry':10,'TreasureChest':11,'SilverHoard':15,
                           'GlassBeads':7,'Helmet':8,'Cloakpin':8,'Belt':8,'Crucifix':8,'DrinkingHorn':8,'AmberFigure':9,
                           'Horseshoe':9,'GoldBrooch':9,'ForgeHammer':10,'Fibula':10,'ThrowingAxe':11,'Chalice':12,'RoundShield':13,'EnglishCrown':16}
        
        # Available mountains
        self.availableMountains = [['Wood','Wood','Wood','Wood','Stone','Stone','Silver'],
                                   ['Wood','Wood','Stone','Stone','Ore','Ore','Silver'],
                                   ['Wood','Wood','Wood','Stone','Ore','Ore','Silver'],
                                   ['Wood','Wood','Stone','Ore','Ore','Silver','Silver'],
                                   ['Wood','Wood','Wood','Stone','Stone','Ore','Silver'],
                                   ['Wood','Wood','Wood','Wood','Stone','Ore','Silver'],
                                   ['Wood','Wood','Wood','Stone','Stone','Stone','Silver'],
                                   ['Wood','Wood','Stone','Stone','Stone','Ore','Silver']] 
        
        # Current Mountains in play
        self.mountains = [] 
        
        # Available Weapons
        self.availableWeapons = ['Sword'] * 11 + ['Bow'] * 12 + ['Spear'] * 12 + ['Snare'] * 12
        
        # Available Houses
        self.availableHouses = ['Shed'] * 3 + ['StoneHouse'] * 3 + ['LongHouse'] * 5
        
        # Available anytime actions
        self.availableAnytimeActions = ['PlaceFeast','PlaceTile','BuyBoat','Arming']
        
        # Populate players in game
        self.players = []
        for i in range(nHumanPlayers):
            self.players.append(Player(i, 'Human'))
        for i in range(nBotPlayers):
            self.players.append(Player(i + nHumanPlayers, ai[i]))
        random.shuffle(self.players)
                   
        # Set starting round
        self.round = 1
        
        # Initialize starting player token which will be assigned when the first person passes
        self.endedLast = 0
        
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
                                                      'SoberMan','MeleeFighter','Woodcutter','TutorBlue','CraftLeader']
                self.availableOccupations += ['ForeignTrader','Steersman','Helmsman','LinenWeaver','Tradesman','ShipBuilder',
                                              'Builder','ShipsCook','Homecomer','Miner','WeaponsSupplier','Follower','Dragonslayer',
                                              'YieldFarmer','Shipowner','Fisherman','OreBoatman','Digger','Farmer','Merchant','Nobleman',
                                              'WhalingEquipper','HideBuyer','VillageLeader','Chief','SheepShearer','SpiceMerchantOrange',
                                              'Miller','Drunkard','RuneEngraver','LinseedOilPresser','Peacemaker','Wanderer','Wholesaler',
                                              'CattleBreeder','OrientShipper','Barbarian','ArmedFighter','Cowherd','Custodian','BlubberCook',
                                              'MeatMerchant','MountainGuard','Priest','Trapper','Preacher','Breeder','ArmsDealer',
                                              'WeaponSupplier','TutorOrange','Furrier','Milker','PeaFlourBaker','FruitPicker','FlaxBaker','Peddler']
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
         
        # List all possible single upgrades
        self.availableSingleUpgrades = {'Peas':'Mead',
                                        'Flax':'Stockfish',
                                        'Beans':'Milk',
                                        'Grain':'SaltMeat',
                                        'Cabbage':'GameMeat',
                                        'Fruits':'WhaleMeat',
                                        'Mead':'Oil',
                                        'Stockfish':'Hide',
                                        'Milk':'Wool',
                                        'SaltMeat':'Linen',
                                        'GameMeat':'SkinAndBones',
                                        'Sheep':'Fur',
                                        'PregnantSheep':'Fur',
                                        'WhaleMeat':'Robe',
                                        'Cattle':'Clothing',
                                        'PregnantCattle':'Clothing',
                                        'Oil':'Runestone',
                                        'Hide':'Silverware',
                                        'Wool':'Chest',
                                        'Linen':'Silk',
                                        'SkinAndBones':'Spices',
                                        'Fur':'Jewelry',
                                        'Robe':'TreasureChest',
                                        'Clothing':'SilverHoard'}
         
        # List all possible double upgrades
        self.availableDoubleUpgrades = {'Peas':'Oil',
                                  'Flax':'Hide',
                                  'Beans':'Wool',
                                  'Grain':'Linen',
                                  'Cabbage':'SkinAndBones',
                                  'Fruits':'Robe',
                                  'Mead':'Runestone',
                                  'Stockfish':'Silverware',
                                  'Milk':'Chest',
                                  'SaltMeat':'Silk',
                                  'GameMeat':'Spices',
                                  'Sheep':'Jewelry',
                                  'PregnantSheep':'Jewelry',
                                  'WhaleMeat':'TreasureChest',
                                  'Cattle':'SilverHoard',
                                  'PregnantCattle':'SilverHoard'}  
                 
        # List all possible Field Farmer upgrades which are orange tiles up and to the right up to two times
        self.availableFieldFarmerUpgrades = {'Peas':['Stockfish','Wool'],
                                  'Flax':['Milk','Linen'],
                                  'Beans':['SaltMeat','SkinAndBones'],
                                  'Grain':['GameMeat','Fur'],
                                  'Cabbage':['Sheep','Robe'],
                                  'Fruits':['Cattle']}  
        # List all possible green upgrades
        self.availableGreenUpgrades = {'Oil':'Runestone',
                                       'Hide':'Silverware',
                                       'Wool':'Chest',
                                       'Linen':'Silk',
                                       'SkinAndBones':'Spices',
                                       'Fur':'Jewelry',
                                       'Robe':'TreasureChest',
                                       'Clothing':'SilverHoard'}
        
        # Draw each player a starting occupation card and starting weapons
        for i in self.players:
            i.occupations.append(self.availableStartingOccupations.pop(random.randint(0, len(self.availableStartingOccupations) - 1)))
            
            i.resources['Bow'] += 1
            i.resources['Spear'] += 1
            i.resources['Snare'] += 1
            
            self.availableWeapons.remove('Bow')
            self.availableWeapons.remove('Spear')
            self.availableWeapons.remove('Snare')
        
    def play(self):        
        # Play through each round
        for i in range(7):
            # Count how many four viking actions were played for Homecomer
            self.playedFourVikingActions = 0
                    
            # Available action spaces
            self.availableActions = ['BuildShed','BuildWhalingBoat','HuntingGameOne','HuntStockfish','BuyStockfish','BuySaltMeat','WeeklyMarketOne','ProductsOne','CraftLinen','CraftRunestone',
                                     'MountainTwo','MountainOneUpgradeOne','UpgradeTwo','UpgradeGreensOne','Raiding','ExplorationOne','DrawOccupation','PlayOccupationsOne','BuildStoneHouse',
                                     'BuildKnarr','HuntingGameTwo','LaySnare','BuySheep','BuyCattle','WeeklyMarketTwo','ProductsTwo','CraftClothing','CraftChest','WoodPerPlayer','MountainThreeUpgradeOne',
                                     'UpgradeThree','UpgradeGreensTwo','PillagingOne','ExplorationTwo','EmigrateOne','PlayOccupationsTwo','BuildLongHouse','BuildLongship','WhalingOne','BuySheepOrCattle',
                                     'WeeklyMarketThree','ProductsThree','CraftSpecial','CraftChestRunestone','MountainThreeTwo','UpgradeThreeWeapons','UpgradeFour','BuySpecials','PillagingTwo',
                                     'ExplorationThree','EmigrateTwo','PlayOccupationsThree','BuildHouseBoat','WhalingTwo','BuySheepAndCattle','WeeklyMarketFour','CraftingFour',
                                     'MountainFourUpgradeTwoTwice','MountainOrUpgrade','Plundering','EmigrateThree']

            print('\n******Starting Round ' + str(self.round) + '******')
            print('\Mountains:')
            print(self.mountains)
            self.harvestPhase()
            self.explorationPhase()
            self.drawWeaponPhase()
            self.actionPhase()
            for j in self.players:
                j.endedTurn = False
                j.vikings = 0
            self.determineStartingPlayerPhase()
            self.incomePhase()
            self.breedingPhase()
            self.actionPhase()
            for j in self.players:
                j.endedTurn = False
            if i < 6:
                self.feastPhase()
                self.bonusPhase()
                self.mountainPhase()
                self.returnVikingsPhase()
            
        return self.score()
            

    def harvestPhase(self):
        print('\n***Harvest Phase***')
        for i in self.players:           
            if self.round == 2:
                i.resources['Peas'] += 1
                i.resources['Flax'] += 1
                i.resources['Beans'] += 1
                i.resources['Grain'] += 1
            elif self.round == 4:
                i.resources['Peas'] += 1
                i.resources['Flax'] += 1
                i.resources['Beans'] += 1
                i.resources['Grain'] += 1
                i.resources['Cabbage'] += 1
            elif self.round == 6:
                i.resources['Peas'] += 1
                i.resources['Flax'] += 1
                i.resources['Beans'] += 1
                i.resources['Grain'] += 1
                i.resources['Cabbage'] += 1
                i.resources['Fruits'] += 1
                
    def explorationPhase(self):
        print('\n***Exploration Phase***')
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
        print('\n***Draw Weapon Phase***')
        for i in self.players:
            self.drawWeapon(i, 1)
                
    def actionPhase(self):
        print('\n***Action Phase***')
        ended = 0
        player = 0
        while ended < len(self.players):
            if not self.players[player].endedTurn:
                ended += self.takeActions(self.players[player])
                self.players[player].madeAction = False
            if player < len(self.players) - 1:
                player += 1
            else:
                player = 0
            
    def determineStartingPlayerPhase(self):
        print('\n***Determine Starting Player Phase***')
        # Rotate players to start with person who ended turn last
        while self.players[0].ID != self.endedLast:
            self.players.append(self.players.pop(0))        
            
    def incomePhase(self):
        print('\n***Income Phase***')
        for i in self.players:
            i.resources['Silver'] += i.income
        
    def breedingPhase(self):
        print('\n***Breeding Phase***')
        for i in self.players:
            if i.resources['PregnantSheep'] > 0:
                i.resources['Sheep'] += i.resources['PregnantSheep'] + 1
                i.resources['PregnantSheep'] -= 1
            elif i.resources['Sheep'] >= 2:
                i.resources['PregnantSheep'] += 1
                i.resources['Sheep'] -= 1
            if i.resources['PregnantCattle'] > 0:
                i.resources['Cattle'] += i.resources['PregnantCattle'] + 1
                i.resources['PregnantCattle'] -= 1
            elif i.resources['Cattle'] >= 2:
                i.resources['PregnantCattle'] += 1
                i.resources['Cattle'] -= 1              
            
    def feastPhase(self):
        print('\n***Feast Phase***')
        for i in self.players:
            # Give thing penalty per open spot in feast table
            i.penalty += i.feastTable.count(['F','B','B'])
            # Clear feast table and add 1 slot
            i.feastTable = [['F','B','B']] * (len(i.feastTable) + 1 )              
                
    def bonusPhase(self):
        print('\n***Bonus Phase***')
        for i in self.players:
            # Look through each player's boards and houses for bonuses
            for j in i.houses + i.boards:
                # Check every X
                for k in range(len(j.tiles[0])):
                    # Check every Y
                    for l in range(len(j.tiles)):
                        # Look for spaces starting with bonus
                        if j.tiles[l][k][0:5] == 'Bonus':
                            validBonus = True
                            # Check top
                            if l < len(j.tiles) - 1:
                                if j.tiles[l + 1][k] in ['F','P']:
                                    validBonus = False
                            # Check right
                            if k < len(j.tiles[0]) - 1:
                                if j.tiles[l][k + 1] in ['F','P']:
                                    validBonus = False
                            # Check bottom
                            if l > 0:
                                if j.tiles[l - 1][k] in ['F','P']:
                                    validBonus = False
                            # Check left
                            if k > 0:
                                if j.tiles[l][k - 1] in ['F','P']:
                                    validBonus = False
                            if validBonus:
                                if j.tiles[l][k] == 'BonusOreStone':
                                    i.resources['Ore'] += 1
                                    i.resources['Stone'] += 1
                                elif j.tiles[l][k] == 'BonusRunestoneOre':
                                    i.resources['Runestone'] += 1
                                    i.resources['Ore'] += 1
                                elif j.tiles[l][k] == 'BonusStoneHouse':
                                    i.houses.append(House('StoneHouse'))
                                elif j.tiles[l][k] == 'BonusClothpin':
                                    if 'Clothinpin' in self.availableSpecialTiles:
                                        i.resources['Clothpin'] += 1
                                        self.availableSpecialTiles.remove('Clothpin')
                                else:
                                    i.resources[j.tiles[l][k][5:99]] += 1

    
    def mountainPhase(self):
        print('\n***Mountain Phase***')
        for i in self.mountains:
            if len(i) > 0:
                i.pop(0)
        self.drawMountain() 

    def returnVikingsPhase(self):
        print('\n***Return Vikings Phase***')
        for i in self.players:
            i.vikings = self.round + 6    
        self.round += 1     

    def score(self):
        score = [0] * len(self.players)
        for i in range(len(self.players)):
            # Ships
            score[i] += len(self.players[i].whalingBoats) * 3
            score[i] += len(self.players[i].knarrs) * 5
            score[i] += len(self.players[i].longships) * 8
            
            # Emigration
            score[i] += self.players[i].emigratePoints     
            
            # Exploration boards
            for j in self.players[i].boards[1:9]:
                score[i] += j.points
                
            # Houses
            for j in self.players[i].houses:
                score[i] += j.points
                
            # Sheep and cattle
            score[i] += self.players[i].resources['Sheep'] * 2
            score[i] += self.players[i].resources['PregnantSheep'] * 3
            score[i] += self.players[i].resources['Cattle'] * 3
            score[i] += self.players[i].resources['PregnantCattle'] * 4
            
            # Ooccupations
            
            # Silver
            score[i] += self.players[i].resources['Silver']
            
            # Crown
            
            # Board negative points (home, explorations, and houses)
            for j in self.players[i].houses + self.players[i].boards:
                score[i] -= sum(x.count('P') for x in j.tiles)
                
            # Thing penalty
            score[i] -= self.players[i].penalty * 3

            
            
        return score            
            
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
                player.resources['Sword'] += 1
            elif weapon == 'Bow':
                player.resources['Bow'] += 1
            elif weapon == 'Spear':
                player.resources['Spear'] += 1
            elif weapon == 'Snare':
                player.resources['Snare'] += 1          
                        
    def drawMountain(self):
        if len(self.availableMountains) > 0:
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
        
    def huntingGame(self, player):
        for i in range(3):
            roll = random.randint(1,8)
            validActions = ['Failure']
            if i < 2:
                validActions.append('Roll')            
            if player.resources['Wood'] + player.resources['Bow'] >= roll:
                validActions.append('Success')
            action = player.ai.takeAction(player, validActions)
            if action == 'Failure':
                player.resources['Wood'] += 1
                player.resources['Bow'] += 1
                break
            elif action == 'Success':
                player.resources['Hide'] += 1
                player.resources['GameMeat'] += 1
                player.resources['Wood'] -= max(0, roll - player.resources['Bow'])
                player.resources['Bow'] -= min(player.resources['Bow'], roll)
                
    # Simplifying by always using snares up first, despite dragonslayer possibly being worse  
    def laySnare(self, player):
        for i in range(3):
            roll = random.randint(1,8)
            validActions = ['Failure']
            if i < 2:
                validActions.append('Roll')            
            if player.resources['Wood'] + player.resources['Snare'] >= roll:
                validActions.append('Success')
            action = player.ai.takeAction(player, validActions)
            if action == 'Failure':
                player.resources['Wood'] += 1
                player.resources['Snare'] += 1
                break
            elif action == 'Success':
                player.resources['Fur'] += 1
                player.resources['Wood'] -= max(0, roll - player.resources['Snare'])
                player.resources['Snare'] -= min(player.resources['Snare'], roll)
                break
                
    def raiding(self, player):
        for i in range(3):
            roll = random.randint(1,8)
            validActions = ['Failure']
            if i < 2:
                validActions.append('Roll')            
            maxPurchase = roll + player.resources['Stone'] + player.resources['Sword']
            for j in self.swordTiles:
                if self.swordTiles[j] <= maxPurchase and (j in self.availableSpecialTiles or j in ['RuneStone','Silverware','Chest','Silk','Spices','Jewelry','TreasureChest','SilverHoard']):
                    validActions.append(j)
            action = player.ai.takeAction(player, validActions)
            if action == 'Failure':
                player.resources['Stone'] += 1
                player.resources['Sword'] += 1
                break
            elif action not in ['Failure','Roll']:
                player.resources[action] += 1
                player.resources['Stone'] -= max(0, self.swordTiles[action] - roll - player.resources['Sword'])
                player.resources['Sword'] -= min(self.swordTiles[action] - roll, player.resources['Sword'])
                break
        
    def pillaging(self, player):
        ore = player.longships[0].ore 
        for i in range(3):
            roll = random.randint(1,12)
            validActions = ['Failure']
            if i < 2:
                validActions.append('Roll')            
            maxPurchase = roll + player.resources['Stone'] + player.resources['Sword'] + ore
            for j in self.swordTiles:
                if self.swordTiles[j] <= maxPurchase and (j in self.availableSpecialTiles or j in ['RuneStone','Silverware','Chest','Silk','Spices','Jewelry','TreasureChest','SilverHoard']):
                    validActions.append(j)
            action = player.ai.takeAction(player, validActions)
            if action == 'Failure':
                player.resources['Stone'] += 1
                player.resources['Sword'] += 1
                player.vikings += 1
                break
            elif action not in ['Failure','Roll']:
                player.resources[action] += 1
                player.resources['Stone'] -= max(0, self.swordTiles[action] - roll - ore - player.resources['Sword'])
                player.resources['Sword'] -= min(self.swordTiles[action] - roll - ore, player.resources['Sword'])
                break
        
    # Simplifying by always using spears up first, despite dragonslayer possibly being worse  
    def whalingOne(self, player):
        ore = 0
        for i in player.whalingBoats:
            ore += i.ore
        for i in range(3):
            roll = random.randint(1,12)
            validActions = ['Failure']
            if i < 2:
                validActions.append('Roll')  
            if player.resources['Wood'] + player.resources['Spear'] >= roll - ore:
                validActions.append('Success')
            action = player.ai.takeAction(player, validActions)
            if action == 'Failure':
                player.resources['Wood'] += 1
                player.resources['Spear'] += 1
                player.vikings += 2
                break
            elif action == 'Success':
                player.resources['Oil'] += 1
                player.resources['SkinAndBones'] += 1
                player.resources['WhaleMeat'] += 1
                player.resources['Wood'] -= max(0, roll - ore - player.resources['Spear'])
                player.resources['Spear'] -= min(player.resources['Spear'], max(roll - ore, 0))
                break
        
    # Simplifying by always using spears up first, despite dragonslayer possibly being worse  
    def whalingTwo(self, player):
        ore = player.whalingBoats[0].ore
        for i in range(3):
            roll = random.randint(1,12)
            validActions = ['Failure']
            if i < 2:
                validActions.append('Roll')  
            if player.resources['Wood'] + player.resources['Spear'] >= roll - ore:
                validActions.append('Success')
            action = player.ai.takeAction(player, validActions)
            if action == 'Failure':
                player.resources['Wood'] += 1
                player.resources['Spear'] += 1
                player.vikings += 2
                break
            elif action == 'Success':
                player.resources['Oil'] += 1
                player.resources['SkinAndBones'] += 1
                player.resources['WhaleMeat'] += 1
                player.resources['Wood'] -= max(0, roll - ore - player.resources['Spear'])
                player.resources['Spear'] -= min(player.resources['Spear'], max(roll - ore, 0))
                break        
            
    def playOccupation(self, player, occupation):
        print('Playing ' + occupation)
        player.occupations.remove(occupation)
        player.playedOccupations.append(occupation)
        
        # Empty valid actions list for potential actions from cards
        validActions = []
            
        # Logic for instant occupation cards
        if occupation == 'Preacher':
            validActions = ['']
#            action = player.ai.takeAction(player, validActions)            
        elif occupation == 'Miner':
            player.resources['Ore'] += len(player.longships)
            player.resources['Stone'] += len(player.longships)
            player.resources['Silver'] += len(player.longships)
        elif occupation == 'Homecomer':
            player.vikings += self.playedFourVikingActions
        elif occupation == 'Chief':
            # Give thing penalty per open spot in feast table
            player.penalty += player.feastTable.count(['F','B','B'])
            # Clear feast table and add 1 slot
            player.feastTable = [['F','B','B']] * (len(player.feastTable) + 1)
        elif occupation == 'ShipBuilder':
            validActions= ['']
        elif occupation == 'SheepShearer':
            if player.resources['Sheep'] + player.resources['PregnantSheep'] >= 6:
                player.resources['Wool'] += 3
            elif player.resources['Sheep'] + player.resources['PregnantSheep'] >= 4:
                player.resources['Wool'] += 2
            elif player.resources['Sheep'] + player.resources['PregnantSheep'] >= 3:
                player.resources['Wool'] += 1
        elif occupation == 'Breeder':
            if player.resources['Cattle'] >= 1:
                player.resources['Cattle'] -= 1
                player.resources['PregnantCattle'] += 1
        elif occupation == 'OrientShipper':
            validActions = ['']
        elif occupation == 'WeaponSupplier':
            self.drawWeapon(player, 4)
        elif occupation == 'Builder':
             for j in player.houses:
                # Check every X
                for k in range(len(j.tiles[0])):
                    # Check every Y
                    for l in range(len(j.tiles)):
                        # Look for spaces starting with bonus
                        if j.tiles[l][k][0:5] == 'Bonus':
                            validBonus = True
                            # Check top
                            if l < len(j.tiles) - 1:
                                if j.tiles[l + 1][k] in ['F','P']:
                                    validBonus = False
                            # Check right
                            if k < len(j.tiles[0]) - 1:
                                if j.tiles[l][k + 1] in ['F','P']:
                                    validBonus = False
                            # Check bottom
                            if l > 0:
                                if j.tiles[l - 1][k] in ['F','P']:
                                    validBonus = False
                            # Check left
                            if k > 0:
                                if j.tiles[l][k - 1] in ['F','P']:
                                    validBonus = False
                            if validBonus:
                                player.resources[j.tiles[l][k][5:99]] += 1
        elif occupation == 'Cowherd':
            validActions = ['']
        elif occupation == 'CattleBreeder':
            if player.resources['PregnantSheep'] > 0:
                player.resources['Sheep'] += player.resources['PregnantSheep'] + 1
                player.resources['PregnantSheep'] -= 1
            elif player.resources['Sheep'] >= 2:
                player.resources['PregnantSheep'] += 1
                player.resources['Sheep'] -= 1
            if player.resources['PregnantCattle'] > 0:
                player.resources['Cattle'] += player.resources['PregnantCattle'] + 1
                player.resources['PregnantCattle'] -= 1
            elif player.resources['Cattle'] >= 2:
                player.resources['PregnantCattle'] += 1
                player.resources['Cattle'] -= 1    
        elif occupation == 'WhalingEquipper':
            player.resources['Oil'] += len(player.knarrs)
            player.resources['Wood'] += len(player.whalingBoats)
        elif occupation == 'Custodian':
            for i in player.houses:
                if i.houseType in ['StoneHouse','LongHouse']:
                    player.resources['Silver'] += 2
        elif occupation == 'Wholesaler':
            for i in self.availableSingleUpgrades:
                if player.resources[i] >= 1:
                    for j in range(max(4, player.resources[i])):
                        validActions.append(['Wholesaler',{'Tile':i,'NumUpgrades':j + 1}])
        elif occupation == 'HideBuyer':
            if player.resources['Silver'] >= 6:
                validActions.append(['HideBuyer',{'Hides':3}])
            if player.resources['Silver'] >= 4:
                validActions.append(['HideBuyer',{'Hides':2}])
            if player.resources['Silver'] >= 2:
                validActions.append(['HideBuyer',{'Hides':1}])
        elif occupation == 'Follower':
            pass
        elif occupation == 'Fisherman':
            player.resources['Stockfish'] += len(player.whalingBoats)
        elif occupation == 'Milker':
            if player.resources['Sheep'] + player.resources['PregnantSheep'] >= 1:
                player.resources['Milk'] += 1
                player.resources['Silver'] += 1
            if player.resources['Cattle'] + player.resources['PregnantCattle'] >= 1:
                player.resources['Milk'] += 1
                player.resources['Silver'] += 1
        elif occupation == 'WeaponsSupplier':
            if len(player.longships) >= 3:
                self.drawWeapon(player, 10)
            elif len(player.longships) == 2:
                self.drawWeapon(player, 5)
            elif len(player.longships) == 1:
                self.drawWeapon(player, 2)
        elif occupation == 'FieldFarmer':
            pass
        elif occupation == 'FruitPicker':
            pass
        elif occupation == 'Helmsman':
            pass
        elif occupation == 'Sheapherd':
            pass
        elif occupation == 'Dragonslayer':
            pass
            
     
    # Take an action or anytime action
    def takeActions(self, player):
        passed = False
        while not passed:
            action = player.ai.takeAction(player, self.determineValidActions(player))
            print('Player ' + str(player.ID + 1) + ' has ' + str(player.vikings) + ' vikings')
            print(str(len(self.determineValidActions(player))) + ' possible actions')
            print(action)
            if action[0] in self.availableActions:
                if action[0] in ['BuildHouseBoat','WhalingTwo','BuySheepAndCattle','WeeklyMarketFour','CraftingFour',
                                     'MountainFourUpgradeTwoTwice','MountainOrUpgrade','Plundering','EmigrateThree']:
                    player.vikings -= 4
                    self.playedFourVikingActions += 1
                if action[0] == 'BuildShed':
                    player.vikings -= 1
                    player.resources['Wood'] -= 2
                    player.houses.append(House('Shed'))
                    self.availableHouses.remove('Shed')
                elif action[0] == 'BuildWhalingBoat':
                    player.vikings -= 1
                    player.resources['Wood'] -= 1
                    player.whalingBoats.append(Boat('WhalingBoat'))
                elif action[0] == 'HuntingGameOne':
                    player.vikings -= 1
                    self.huntingGame(player)
                elif action[0] == 'HuntStockfish':
                    player.vikings -= 1
                    player.resources['Stockfish'] += 1
                elif action[0] == 'BuyStockfish':
                    player.vikings -= 1
                    player.resources['Silver'] -= 1
                    player.resources['Stockfish'] += 2
                elif action[0] == 'BuySaltMeat':
                    player.vikings -= 1
                    player.resources['Silver'] -= 2
                    player.resources['SaltMeat'] += 2
                elif action[0] == 'WeeklyMarketOne':
                    player.vikings -= 1
                    player.resources['Beans'] += 1
                    player.resources['Silver'] += 1
                elif action[0] == 'ProductsOne':
                    player.vikings -= 1
                    player.resources['Milk'] += max(player.resources['Cattle'] + player.resources['PregnantCattle'], 3)
                elif action[0] == 'CraftLinen':
                    player.vikings -= 1
                    player.resources['Flax'] -= 1
                    player.resources['Linen'] += 1
                elif action[0] == 'CraftRunestone':
                    player.vikings -= 1
                    player.resources['Stone'] -= 1
                    player.resources['Silver'] += 1
                    player.resources['Runestone'] += 1
                elif action[0] == 'MountainTwo':
                    player.vikings -= 1
                    for i in range(action[1][1]):
                        if self.mountains[action[1][0]][0] == 'Silver':
                            player.resources['Silver'] += 1
                        player.resources[self.mountains[action[1][0]].pop(0)] += 1
                elif action[0] == 'MountainOneUpgradeOne':
                    player.vikings -= 1
                    for i in range(action[1][1]):
                        if self.mountains[action[1][0]][0] == 'Silver':
                            player.resources['Silver'] += 1
                        player.resources[self.mountains[action[1][0]].pop(0)] += 1
                    if action[1][2] != 'None':
                        player.resources[action[1][2]] -= 1
                        player.resources[self.availableSingleUpgrades[action[1][2]]] += 1                        
                elif action[0] == 'UpgradeTwo':
                    player.vikings -= 1
                    for i in action[1]:
                        player.resources[i] -= 1
                        player.resources[self.availableSingleUpgrades[i]] += 1
                elif action[0] == 'UpgradeGreensOne':
                    player.vikings -= 1
                    player.resources['Silver'] -= 1
                    for i in action[1]:
                        player.resources[i] -= 1
                        player.resources[self.availableGreenUpgrades[i]] -= 1
                elif action[0] == 'Raiding':
                    player.vikings -= 1
                    self.raiding(player)
                elif action[0] == 'ExplorationOne':
                    player.vikings -= 1
                    player.resources['Silver'] += self.availableExplorationBoards[action[1][0]]
                    del self.availableExplorationBoards[action[1][0]]
                    player.boards.append(ExpBoard(action[1][0]))
                elif action[0] == 'DrawOccupation':
                    player.vikings -= 1
                    player.occupations.append(self.availableOccupations.pop(random.randint(0, len(self.availableOccupations) - 1)))
                    player.resources['Silver'] += 1
                elif action[0] == 'PlayOccupationsOne':
                    player.vikings -= 1
                    player.resources -= action[1][0]
                    self.playOccupation(player, action[1][1])
                elif action[0] == 'BuildStoneHouse':
                    player.vikings -= 2
                    player.resources['Stone'] -= 1
                    player.houses.append(House('StoneHouse'))
                    self.availableHouses.remove('StoneHouse')
                elif action[0] == 'BuildKnarr':
                    player.vikings -= 2
                    player.resources['Wood'] -= 2
                    player.knarrs.append(Boat('Knarr'))
                elif action[0] == 'HuntingGameTwo':
                    player.vikings -= 2
                    self.huntingGame(player)
                elif action[0] == 'LaySnare':
                    player.vikings -= 2
                    self.laySnare(player)
                elif action[0] == 'BuySheep':
                    player.vikings -= 2
                    player.resources['Silver'] -= 1
                    player.resources['Sheep'] += 1
                elif action[0] == 'BuyCattle':
                    player.vikings -= 2
                    player.resources['Silver'] -= 3
                    player.resources['Cattle'] += 1
                elif action[0] == 'WeeklyMarketTwo':
                    player.vikings -= 2
                    player.resources['Flax'] += 1
                    player.resources['Stockfish'] += 1
                    player.resources['Silver'] += 1
                elif action[0] == 'ProductsTwo':
                    player.vikings -= 2                    
                    player.resources['Mead'] += 2
                    player.resources['Silver'] += 2
                elif action[0] == 'CraftClothing':
                    player.vikings -= 2
                    player.resources['Hide'] -= 1
                    player.resources['Linen'] -= 1
                    player.resources['Clothing'] += 1
                    player.resources['Silver'] += 2
                elif action[0] == 'CraftChest':
                    player.vikings -= 2
                    player.resources[action[1][0]] -= 1
                    player.resources['Chest'] += 1
                    player.resources['Silver'] += 1
                elif action[0] == 'WoodPerPlayer':
                    player.vikings -= 2
                    player.resources['Wood'] += len(self.players)
                    player.resources['Ore'] += 1
                elif action[0] == 'MountainThreeUpgradeOne':
                    player.vikings -= 2
                    for i in range(action[1][1]):
                        if self.mountains[action[1][0]][0] == 'Silver':
                            player.resources['Silver'] += 1
                        player.resources[self.mountains[action[1][0]].pop(0)] += 1
                    if action[1][2] != 'None':
                        player.resources[action[1][2]] -= 1
                        player.resources[self.availableSingleUpgrades[action[1][2]]] += 1         
                elif action[0] == 'UpgradeThree':
                    player.vikings -= 2
                    for i in action[1]:
                        player.resources[i] -= 1
                        player.resources[self.availableSingleUpgrades[i]] += 1
                elif action[0] == 'UpgradeGreensTwo':
                    player.vikings -= 2
                    player.resources['Silver'] -= 1
                    for i in action[1]:
                        player.resources[i] -= 1
                        player.resources[self.availableGreenUpgrades[i]] -= 1
                elif action[0] == 'PillagingOne':
                    player.vikings -= 2
                    self.pillaging(player)
                elif action[0] == 'ExplorationTwo':
                    player.vikings -= 2
                    player.resources['Silver'] += self.availableExplorationBoards[action[1][0]]
                    del self.availableExplorationBoards[action[1][0]]
                    player.boards.append(ExpBoard(action[1][0]))
                elif action[0] == 'EmigrateOne':
                    player.vikings -= 2
                    player.resources['Silver'] -= self.round
                    if action[1][0] == 'Knarr':
                        player.emigratePoints += 21
                        player.knarrs.remove(0)
                    elif action[1][0] == 'Longship':
                        player.emigratePoints += 18
                        # Longships should be sorted by ore and will always remove last ship (lowest ore ship)
                        player.longships.remove(len(player.longships) - 1)
                    player.feastTable.remove(0)
                    player.feastTable.remove(0)
                elif action[0] == 'PlayOccupationsTwo':
                    player.vikings -= 2
                    for i in action[1]:
                        self.playOccupation(player, i)
                elif action[0] == 'BuildLongHouse':
                    player.vikings -= 3
                    player.occupations.append(self.availableOccupations.pop(random.randint(0, len(self.availableOccupations) - 1)))
                    if action[1][0] == 'BuildLongHouse':
                        player.resources['Stone'] -= 2
                        player.houses.append(House('LongHouse'))
                        self.availableHouses.remove('LongHouse')
                elif action[0] == 'BuildLongship':
                    player.vikings -= 3
                    player.occupations.append(self.availableOccupations.pop(random.randint(0, len(self.availableOccupations) - 1)))
                    if action[1][0] == 'BuildLongship':
                        player.longships.append(Boat('Longship'))
                        player.resources['Wood'] -= 2                        
                elif action[0] == 'WhalingOne':
                    player.vikings -= 3
                    player.occupations.append(self.availableOccupations.pop(random.randint(0, len(self.availableOccupations) - 1)))
                    if action[1][0] == 'WhalingOne':
                        self.whalingOne(player)
                elif action[0] == 'BuySheepOrCattle':
                    player.vikings -= 3
                    player.occupations.append(self.availableOccupations.pop(random.randint(0, len(self.availableOccupations) - 1)))
                    if action[1][0] == 'Cattle':
                        player.resources['Silver'] -= 1
                    player.resources[action[1][0]] += 1
                elif action[0] == 'WeeklyMarketThree':
                    player.vikings -= 3
                    player.occupations.append(self.availableOccupations.pop(random.randint(0, len(self.availableOccupations) - 1)))
                    player.resources['Fruits'] += 1
                    player.resources['SaltMeat'] += 1
                    player.resources['Oil'] += 1
                    player.resources['Silver'] += 1
                elif action[0] == 'ProductsThree':
                    player.vikings -= 3
                    player.occupations.append(self.availableOccupations.pop(random.randint(0, len(self.availableOccupations) - 1)))
                    player.resources['Wool'] += max(player.resources['Sheep'] + player.resources['PregnantSheep'], 3)
                elif action[0] == 'CraftSpecial':
                    player.vikings -= 3
                    player.occupations.append(self.availableOccupations.pop(random.randint(0, len(self.availableOccupations) - 1)))
                    if action[1][0] != 'None':
                        player.resources[action[1][0]] += 1
                        player.resources['Silver'] -= self.availableSpecialTiles[action[1][0]]
                        del self.availableSpecialTiles[action[1][0]]
                elif action[0] == 'CraftChestRunestone':
                    player.vikings -= 3
                    player.occupations.append(self.availableOccupations.pop(random.randint(0, len(self.availableOccupations) - 1)))
                    if action[1][0] == 'CraftChestRunestone':
                        player.resources['Stone'] -= 2
                        player.resources['Wood'] -= 2
                        player.resources['Chest'] += 2
                        player.resources['Runestone'] += 2
                elif action[0] == 'MountainThreeTwo':
                    player.vikings -= 3
                    player.occupations.append(self.availableOccupations.pop(random.randint(0, len(self.availableOccupations) - 1)))                    
                elif action[0] == 'UpgradeThreeWeapons':
                    player.vikings -= 3
                    player.occupations.append(self.availableOccupations.pop(random.randint(0, len(self.availableOccupations) - 1)))
                    self.drawWeapon(player, 4)
                    for i in action[1]:
                        player.resources[i] -= 1
                        player.resources[self.availableSingleUpgrades[i]] += 1                        
                elif action[0] == 'UpgradeFour':
                    player.vikings -= 3
                    player.occupations.append(self.availableOccupations.pop(random.randint(0, len(self.availableOccupations) - 1)))
                    for i in action[1]:
                        player.resources[i] -= 1
                        player.resources[self.availableSingleUpgrades[i]] += 1
                elif action[0] == 'BuySpecials':
                    player.vikings -= 3
                    player.occupations.append(self.availableOccupations.pop(random.randint(0, len(self.availableOccupations) - 1)))
                    for i in action[1]:
                        player.resources[i] += 1
                        player.resources['Silver'] -= self.availableSpecialTiles[i]
                        del self.availableSpecialTiles[i]
                elif action[0] == 'PillagingTwo':
                    player.vikings -= 3
                    player.occupations.append(self.availableOccupations.pop(random.randint(0, len(self.availableOccupations) - 1)))
                    if action[1][0] == 'PillagingTwo':
                        self.pillaging(player)
                elif action[0] == 'ExplorationThree':
                    player.vikings -= 3
                    player.occupations.append(self.availableOccupations.pop(random.randint(0, len(self.availableOccupations) - 1)))
                    if action[1][0] != 'None':
                        player.resources['Silver'] += self.availableExplorationBoards[action[1][0]]
                        del self.availableExplorationBoards[action[1][0]]
                        player.boards.append(ExpBoard(action[1][0]))
                elif action[0] == 'EmigrateTwo':
                    player.vikings -= 3
                    player.occupations.append(self.availableOccupations.pop(random.randint(0, len(self.availableOccupations) - 1)))
                    if action[1][0] != 'None':
                        player.resources['Silver'] -= self.round
                        if action[1][0] == 'Knarr':
                            player.emigratePoints += 21
                            player.knarrs.remove(0)
                        elif action[1][0] == 'Longship':
                            player.emigratePoints += 18
                            # Longships should be sorted by ore and will always remove last ship (lowest ore ship)
                            player.longships.remove(len(player.longships) - 1)
                        player.feastTable.remove(0)
                        player.feastTable.remove(0)
                elif action[0] == 'PlayOccupationsThree':
                    player.vikings -= 3
                    if 'Drawn' in action[1]:
                        action[1].remove('Drawn')
                        newOcc = self.availableOccupations.pop(random.randint(0, len(self.availableOccupations) - 1))
                        action[1].append(newOcc)
                        player.occupations.append(newOcc)
                    else:
                        player.occupations.append(self.availableOccupations.pop(random.randint(0, len(self.availableOccupations) - 1)))                        
                    for i in action[1]:
                        self.playOccupation(player, i)                        
                elif action[0] == 'BuildHouseBoat':
                    player.vikings -= 4
                    if action[1][0] != 'None':
                        self.playOccupation(player, action[1][0])
                    if action[1][1] != 'None':
                        player.resources['Stone'] -= 2
                        player.resources['Wood'] -= 2
                    if action[1][1] == 'StoneHouseLongship':
                        player.houses.append(House('StoneHouse'))
                        self.availableHouses.remove('StoneHouse')
                        player.longships.append(Boat('Longship'))
                    elif action[1][1] == 'LongHouseKnarr':
                        player.houses.append(House('LongHouse'))
                        self.availableHouses.remove('LongHouse')
                        player.longships.append(Boat('Knarr'))
                    elif action[1][1] == 'StoneHouse':
                        player.houses.append(House('StoneHouse'))
                        self.availableHouses.remove('StoneHouse')
                    elif action[1][1] == 'LongHouse':
                        player.houses.append(House('LongHouse'))
                        self.availableHouses.remove('LongHouse')
                    elif action[1][1] == 'Knarr':
                        player.longships.append(Boat('Knarr'))
                    elif action[1][1] == 'Longship':
                        player.longships.append(Boat('Longship'))
                elif action[0] == 'WhalingTwo':
                    player.vikings -= 4
                    if action[1][0] != 'None':
                        self.playOccupation(player, action[1][0])
                    if action[1][1] == 'WhalingTwo':
                        self.whalingTwo(player)
                elif action[0] == 'BuySheepAndCattle':
                    player.vikings -= 4
                    if action[1][0] != 'None':
                        self.playOccupation(player, action[1][0])
                    if action[1][1] != 'None':
                        player.resources['Silver'] -= 3
                        player.resources['Sheep'] += 1
                        player.resources['Cattle'] += 1
                elif action[0] == 'WeeklyMarketFour':
                    player.vikings -= 4
                    if action[1][0] != 'None':
                        self.playOccupation(player, action[1][0])
                    player.resources['Spices'] += 1
                    player.resources['Silver'] += 1
                    if player.resources['Cattle'] + player.resources['PregnantCattle'] >= 1:
                        player.resources['Milk'] += 2
                    if player.resources['Sheep'] + player.resources['PregnantSheep'] >= 1:
                        player.resources['Wool'] += 1
                elif action[0] == 'CraftingFour':
                    player.vikings -= 4
                    if action[1][0] != 'None':
                        self.playOccupation(player, action[1][0])
                    player.resources['Silver'] += 4
                    if action[1][1] == 'CraftRobe':
                        player.resources['Robe'] += 1
                        player.resources['Wool'] -= 1
                    if action[1][2] == 'CraftJewelry':
                        player.resources['Jewelry'] += 1
                        player.resources['Silverware'] -= 1
                elif action[0] == 'MountainFourUpgradeTwoTwice':
                    player.vikings -= 4
                    if action[1][0] != 'None':
                        self.playOccupation(player, action[1][0])
                    for i in range(action[1][2]):
                        if self.mountains[action[1][1]][0] == 'Silver':
                            player.resources['Silver'] += 1
                        player.resources[self.mountains[action[1][1]].pop(0)] += 1
                    if action[1][3] != 'None':
                        player.resources[action[1][3]] -= 1
                        player.resources[self.availableDoubleUpgrades[action[1][3]]] += 1
                    if action[1][4] != 'None':
                        player.resources[action[1][4]] -= 1
                        player.resources[self.availableDoubleUpgrades[action[1][4]]] += 1
                elif action[0] == 'MountainOrUpgrade':
                    player.vikings -= 4
                elif action[0] == 'Plundering':
                    player.vikings -= 4
                    if action[1][0] != 'None':
                        self.playOccupation(player, action[1][0])
                    if action[1][1] != 'None':
                        player.resources['SilverHoard'] += 1
                elif action[0] == 'EmigrateThree':              
                    player.vikings -= 4  
                    if action[1][0] != 'None':
                        self.playOccupation(player, action[1][0])
                    if action[1][1] != 'None':                        
                        player.resources['Silver'] -= self.round
                        if action[1][1] == 'Knarr':
                            player.emigratePoints += 21
                            player.knarrs.remove(0)
                        elif action[1][1] == 'Longship':
                            player.emigratePoints += 18
                            player.longships.remove(len(player.longships) - 1)
                        player.feastTable.remove(0)
                        player.feastTable.remove(0)
                    if action[1][2] != 'None':
                        player.whalingBoats.pop(len(player.whalingBoats) - 1)
                        player.knarrs.append(Boat('Knarr'))
                player.madeAction = True
            elif action[0] == 'FeastPlacements':
                for i in range(action[1][1]):
                    player.feastTable[action[1][4] + i] = [action[1][0],action[1][2],action[1][3]] 
                player.resources[action[1][0]] -= 1
            elif action[0] == 'BoardPlacements':
                for i in range(action[1][1]):
                    for j in range(action[1][2]):
                        if [i, j] not in action[1][3]:
                            player.boards[action[1][7]].tiles[action[1][9] + j][action[1][8] + i] = 'O' + action[1][6]    
                player.resources[action[1][0]] -= 1
            elif action[0] == 'Arm':
                if action[1][0] == 'Longship':
                    for i in range(len(player.longships)):
                        if player.longships[i].ore < 3:
                            player.longships[i].ore += 1
                            break                    
                if action[1][0] == 'WhalingBoat':
                    for i in range(len(player.whalingBoats)):
                        if player.whalingBoats[i].ore < 2:
                            player.whalingBoats[i].ore += 1
                            break
                player.resources['Ore'] -= 1
            elif action[0] == 'BuyBoat':
                if action[1][0] == 'WhalingBoat':
                    player.resources['Silver'] -= 3
                    player.whalingBoats.append(Boat('WhalingBoat'))                
                elif action[1][0] == 'Knarr':
                    player.resources['Silver'] -= 5
                    player.knarrs.append(Boat('Knarr'))
                elif action[1][0] == 'Longship':
                    player.resources['Silver'] -= 8
                    player.longships.append(Boat('Longship'))
            elif action[0] == 'PassTurn':
                passed = True
            elif action[0] == 'EndTurn':
                passed = True
                player.endedTurn = True  
        return player.endedTurn

    # Returns list of all possible actions
    def determineValidActions(self, player):
        # List of valid actions. First value of each list is name of action followed by list of variations of that action
        validActions = []
        
        # Add all board placements (expansion and main)
        validBoardPlacements = self.determineValidBoardPlacement(player)
        if len(validBoardPlacements) > 0:
            validActions += validBoardPlacements
         
        # Add all feast placements
        validFeastPlacements = self.determineValidFeastPlacement(player)
        if len(validFeastPlacements) > 0:
            validActions += validFeastPlacements
        
        # Add all house placements                
        validHousePlacements = self.determineValidHousePlacement(player)
        if len(validHousePlacements) > 0:
            validActions += validHousePlacements            
            
        # Option to completely end turn for the round
        validActions.append(['EndTurn',['EndTurn']])
        
        # Arm option
        if len(player.longships) > 0:
            if player.resources['Ore'] >= 1 and player.longships[len(player.longships) - 1].ore < 3:
                validActions.append(['Arm',['Longship']])
        if len(player.whalingBoats) > 0:
            if player.resources['Ore'] >= 1 and player.whalingBoats[len(player.whalingBoats) - 1].ore < 2:
                validActions.append(['Arm',['WhalingBoat']])
            
        # Buy boat option
        if player.resources['Silver'] >= 3 and len(player.whalingBoats) < 3:
            validActions.append(['BuyBoat',['WhalingBoat']])
        if player.resources['Silver'] >= 5 and len(player.knarrs) + len(player.longships) < 4:
            validActions.append(['BuyBoat',['Knarr']])        
        if player.resources['Silver'] >= 8 and len(player.knarrs) + len(player.longships) < 4:
            validActions.append(['BuyBoat',['Longship']])
        
        # Tanner
        if 'Tanner' in player.playedOccupations and player.resources['SaltMeat'] >= 1:
            validActions.append(['Tanner',['Tanner']])
            
        # Linen Weaver
        if 'LinenWeaver' in player.playedOccupations and player.resources['Flax'] >= 2 and player.resources['Silver'] >= 1:
            validActions.append(['LinenWeaver',['LinenWeaver']])
            
        # Arms Dealer
        if 'ArmsDealer' in player.playedOccupations and player.resources['Sword'] + player.resources['Bow'] + player.resources['Spear'] + player.resources['Snare'] >= 2:
            weaponCombinations = list(itertools.combinations(['Sword'] * player.resources['Sword'] + ['Bow'] * player.resources['Bow'] + ['Spear'] * player.resources['Spear'] + ['Snare'] * player.resources['Snare'], 2))
            for i in weaponCombinations:
                validActions.append(['ArmsDealer',i])
            
        # Farmer
        if 'Farmer' in player.playedOccupations and player.resources['Cattle'] + player.resources['PregnantCattle'] >= 1:
            if player.resources['Cattle'] >= 1:
                validActions.append(['Farmer',['Cattle']])
            if player.resources['PregnantCattle'] >= 1:
                validActions.append(['Farmer',['Farmer']])  
                
        # Rune Engraver
        if 'RuneEngraver' in player.playedOccupations and player.resources['Runestone'] >= 1:
            validActions.append(['RuneEngraver',['RuneEngraver']])
            
        # Lineseed Oil Presser
        if 'LinseedOilPresser' in player.playedOccupations and player.resources['Flax'] >= 2:
            validActions.append(['LinseedOilPresser',['LinseedOilPresser']])
            
        # Tradesman
        if 'Tradesman' in player.playedOccupations and player.resources['Silverware'] >= 1:
            validActions.append(['Tradesman',['Tradesman']])
                        
        # Tutor Blue
        if 'TutorBlue' in player.playedOccupations and player.resources['Silver'] >= 1 and len(player.occupations) > 0:
            for i in player.occupations:                
                validActions.append(['TutorBlue',[i]])            
        
        # Option to pass the turn to next player. Otherwise can play action
        if player.madeAction:
            validActions.append(['PassTurn',['PassTurn']])
        else:        
            # One viking actions
            if player.vikings >= 1:
                # Build Shed
                if player.resources['Wood'] >= 2 and 'Shed' in self.availableHouses and 'BuildShed' in self.availableActions:
                    validActions.append(['BuildShed',['BuildShed']])
                
                # Build Whaling Boat
                if player.resources['Wood'] >= 1 and len(player.whalingBoats) < 3 and 'BuildWhalingBoat' in self.availableActions:
                    validActions.append(['BuildWhalingBoat',['BuildWhalingBoat']])
                    
                # Hunting Game 1
                if 'HuntingGameOne' in self.availableActions:
                    validActions.append(['HuntingGameOne',['HuntingGameOne']])
                
                # Hunt Stockfish
                if 'HuntStockfish' in self.availableActions:
                    validActions.append(['HuntStockfish',['HuntStockfish']])
                
                # Buy Stockfish
                if player.resources['Silver'] >= 1 and 'BuyStockfish' in self.availableActions:
                    validActions.append(['BuyStockfish',['BuyStockfish']])
                    
                # Buy SaltMeat
                if player.resources['Silver'] >= 2 and 'BuySaltMeat' in self.availableActions:
                    validActions.append(['BuySaltMeat',['BuySaltMeat']])
                
                # Weekly Market 1
                if 'WeeklyMarketOne' in self.availableActions:
                    validActions.append(['WeeklyMarketOne',['WeeklyMarketOne']])
                
                # Products 1
                if player.resources['Cattle'] + player.resources['PregnantCattle'] >= 1 and 'ProductsOne' in self.availableActions:
                    validActions.append(['ProductsOne',['ProductsOne']])
                    
                # Craft Linen
                if player.resources['Flax'] >= 1 and 'CraftLinen' in self.availableActions:
                    validActions.append(['CraftLinen',['CraftLinen']])
                    
                # Craft Runestone
                if player.resources['Stone'] >= 1 and 'CraftRunestone' in self.availableActions:
                    validActions.append(['CraftRunestone',['CraftRunestone']])
                    
                # Mountain take two (1 or 2)
                if 'MountainTwo' in self.availableActions:
                    for i in range(len(self.mountains)):
                        if len(self.mountains[i]) >= 1:
                            validActions.append(['MountainTwo',[i, 1]])
                        if len(self.mountains[i]) >= 2:
                            validActions.append(['MountainTwo',[i, 2]])
                    
                # Mountain take 1 and upgrade (take 1, upgrade 1, or both)
                # Loop through upgrades
                if 'MountainOneUpgradeOne' in self.availableActions:
                    for i in self.availableSingleUpgrades:
                        # Loop through mountains
                        for j in range(len(self.mountains)):
                            # If has upgradeable resrouces
                            if player.resources[i] >= 1:
                                # If has mountain to take from
                                if len(self.mountains[j]) >= 1:
                                    validActions.append(['MountainOneUpgradeOne',[j, 1, i]])                            
                            # Add option to just take 1. This should trigger only once so add on one loop only
                            if i == 'Clothing' and len(self.mountains[j]) >= 1:
                                validActions.append(['MountainOneUpgradeOne',[j, 1, 'None']])                        
                        # Always add option to just upgrade
                        if player.resources[i] >= 1:
                            validActions.append(['MountainOneUpgradeOne',[0, 0, i]])
                    
                # Upgrade two action            
                if 'UpgradeTwo' in self.availableActions:
                    # List upgradeable resources player has, up to three times
                    upgradeableSingles = []
                    for i in self.availableSingleUpgrades:
                        if player.resources[i] >= 2:
                            upgradeableSingles.append(i)
                        if player.resources[i] >= 1:
                            upgradeableSingles.append(i)
                    # Create list of two combinations
                    for i in set(list(itertools.combinations(upgradeableSingles, 2))):
                        validActions.append(['UpgradeTwo',[i[0], i[1]]])
                    # Create list of one combinations
                    for i in set(list(itertools.combinations(upgradeableSingles, 1))):
                        validActions.append(['UpgradeTwo',[i[0]]])
                
                # Upgrade all greens one
                if 'UpgradeGreensOne' in self.availableActions:
                    validGreenUpgrades = []
                    if len(player.knarrs) >= 1 and player.resources['Silver'] >= 1:
                        for i in self.availableGreenUpgrades:
                            # Track all possible green upgrades
                            if player.resources[i] >= 1:
                                validGreenUpgrades.append(i)
                        # Populate list of every possible combination of valid green upgrades
                        print(validGreenUpgrades)
                        for i in range(len(validGreenUpgrades) + 1):
                            for j in itertools.combinations(validGreenUpgrades, i):
                                validActions.append(['UpgradeGreensOne',list(j)])
                            
                # Raiding
                if len(player.longships) >= 1 and 'Raiding' in self.availableActions:
                    validActions.append(['Raiding',['Raiding']])
                    
                # Exploration 1
                if len(player.whalingBoats) + len(player.longships) + len(player.knarrs) >= 1 and 'ExplorationOne' in self.availableActions:
                    if 'Shetland' in self.availableExplorationBoards:
                        validActions.append(['ExplorationOne',['Shetland']])
                    if 'FaroeIslands' in self.availableExplorationBoards:
                        validActions.append(['ExplorationOne',['FaroeIslands']])
                        
                # Draw Occupation
                if 'DrawOccupation' in self.availableActions:
                    validActions.append(['DrawOccupation',['DrawOccupation']])
                
                # Play Occupation
                if player.resources['Stone'] + player.resources['Ore'] >= 1 and 'PlayOccupationOne' in self.availableActions:
                    # Options to play any cards
                    for i in player.occupations:
                        if player.resources['Stone'] >= 1:
                            validActions.append(['PlayOccupationOne',['Stone', i]])
                        if player.resources['Ore'] >= 1:
                            validActions.append(['PlayOccupationOne',['Ore', i]])
                    # Options to play no cards
                    if player.resources['Stone'] >= 1:
                        validActions.append(['PlayOccupationOne',['Stone','None']])
                    if player.resources['Ore'] >= 1:
                        validActions.append(['PlayOccupationOne',['Ore','None']])
            
            # Two viking actions            
            if player.vikings >= 2:
                # Build StoneHouse
                if player.resources['Stone'] >= 1 and 'StoneHouse' in self.availableHouses and 'BuildStoneHouse' in self.availableActions:
                    validActions.append(['BuildStoneHouse',['BuildStoneHouse']])
                    
                # Build Knarr
                if player.resources['Wood'] >= 2 and len(player.knarrs) + len(player.longships) < 4 and 'BuildKnarr' in self.availableActions:
                    validActions.append(['BuildKnarr',['BuildKnarr']])
                    
                # Hunting Game two
                if 'HuntingGameTwo' in self.availableActions:
                    validActions.append(['HuntingGameTwo',['HuntingGameTwo']])
                    
                # Lay Snare
                if 'LaySnare' in self.availableActions:
                    validActions.append(['LaySnare',['LaySnare']])
                    
                # Buy Sheep
                if player.resources['Silver'] >= 1 and 'BuySheep' in self.availableActions:
                    validActions.append(['BuySheep',['BuySheep']])
                    
                # Buy Cattle              
                if player.resources['Silver'] >= 3 and 'BuyCattle' in self.availableActions:
                    validActions.append(['BuyCattle',['BuyCattle']])
                    
                # Weekly Market two
                if 'WeeklyMarketTwo' in self.availableActions:
                    validActions.append(['WeeklyMarketTwo',['WeeklyMarketTwo']])
                            
                # Products two
                if 'ProductsTwo' in self.availableActions:
                    validActions.append(['ProductsTwo',['ProductsTwo']])
                    
                # Make Clothing
                if player.resources['Hide'] >= 1 and player.resources['Linen'] >= 1 and 'CraftClothing' in self.availableActions:
                    validActions.append(['CraftClothing',['CraftClothing']])
    
                # Craft chest
                if player.resources['Wood'] + player.resources['Ore'] >= 1 and 'CraftChest' in self.availableActions:
                    if player.resources['Wood'] >= 1:
                        validActions.append(['CraftChest',['Wood']])                
                    if player.resources['Ore'] >= 1:
                        validActions.append(['CraftChest',['Ore']])
                        
                # Wood per player
                if 'WoodPerPlayer' in self.availableActions:
                    validActions.append(['WoodPerPlayer',['WoodPerPlayer']])
                    
                # Three mountain upgrade one
                # Loop through upgrades
                if 'MountainThreeUpgradeOne' in self.availableActions:
                    for i in self.availableSingleUpgrades:
                        # Loop through mountains
                        for j in range(len(self.mountains)):
                            # If has upgradeable resrouces
                            if player.resources[i] >= 1:
                                # If has mountain to take from
                                if len(self.mountains[j]) >= 3:
                                    validActions.append(['MountainThreeUpgradeOne',[j, 3, i]])  
                                if len(self.mountains[j]) >= 2:
                                    validActions.append(['MountainThreeUpgradeOne',[j, 2, i]])  
                                if len(self.mountains[j]) >= 1:
                                    validActions.append(['MountainThreeUpgradeOne',[j, 1, i]])                            
                            # Add option to just take 1. This should trigger only once so add on one loop only
                            if i == 'Clothing' and len(self.mountains[j]) >= 3:
                                validActions.append(['MountainThreeUpgradeOne',[j, 3, 'None']])  
                            if i == 'Clothing' and len(self.mountains[j]) >= 2:
                                validActions.append(['MountainThreeUpgradeOne',[j, 2, 'None']]) 
                            if i == 'Clothing' and len(self.mountains[j]) >= 1:
                                validActions.append(['MountainThreeUpgradeOne',[j, 1, 'None']]) 
                        # Always add option to just upgrade
                        if player.resources[i] >= 1:
                            validActions.append(['MountainThreeUpgradeOne',[0, 0, i]])   
                            
                # Upgrade Three
                if 'UpgradeThree' in self.availableActions:
                    # List upgradeable resources player has, up to three times
                    upgradeableSingles = []
                    for i in self.availableSingleUpgrades:
                        if player.resources[i] >= 3:
                            upgradeableSingles.append(i)
                        if player.resources[i] >= 2:
                            upgradeableSingles.append(i)
                        if player.resources[i] >= 1:
                            upgradeableSingles.append(i)
                    # Create list of three combinations
                    for i in set(list(itertools.combinations(upgradeableSingles, 3))):
                        validActions.append(['UpgradeThree',[i[0], i[1], i[2]]])
                    # Create list of two combinations
                    for i in set(list(itertools.combinations(upgradeableSingles, 2))):
                        validActions.append(['UpgradeThree',[i[0], i[1]]])
                    # Create list of one combinations
                    for i in set(list(itertools.combinations(upgradeableSingles, 1))):
                        validActions.append(['UpgradeThree',[i[0]]])
                     
                # Upgrade all greens two
                if 'UpgradeGreensTwo' in self.availableActions:
                    validGreenUpgrades = []
                    if len(player.knarrs) >= 1 and player.resources['Silver'] >= 1:
                        for i in self.availableGreenUpgrades:
                            # Track all possible green upgrades
                            if player.resources[i] >= 1:
                                validGreenUpgrades.append(i)
                        # Populate list of every possible combination of valid green upgrades
                        print(validGreenUpgrades)
                        for i in range(len(validGreenUpgrades) + 1):
                            for j in itertools.combinations(validGreenUpgrades, i):
                                validActions.append(['UpgradeGreensOne',list(j)])  
                                
                # Pillaging one
                if len(player.longships) >= 1 and 'PillagingOne' in self.availableActions:
                    validActions.append(['PillagingOne',['PillagingOne']])
                    
                # Exploration two            
                if len(player.longships) + len(player.knarrs) >= 1 and 'ExplorationTwo' in self.availableActions:
                    if 'Iceland' in self.availableExplorationBoards:
                        validActions.append(['ExplorationTwo',['Iceland']])
                    if 'Greenland' in self.availableExplorationBoards:
                        validActions.append(['ExplorationTwo',['Greenland']])
                    if 'BearIsland' in self.availableExplorationBoards:
                        validActions.append(['ExplorationTwo',['BearIsland']])
                        
                # Emigrate one
                if player.resources['Silver'] >= self.round and player.feastTable[0][0] == 'F' and player.feastTable[1][0] == 'F' and 'EmigrateOne' in self.availableActions:
                    if len(player.knarrs) >= 1:
                        validActions.append(['EmigrateOne',['Knarr']])
                    if len(player.longships) >= 1:
                        validActions.append(['EmigrateOne',['Longship']])
                        
                # Play occupations two
                if len(player.occupations) >= 1 and 'PlayOccupationsTwo' in self.availableActions:
                    # Playing two occupations
                    for i in list(itertools.combinations(player.occupations, 2)):
                        validActions.append(['PlayOccupationsTwo',[i[0],i[1]]])
                    # Playing one occupation
                    for i in list(itertools.combinations(player.occupations, 1)):
                        validActions.append(['PlayOccupationsTwo',[i[0]]])
            
            # Three viking actions. All of these will also have an option to just take occupation
            if player.vikings >= 3:
                # Build LongHouse
                if player.resources['Stone'] >= 2 and 'LongHouse' in self.availableHouses and 'BuildLongHouse' in self.availableActions:
                    validActions.append(['BuildLongHouse',['BuildLongHouse']])
                if 'BuildLongHouse' in self.availableActions:
                    validActions.append(['BuildLongHouse',['None']])
                    
                # Build Longship
                if player.resources['Wood'] >= 2 and len(player.knarrs) + len(player.longships) < 4 and 'BuildLongship' in self.availableActions:
                    validActions.append(['BuildLongship',['BuuildLongship']])
                if 'BuildLongship' in self.availableActions:
                    validActions.append(['BuildLongship',['None']])
                    
                # Whaling one
                if len(player.whalingBoats) >= 1 and 'WhalingOne' in self.availableActions:
                    validActions.append(['WhalingOne',['WhalingOne']])
                if 'WhalingOne' in self.availableActions:
                    validActions.append(['WhalingOne',['None']])
                
                # Buy Sheep or Cattle
                if player.resources['Silver'] >= 1 and 'BuySheepOrCattle' in self.availableActions:
                    validActions.append(['BuySheepOrCattle',['Cattle']])
                if 'BuySheepOrCattle' in self.availableActions:
                    validActions.append(['BuySheepOrCattle',['Sheep']])
                    
                # Weekly market three
                if 'WeeklyMarketThree' in self.availableActions:
                    validActions.append(['WeeklyMarketThree',['WeeklyMarketThree']])
                    
                # Products three
                if 'ProductsThree' in self.availableActions:
                    validActions.append(['ProductsThree',['ProductsThree']])
                    
                # Craft special tile
                if player.resources['Ore'] >= 1 and 'CraftSpecial' in self.availableActions:
                    for i in self.availableSpecialTiles:
                        validActions.append(['CraftSpecial',[i]])
                if 'CraftSpecial' in self.availableActions:
                    validActions.append(['CraftSpecial',['None']])
                    
                # Craft chests and runestones
                if player.resources['Stone'] >= 2 and player.resources['Stone'] >= 2 and 'CraftChestRunestone' in self.availableActions:
                    validActions.append(['CraftChestRunestones',['CraftChestRunestone']])
                if 'CraftChestRunestone' in self.availableActions:
                    validActions.append(['CraftChestRunestone',['None']])
                    
                # Mountain three and two
                
                # Upgrade three weapons
                if 'UpgradeThreeWeapons' in self.availableActions:
                    # List upgradeable resources player has, up to three times
                    upgradeableSingles = []
                    for i in self.availableSingleUpgrades:
                        if player.resources[i] >= 3:
                            upgradeableSingles.append(i)
                        if player.resources[i] >= 2:
                            upgradeableSingles.append(i)
                        if player.resources[i] >= 1:
                            upgradeableSingles.append(i)
                    # Create list of three combinations
                    for i in set(list(itertools.combinations(upgradeableSingles, 3))):
                        validActions.append(['UpgradeThreeWeapons',[i[0], i[1], i[2]]])
                    # Create list of two combinations
                    for i in set(list(itertools.combinations(upgradeableSingles, 2))):
                        validActions.append(['UpgradeThreeWeapons',[i[0], i[1]]])
                    # Create list of one combinations
                    for i in set(list(itertools.combinations(upgradeableSingles, 1))):
                        validActions.append(['UpgradeThreeWeapons',[i[0]]])
                    # Option to upgrade none
                    validActions.append(['UpgradeThreeWeapons',[]])
                    
                # Upgrade four
                if 'UpgradeFour' in self.availableActions:
                    # List upgradeable resources player has, up to three times
                    upgradeableSingles = []
                    for i in self.availableSingleUpgrades:
                        if player.resources[i] >= 4:
                            upgradeableSingles.append(i)
                        if player.resources[i] >= 3:
                            upgradeableSingles.append(i)
                        if player.resources[i] >= 2:
                            upgradeableSingles.append(i)
                        if player.resources[i] >= 1:
                            upgradeableSingles.append(i)
                    # Create list of four combinations
                    for i in set(list(itertools.combinations(upgradeableSingles, 4))):
                        validActions.append(['UpgradeFour',[i[0], i[1], i[2], i[3]]])
                    # Create list of three combinations
                    for i in set(list(itertools.combinations(upgradeableSingles, 3))):
                        validActions.append(['UpgradeFour',[i[0], i[1], i[2]]])
                    # Create list of two combinations
                    for i in set(list(itertools.combinations(upgradeableSingles, 2))):
                        validActions.append(['UpgradeFour',[i[0], i[1]]])
                    # Create list of one combinations
                    for i in set(list(itertools.combinations(upgradeableSingles, 1))):
                        validActions.append(['UpgradeFour',[i[0]]])
                    # Option to upgrade none
                    validActions.append(['UpgradeFour',[]])
                    
                # Buy special tiles
                if len(player.knarrs) >= 1 and 'BuySpecials' in self.availableActions:
                    for i in self.availableSpecialTiles:
                        for j in self.availableSpecialTiles:
                            # Buy two specials
                            if i != j and player.resources['Silver'] >= self.availableSpecialTiles[i] + self.availableSpecialTiles[j] :
                                validActions.append(['BuySpecials',[i,j]])
                        # Buy one special
                        if player.resources['Silver'] >= self.availableSpecialTiles[i]:
                            validActions.append(['BuySpecials',[i]])
                if 'BuySpecials' in self.availableActions:
                    validActions.append(['BuySpecials',[]])
                    
                # Pillaging two
                if len(player.longships) >= 1 and 'PillagingTwo' in self.availableActions:
                    validActions.append(['PillagingTwo',['PillagingTwo']])
                if 'PillagingTwo' in self.availableActions:
                    validActions.append(['PillagingTwo',['None']])
                    
                # Exploration three         
                if len(player.longships) >= 1 and 'ExplorationThree' in self.availableActions:
                    if 'BaffinIsland' in self.availableExplorationBoards:
                        validActions.append(['ExplorationThree',['BaffinIsland']])
                    if 'Labrador' in self.availableExplorationBoards:
                        validActions.append(['ExplorationThree',['Labrador']])
                    if 'Newfoundland' in self.availableExplorationBoards:
                        validActions.append(['ExplorationThree',['Newfoundland']])
                if 'ExplorationThree' in self.availableActions:
                    validActions.append(['ExplorationThree',['None']])
                    
                # Emigrate two
                if player.resources['Silver'] >= self.round and player.feastTable[0][0] == 'F' and player.feastTable[1][0] == 'F' and 'EmigrateTwo' in self.availableActions:
                    if len(player.knarrs) >= 1:
                        validActions.append(['EmigrateTwo',['Knarr']])
                    if len(player.longships) >= 1:
                        validActions.append(['EmigrateTwo',['Longship']])  
                if 'EmigrateTwo' in self.availableActions:
                    validActions.append(['EmigrateTwo',['None']])    
                    
                # Play occupations three
                if 'PlayOccupationsThree' in self.availableActions:
                    # Playing four occupations
                    for i in list(itertools.combinations(player.occupations + ['Drawn'], 4)):
                        validActions.append(['PlayOccupationsThree',[i[0],i[1],i[2],i[3]]])
                    # Playing three occupations
                    for i in list(itertools.combinations(player.occupations + ['Drawn'], 3)):
                        validActions.append(['PlayOccupationsThree',[i[0],i[1],i[2]]])
                    # Playing two occupations
                    for i in list(itertools.combinations(player.occupations + ['Drawn'], 2)):
                        validActions.append(['PlayOccupationsThree',[i[0],i[1]]])
                    # Playing one occupation
                    for i in list(itertools.combinations(player.occupations + ['Drawn'], 1)):
                        validActions.append(['PlayOccupationsThree',[i[0]]])
                    validActions.append(['PlayOccupationsThree',[]])
                    
            # Four viking actions. These will also have an option to just play an occupation if they have one
            if player.vikings >= 4:
                # Build house and boat
                if player.resources['Stone'] >= 2 and player.resources['Wood'] >= 2 and 'BuildHouseBoat' in self.availableActions:
                    for i in player.occupations + ['None']:
                        if 'StoneHouse' in self.availableHouses and len(player.longships) + len(player.knarrs) < 4:
                            validActions.append(['BuildHouseBoat',[i,'StoneHouseLongship']])
                        if 'LongHouse' in self.availableHouses and len(player.longships) + len(player.knarrs) < 4:
                            validActions.append(['BuildHouseBoat',[i,'LongHouseKnarr']])
                        if 'StoneHouse' in self.availableHouses:
                            validActions.append(['BuildHouseBoat',[i,'StoneHouse']])
                        if 'LongHouse' in self.availableHouses:
                            validActions.append(['BuildHouseBoat',[i,'LongHouse']])
                        if len(player.longships) + len(player.knarrs) < 4:
                            validActions.append(['BuildHouseBoat',[i,'Knarr']])
                            validActions.append(['BuildHouseBoat',[i,'Longship']])
                if len(player.occupations) >= 1 and 'BuildHouseBoat' in self.availableActions:
                    for i in player.occupations:
                        validActions.append(['BuildHouseBoat',[i,'None']])
                        
                # Whaling two
                if len(player.whalingBoats) >= 1 and 'WhalingTwo' in self.availableActions:
                    for i in player.occupations + ['None']:
                        validActions.append(['WhalingTwo',[i,'WhalingTwo']])
                if len(player.occupations) >= 1 and 'WhalingTwo' in self.availableActions:
                    for i in player.occupations:
                        validActions.append(['WhalingTwo',[i,'None']])
                        
                # Buy sheep and cattle            
                if player.resources['Silver'] >= 3 and 'BuySheepAndCattle' in self.availableActions:
                    for i in player.occupations + ['None']:
                        validActions.append(['BuySheepAndCattle',[i,'BuySheepAndCattle']])
                if len(player.occupations) >= 1 and 'BuySheepAndCattle' in self.availableActions:
                    for i in player.occupations:
                        validActions.append(['BuySheepAndCattle',[i,'None']])
                        
                # Weekly market four
                if 'WeeklyMarketFour' in self.availableActions:
                    for i in player.occupations + ['None']:
                        validActions.append(['WeeklyMarketFour',[i,'WeeklyMarketFour']])
                        
                # Crafting four
                if 'CraftingFour' in self.availableActions:
                    for i in player.occupations + ['None']:
                        validActions.append(['CraftingFour',[i,'None','None']])
                        if player.resources['Wool'] >= 1:
                            validActions.append(['CraftingFour',[i,'CrafRobe','None']])
                        if player.resources['Silverware'] >= 1:
                            validActions.append(['CraftingFour',[i,'None','CraftJewelry']])
                        if player.resources['Wool'] >= 1 and player.resources['Silverware'] >= 1:
                            validActions.append(['CraftingFour',[i,'CrafRobe','CraftJewelry']])
                        
                # Take four mountain upgrade two twice
                if 'MountainFourUpgradeTwoTwice' in self.availableActions:
                    # Get list of all two double upgrades
                    upgradeableDoubles = []
                    validDoubleUpgrades = []
                    for i in self.availableDoubleUpgrades:
                        if player.resources[i] >= 2:
                            upgradeableDoubles.append(i)
                        if player.resources[i] >= 1:
                            upgradeableDoubles.append(i)                    
                    # Create list of two combinations
                    for i in set(list(itertools.combinations(upgradeableDoubles, 2))):
                        validDoubleUpgrades.append([i[0],i[1]])
                    # Create list of one combinations
                    for i in set(list(itertools.combinations(upgradeableDoubles, 1))):
                        validDoubleUpgrades.append([i[0],'None'])
                    validDoubleUpgrades.append(['None','None'])
                    # Loop through occupations
                    for i in player.occupations + ['None']:
                        # Loop through valid double upgrades
                        for j in validDoubleUpgrades:
                            # Loop through mountains
                            for k in range(len(self.mountains)):
                                if len(self.mountains[k]) >= 4:
                                    validActions.append(['MountainFourUpgradeTwoTwice',[i, k, 4] + j])
                                if len(self.mountains[k]) >= 3:
                                    validActions.append(['MountainFourUpgradeTwoTwice',[i, k, 3] + j])
                                if len(self.mountains[k]) >= 2:
                                    validActions.append(['MountainFourUpgradeTwoTwice',[i, k, 2] + j])
                                if len(self.mountains[k]) >= 1:
                                    validActions.append(['MountainFourUpgradeTwoTwice',[i, k, 1] + j])                              
                            validActions.append(['MountainFourUpgradeTwoTwice',[i, 0, 0] + j])  
                    validActions.remove(['MountainFourUpgradeTwoTwice', [i, 0, 0, 'None', 'None']])               
            
            
                # Take two from four mountains or upgrade three twice. WORKING ON LOGIC FOR MOUNTAIN
                if len(player.occupations) >= 1 and 'MountainOrUpgrade' in self.availableActions:
                    # Get list of all two double upgrades
                    upgradeableDoubles = []
                    validDoubleUpgrades = []
                    for i in self.availableDoubleUpgrades:
                        if player.resources[i] >= 2:
                            upgradeableDoubles.append(i)
                        if player.resources[i] >= 1:
                            upgradeableDoubles.append(i)     
                    # Create list of two combinations
                    for i in set(list(itertools.combinations(upgradeableDoubles, 2))):
                        validDoubleUpgrades.append([i[0],i[1]])
                    # Create list of one combinations
                    for i in set(list(itertools.combinations(upgradeableDoubles, 1))):
                        validDoubleUpgrades.append([i[0],'None'])
                    # Add each double upgrade with each possible occupation
                    for i in player.occupations + ['None']:
                        for j in validDoubleUpgrades:
                            validActions.append(['MountainOrUpgrade',[i,'Upgrade'] + j])
                            
                    # List all combinations of up to four mountains
                    validMountains = list(itertools.combinations(range(len(self.mountains)),4)) + list(itertools.combinations(range(len(self.mountains)),3)) + list(itertools.combinations(range(len(self.mountains)),2)) + list(itertools.combinations(range(len(self.mountains)),1)) 
                    # Loop through each occupation
                    for i in player.occupations + ['None']:
                        # Loop through each combination
                        for j in validMountains:
                            # Loop through each mountain of each combination, storing possible mountain taking in m
                            m = []
                            for k in j:
                                if len(self.mountains[k]) >= 2:
                                    m.append([k, 2])                            
                                m.append([k, 1])
                            if len(m) == 4:
                                validActions.append(['MountainOrUpgrade',[i,'Mountain',m[0][0],m[0][1],m[1][0],m[1][1],m[2][0],m[2][1],m[3][0],m[3][1]]])
                            if len(m) == 3:
                                validActions.append(['MountainOrUpgrade',[i,'Mountain',m[0][0],m[0][1],m[1][0],m[1][1],m[2][0],m[2][1],0,0]])
                            if len(m) == 2:
                                validActions.append(['MountainOrUpgrade',[i,'Mountain',m[0][0],m[0][1],m[1][0],m[1][1],0,0,0,0]])
                            if len(m) == 1:
                                validActions.append(['MountainOrUpgrade',[i,'Mountain',m[0][0],m[0][1],0,0,0,0,0,0]])
                if len(player.occupations) >= 1 and 'MountainOrUpgrade' in self.availableActions:
                    for i in player.occupations:
                        validActions.append(['MountainOrUpgrade',[i,'None']])
                        
                # Plundering
                if len(player.longships) >= 2 and len(player.occupations) >= 1 and 'Plundering' in self.availableActions:
                    for i in player.occupations:
                        validActions.append(['Plundering',[i,'Plundering']]) 
                if len(player.occupations) >= 1 and 'Plundering' in self.availableActions:
                    for i in player.occupations:
                        validActions.append(['Plundering',[i,'None']])           
                        
                # Emigrate three
                if player.resources['Silver'] >= self.round and player.feastTable[0][0] == 'F' and player.feastTable[1][0] == 'F' and 'EmigrateThree' in self.availableActions:
                    for i in player.occupations + ['None']:
                        if len(player.knarrs) >= 1 and len(player.whalingBoats) >= 1:
                            validActions.append(['EmigrateThree',[i,'Knarr','WhalingBoat']])  
                        if len(player.longships) >= 1 and len(player.whalingBoats) >= 1:
                            validActions.append(['EmigrateThree',[i,'Longship','WhalingBoat']])  
                        if len(player.knarrs) >= 1:
                            validActions.append(['EmigrateThree',[i,'Knarr','None']])  
                        if len(player.longships) >= 1:
                            validActions.append(['EmigrateThree',[i,'Longship','None']])  
                if len(player.occupations) >= 1 and 'EmigrateThree' in self.availableActions:
                    for i in player.occupations + ['None']:
                        if len(player.whalingBoats) >= 1 and len(player.knarrs) + len(player.longships) < 4:                        
                            validActions.append(['EmigrateThree',[i,'None','WhalingBoat']])  
                        validActions.append(['EmigrateThree',[i,'None','None']]) 
                    validActions.remove(['EmigrateThree',['None','None','None']])
                  
        
        return validActions
        
         
    # Returns list of possible board (main and exploration) placements
    def determineValidBoardPlacement(self, player):
        # Name possible tiles: contains info on length; width; missing spots [X,Y]; rotations horizontal, left, upsidedown or right(H, L, U, or R); flipped (True or False); and colors (O, R, G, or B)
        tileTemplate = [['Oil',2,1,[],'H',False,'G'],
                        ['Oil',1,2,[],'L',False,'G'],
                        ['Hide',3,1,[],'H',False,'G'],
                        ['Hide',1,3,[],'L',False,'G'],
                        ['Linen',4,1,[],'H',False,'G'],
                        ['Linen',1,4,[],'L',False,'G'],
                        ['SkinAndBones',3,2,[],'H',False,'G'],
                        ['SkinAndBones',2,3,[],'L',False,'G'],
                        ['Fur',4,2,[],'H',False,'G'],
                        ['Fur',2,4,[],'L',False,'G'],
                        ['Clothing',4,3,[],'H',False,'G'],
                        ['Clothing',3,4,[],'L',False,'G'],
                        ['Wool',2,2,[],'H',False,'G'],
                        ['Robe',3,3,[],'H',False,'G'],
                        ['Runestone',2,1,[],'H',False,'B'],
                        ['Runestone',1,2,[],'L',False,'B'],
                        ['Silverware',3,1,[],'H',False,'B'],
                        ['Silverware',1,3,[],'L',False,'B'],
                        ['Silk',4,1,[],'H',False,'B'],
                        ['Silk',1,4,[],'L',False,'B'],
                        ['Spices',3,2,[],'H',False,'B'],
                        ['Spices',2,3,[],'L',False,'B'],
                        ['Jewelry',4,2,[],'H',False,'B'],
                        ['Jewelry',2,4,[],'L',False,'B'],
                        ['SilverHoard',4,3,[],'H',False,'B'],
                        ['SilverHoard',3,4,[],'L',False,'B'],
                        ['Chest',2,2,[],'H',False,'B'],
                        ['TreasureChest',3,3,[],'H',False,'B'],
                        ['Silver',1,1,[],'H',False,'B'],
                        ['Ore',1,1,[],'H',False,'B'],
                        ['GlassBeads',3,3,[[0,0],[2,0],[0,2],[2,2]],'H',False,'B'],
                        ['Helmet',2,3,[[1,0]],'H',False,'B'],
                        ['Helmet',3,2,[[2,1]],'L',False,'B'],
                        ['Helmet',2,3,[[0,2]],'U',False,'B'],
                        ['Helmet',3,2,[[0,0]],'R',False,'B'],
                        ['Helmet',2,3,[[0,0]],'H',True,'B'],
                        ['Helmet',3,2,[[2,0]],'L',True,'B'],
                        ['Helmet',2,3,[[1,2]],'U',True,'B'],
                        ['Helmet',3,2,[[0,1]],'R',True,'B'],
                        ['Cloakpin',4,2,[[1,1],[2,1],[3,1]],'H',False,'B'],
                        ['Cloakpin',2,4,[[0,1],[0,2],[0,3]],'L',False,'B'],
                        ['Cloakpin',4,2,[[0,0],[0,1],[0,2]],'U',False,'B'],
                        ['Cloakpin',2,4,[[1,0],[1,1],[1,2]],'R',False,'B'],
                        ['Cloakpin',4,2,[[0,1],[1,1],[2,1]],'H',True,'B'],
                        ['Cloakpin',2,4,[[0,0],[0,1],[0,2]],'L',True,'B'],
                        ['Cloakpin',4,2,[[0,1],[0,2],[0,3]],'U',True,'B'],
                        ['Cloakpin',2,4,[[1,1],[1,2],[1,3]],'R',True,'B'],
                        ['Belt',5,1,[],'H',False,'B'],
                        ['Belt',1,5,[],'L',False,'B'],
                        ['Crucifix',3,4,[[0,0],[0,1],[0,3],[2,0],[2,1],[2,3]],'H',False,'B'],
                        ['Crucifix',4,3,[[0,0],[0,2],[2,0],[2,2],[3,0],[3,2]],'L',False,'B'],
                        ['Crucifix',3,4,[[0,0],[0,2],[0,3],[2,0],[2,2],[2,3]],'U',False,'B'],
                        ['Crucifix',4,3,[[0,0],[0,2],[1,0],[1,2],[3,0],[3,2]],'R',False,'B'],
                        ['DrinkingHorn',3,3,[[0,2],[1,0],[2,0]],'H',False,'B'],
                        ['DrinkingHorn',3,3,[[0,0],[2,1],[2,2]],'L',False,'B'],
                        ['DrinkingHorn',3,3,[[0,2],[1,2],[2,0]],'U',False,'B'],
                        ['DrinkingHorn',3,3,[[0,0],[0,1],[2,2]],'R',False,'B'],
                        ['DrinkingHorn',3,3,[[0,0],[0,1],[2,2]],'H',True,'B'],
                        ['DrinkingHorn',3,3,[[0,2],[2,0],[2,1]],'L',True,'B'],
                        ['DrinkingHorn',3,3,[[0,0],[1,2],[2,2]],'U',True,'B'],
                        ['DrinkingHorn',3,3,[[0,1],[0,2],[2,0]],'R',True,'B'],
                        ['AmberFigure',3,3,[[0,2],[2,2]],'H',False,'B'],
                        ['AmberFigure',3,3,[[0,0],[0,2]],'R',False,'B'],
                        ['AmberFigure',3,3,[[0,0],[2,0]],'U',False,'B'],
                        ['AmberFigure',3,3,[[2,0],[2,2]],'L',False,'B'],
                        ['Horseshoe',3,3,[[1,1],[1,2]],'H',False,'B'],
                        ['Horseshoe',3,3,[[0,1],[1,1]],'L',False,'B'],
                        ['Horseshoe',3,3,[[1,0],[1,1]],'U',False,'B'],
                        ['Horseshoe',3,3,[[1,1],[2,1]],'R',False,'B'],
                        ['GoldBrooch',3,4,[[0,0],[0,3],[2,0],[2,3]],'H',False,'B'],
                        ['GoldBrooch',4,3,[[0,0],[0,2],[3,0],[3,2]],'L',False,'B'],
                        ['Fibula',3,5,[[1,1],[1,3],[2,0],[2,1],[2,3],[2,4]],'H',False,'B'],
                        ['Fibula',5,3,[[0,2],[1,1],[1,2],[3,1],[3,2],[4,2]],'L',False,'B'],
                        ['Fibula',3,5,[[0,0],[0,1],[0,3],[0,4],[1,1],[1,3]],'U',False,'B'],
                        ['Fibula',5,3,[[0,0],[1,0],[1,1],[3,0],[3,1],[4,0]],'R',False,'B'],
                        ['ThrowingAxe',5,3,[[0,0],[0,1],[1,0],[3,0],[4,0],[4,1]],'H',False,'B'],
                        ['ThrowingAxe',3,5,[[1,0],[1,4],[2,0],[2,1],[2,3],[2,4]],'L',False,'B'],
                        ['ThrowingAxe',5,3,[[0,1],[0,2],[1,2],[3,2],[4,1],[4,2]],'U',False,'B'],
                        ['ThrowingAxe',3,5,[[0,0],[0,1],[0,3],[0,4],[1,0],[1,4]],'R',False,'B'],
                        ['ForgeHammer',3,5,[[0,0],[0,1],[0,2],[2,0],[2,1],[2,2]],'H',False,'B'],
                        ['ForgeHammer',5,3,[[2,0],[2,2],[3,0],[3,2],[4,0],[4,2]],'L',False,'B'],
                        ['ForgeHammer',3,5,[[0,2],[0,3],[0,4],[2,2],[2,3],[2,4]],'U',False,'B'],
                        ['ForgeHammer',5,3,[[0,0],[0,2],[1,0],[1,2],[2,0],[2,2]],'R',False,'B'],
                        ['Chalice',3,4,[[0,1],[2,1]],'H',False,'B'],
                        ['Chalice',4,3,[[2,0],[2,2]],'L',False,'B'],
                        ['Chalice',3,4,[[0,2],[2,2]],'U',False,'B'],
                        ['Chalice',4,3,[[1,0],[1,2]],'R',False,'B'],
                        ['RoundShield',4,4,[[0,0],[0,3],[3,0],[3,3]],'H',False,'B'],
                        ['EnglishCrown',5,3,[[1,2],[3,2]],'H',False,'B'],
                        ['EnglishCrown',3,5,[[0,1],[0,3]],'L',False,'B'],
                        ['EnglishCrown',5,3,[[1,0],[3,0]],'U',False,'B'],
                        ['EnglishCrown',3,5,[[2,1],[2,3]],'R',False,'B']]      
                    
        tile = []
        
        # Only keep tile the player has
        for i in tileTemplate:
            if player.resources[i[0]] > 0:
                tile.append(i)

        possiblePlacements = []
        
        # Loop through each house, spot, and tile
        for i in range(len(player.boards)):               
            # Loop through board length
            for j in range(len(player.boards[i].tiles[0])):
                # Loop through board height
                for k in range(len(player.boards[i].tiles)):                        
                    # Loop through each tile
                    for l in range(len(tile)):   
                        # Check if spot is free, Bonus, or Income
                        if player.boards[i].tiles[k][j] in ['F','P'] or player.boards[i].tiles[k][j][0:5] == 'Bonus' or player.boards[i].tiles[k][j][0:6] == 'Income' or [0,0] in tile[l][3]:
                            validPlacement = True   
                            # Loop through length of tile
                            for m in range(tile[l][1]):
                                # Loop through height of tile
                                for n in range(tile[l][2]):
                                    # Check if its on the board
                                    if len(player.boards[i].tiles[0]) <= j + m or len(player.boards[i].tiles) <= k + n:
                                        validPlacement = False
                                        continue
                                    
                                    # Reject if spot is not free or Bonus. Include special tile logic
                                    if player.boards[i].tiles[k + n][j + m] not in ['F','P'] and player.boards[i].tiles[k + n][j + m][0:5] != 'Bonus' and player.boards[i].tiles[k + n][j + m][0:6] != 'Income' and [m, n] not in tile[l][3]: 
                                        validPlacement = False
                                        continue
                                    
                                    # Checks for greens
                                    if tile[l][6] == 'G':
                                        # If at left of tile
                                        if m == 0 and j + m != 0:
                                            if player.boards[i].tiles[k + n][j + m - 1] == 'OG':
                                                validPlacement = False
                                                continue
                                            
                                        # If at right of tile
                                        if m == tile[l][1] - 1 and j + m != len(player.boards[i].tiles[0]) - 1:
                                            if player.boards[i].tiles[k + n][j + m  + 1] == 'OG':
                                                validPlacement = False
                                                continue 
                                            
                                        # If at top of tile
                                        if n == tile[l][2] - 1 and k + n != len(player.boards[i].tiles) - 1:
                                            if player.boards[i].tiles[k + n + 1][j + m ] == 'OG':
                                                validPlacement = False
                                                continue    
                                            
                                        # If at bottom of tile
                                        if n == 0 and k + n != 0:
                                            if player.boards[i].tiles[k + n - 1][j + m ] == 'OG':
                                                validPlacement = False
                                                continue
                                                                        
                                    # Check for valid income by checking if every spot below and to left of income is filled or being filled
                                    if player.boards[i].tiles[k + n][j + m][0:6] == 'Income':
                                        # Loop through left of income
                                        for o in range(j + m + 1):
                                            # Loop through bottom of income
                                            for p in range(k + n + 1):
                                                # Check if tile is not free or if not occupied                                                                                                
                                                if (player.boards[i].tiles[p][o] in ['F','P'] or player.boards[i].tiles[p][o][0:6] == 'Income') and not (o < j + tile[l][1] and o >= j and p < k + tile[l][2] and p >= k and [o - j, p - k] not in tile[l][3]):
                                                    validPlacement = False
                                                    break       
                                            # Quit loop if already failed    
                                            if validPlacement == False:
                                                break
                                                
                                # Quit loop if already failed    
                                if validPlacement == False:
                                    break
                                    
                            if validPlacement:
                                possiblePlacements.append(['BoardPlacements',tile[l] + [i, j, k]])
                               
        return possiblePlacements
    
    def determineValidHousePlacement(self, player):
        # Name possible tiles: contains info on length; width; missing spots [X,Y]; rotations horizontal, left, upsidedown or right(H, L, U, or R); flipped (True or False); and colors (O, R, G, or B)
        tileTemplate = [['Peas',2,1,[],'H',False,'O'],
                        ['Peas',1,2,[],'L',False,'O'],
                        ['Flax',3,1,[],'H',False,'O'],
                        ['Flax',1,3,[],'L',False,'O'],
                        ['Grain',4,1,[],'H',False,'O'],
                        ['Grain',1,4,[],'L',False,'O'],
                        ['Cabbage',3,2,[],'H',False,'O'],
                        ['Cabbage',2,3,[],'L',False,'O'],
                        ['Beans',2,2,[],'H',False,'O'],
                        ['Fruits',3,3,[],'H',False,'O'],
                        ['Mead',2,1,[],'H',False,'R'],
                        ['Mead',1,2,[],'L',False,'R'],
                        ['Stockfish',3,1,[],'H',False,'R'],
                        ['Stockfish',1,3,[],'L',False,'R'],
                        ['SaltMeat',4,1,[],'H',False,'R'],
                        ['SaltMeat',1,4,[],'L',False,'R'],
                        ['GameMeat',3,2,[],'H',False,'R'],
                        ['GameMeat',2,3,[],'L',False,'R'],
                        ['Milk',2,2,[],'H',False,'R'],
                        ['WhaleMeat',3,3,[],'H',False,'R'],
                        ['Oil',2,1,[],'H',False,'G'],
                        ['Oil',1,2,[],'L',False,'G'],
                        ['Hide',3,1,[],'H',False,'G'],
                        ['Hide',1,3,[],'L',False,'G'],
                        ['Linen',4,1,[],'H',False,'G'],
                        ['Linen',1,4,[],'L',False,'G'],
                        ['SkinAndBones',3,2,[],'H',False,'G'],
                        ['SkinAndBones',2,3,[],'L',False,'G'],
                        ['Wool',2,2,[],'H',False,'G'],
                        ['Robe',3,3,[],'H',False,'G'],
                        ['Runestone',2,1,[],'H',False,'B'],
                        ['Runestone',1,2,[],'L',False,'B'],
                        ['Silverware',3,1,[],'H',False,'B'],
                        ['Silverware',1,3,[],'L',False,'B'],
                        ['Silk',4,1,[],'H',False,'B'],
                        ['Silk',1,4,[],'L',False,'B'],
                        ['Spices',3,2,[],'H',False,'B'],
                        ['Spices',2,3,[],'L',False,'B'],
                        ['Chest',2,2,[],'H',False,'B'],
                        ['TreasureChest',3,3,[],'H',False,'B'],
                        ['Silver',1,1,[],'H',False,'B'],
                        ['GlassBeads',3,3,[[0,0],[2,0],[0,2],[2,2]],'H',False,'B'],
                        ['Helmet',2,3,[[1,0]],'H',False,'B'],
                        ['Helmet',3,2,[[2,1]],'L',False,'B'],
                        ['Helmet',2,3,[[0,2]],'U',False,'B'],
                        ['Helmet',3,2,[[0,0]],'R',False,'B'],
                        ['Helmet',2,3,[[0,0]],'H',True,'B'],
                        ['Helmet',3,2,[[2,0]],'L',True,'B'],
                        ['Helmet',2,3,[[1,2]],'U',True,'B'],
                        ['Helmet',3,2,[[0,1]],'R',True,'B'],
                        ['Cloakpin',4,2,[[1,1],[2,1],[3,1]],'H',False,'B'],
                        ['Cloakpin',2,4,[[0,1],[0,2],[0,3]],'L',False,'B'],
                        ['Cloakpin',4,2,[[0,0],[0,1],[0,2]],'U',False,'B'],
                        ['Cloakpin',2,4,[[1,0],[1,1],[1,2]],'R',False,'B'],
                        ['Cloakpin',4,2,[[0,1],[1,1],[2,1]],'H',True,'B'],
                        ['Cloakpin',2,4,[[0,0],[0,1],[0,2]],'L',True,'B'],
                        ['Cloakpin',4,2,[[0,1],[0,2],[0,3]],'U',True,'B'],
                        ['Cloakpin',2,4,[[1,1],[1,2],[1,3]],'R',True,'B'],
                        ['Belt',5,1,[],'H',False,'B'],
                        ['Belt',1,5,[],'L',False,'B'],
                        ['Crucifix',3,4,[[0,0],[0,1],[0,3],[2,0],[2,1],[2,3]],'H',False,'B'],
                        ['Crucifix',4,3,[[0,0],[0,2],[2,0],[2,2],[3,0],[3,2]],'L',False,'B'],
                        ['Crucifix',3,4,[[0,0],[0,2],[0,3],[2,0],[2,2],[2,3]],'U',False,'B'],
                        ['Crucifix',4,3,[[0,0],[0,2],[1,0],[1,2],[3,0],[3,2]],'R',False,'B'],
                        ['DrinkingHorn',3,3,[[0,2],[1,0],[2,0]],'H',False,'B'],
                        ['DrinkingHorn',3,3,[[0,0],[2,1],[2,2]],'L',False,'B'],
                        ['DrinkingHorn',3,3,[[0,2],[1,2],[2,0]],'U',False,'B'],
                        ['DrinkingHorn',3,3,[[0,0],[0,1],[2,2]],'R',False,'B'],
                        ['DrinkingHorn',3,3,[[0,0],[0,1],[2,2]],'H',True,'B'],
                        ['DrinkingHorn',3,3,[[0,2],[2,0],[2,1]],'L',True,'B'],
                        ['DrinkingHorn',3,3,[[0,0],[1,2],[2,2]],'U',True,'B'],
                        ['DrinkingHorn',3,3,[[0,1],[0,2],[2,0]],'R',True,'B'],
                        ['AmberFigure',3,3,[[0,2],[2,2]],'H',False,'B'],
                        ['AmberFigure',3,3,[[0,0],[0,2]],'R',False,'B'],
                        ['AmberFigure',3,3,[[0,0],[2,0]],'U',False,'B'],
                        ['AmberFigure',3,3,[[2,0],[2,2]],'L',False,'B'],
                        ['Horseshoe',3,3,[[1,1],[1,2]],'H',False,'B'],
                        ['Horseshoe',3,3,[[0,1],[1,1]],'L',False,'B'],
                        ['Horseshoe',3,3,[[1,0],[1,1]],'U',False,'B'],
                        ['Horseshoe',3,3,[[1,1],[2,1]],'R',False,'B'],
                        ['GoldBrooch',3,4,[[0,0],[0,3],[2,0],[2,3]],'H',False,'B'],
                        ['GoldBrooch',4,3,[[0,0],[0,2],[3,0],[3,2]],'L',False,'B'],
                        ['Fibula',3,5,[[1,1],[1,3],[2,0],[2,1],[2,3],[2,4]],'H',False,'B'],
                        ['Fibula',5,3,[[0,2],[1,1],[1,2],[3,1],[3,2],[4,2]],'L',False,'B'],
                        ['Fibula',3,5,[[0,0],[0,1],[0,3],[0,4],[1,1],[1,3]],'U',False,'B'],
                        ['Fibula',5,3,[[0,0],[1,0],[1,1],[3,0],[3,1],[4,0]],'R',False,'B'],
                        ['ThrowingAxe',5,3,[[0,0],[0,1],[1,0],[3,0],[4,0],[4,1]],'H',False,'B'],
                        ['ThrowingAxe',3,5,[[1,0],[1,4],[2,0],[2,1],[2,3],[2,4]],'L',False,'B'],
                        ['ThrowingAxe',5,3,[[0,1],[0,2],[1,2],[3,2],[4,1],[4,2]],'U',False,'B'],
                        ['ThrowingAxe',3,5,[[0,0],[0,1],[0,3],[0,4],[1,0],[1,4]],'R',False,'B']]      
                    
        tile = []
        
        # Only keep tile the player has
        for i in tileTemplate:
            if player.resources[i[0]] > 0:
                tile.append(i)

        possiblePlacements = []
        
        # Loop through each house, spot, and tile
        for i in range(len(player.houses)):
            # If wood slots, append these as possible options
            if player.resources['Wood'] > 0 and player.houses[i].WoodSlots > 0:
                possiblePlacements.append(['Wood','None',0,0,[],'',False,'B',i,0,0])
            if player.resources['Stone'] > 0 and player.houses[i].StoneSlots > 0:
                possiblePlacements.append(['Stone','None',0,0,[],'',False,'B',i,0,0])
                
            # Loop through house length
            for j in range(len(player.houses[i].tiles[0])):
                # Loop through house height
                for k in range(len(player.houses[i].tiles)):                        
                    # Loop through each tile
                    for l in range(len(tile)):   
                        # Check if spot is free or is Bonus
                        if player.houses[i].tiles[k][j] in ['F','P'] or player.houses[i].tiles[k][j][0:5] == 'Bonus' or [0,0] in tile[l][3]:
                            validPlacement = True   
                            # Loop through length of tile
                            for m in range(tile[l][1]):
                                # Loop through height of tile
                                for n in range(tile[l][2]):
                                    # Check if its on the board
                                    if len(player.houses[i].tiles[0]) <= j + m or len(player.houses[i].tiles) <= k + n:
                                        validPlacement = False
                                        continue
                                    
                                    # Reject if spot is not free or Bonus. Include special tile logic
                                    if player.houses[i].tiles[k + n][j + m] not in ['F','P'] and player.houses[i].tiles[k + n][j + m][0:5] != 'Bonus' and [m, n] not in tile[l][3]: 
                                        validPlacement = False
                                        continue
                                    
                                    # Checks for reds/oranges
                                    if tile[l][6] == 'O':
                                        # If at left of tile
                                        if m == 0 and j + m != 0:
                                            if player.houses[i].tiles[k + n][j + m - 1] == 'OO':
                                                validPlacement = False
                                                continue
                                            
                                        # If at right of tile
                                        if m == tile[l][1] - 1 and j + m != len(player.houses[i].tiles[0]) - 1:
                                            if player.houses[i].tiles[k + n][j + m  + 1] == 'OO':
                                                validPlacement = False
                                                continue 
                                            
                                        # If at top of tile
                                        if n == tile[l][2] - 1 and k + n != len(player.houses[i].tiles) - 1:
                                            if player.houses[i].tiles[k + n + 1][j + m ] == 'OO':
                                                validPlacement = False
                                                continue    
                                            
                                        # If at bottom of tile
                                        if n == 0 and k + n != 0:
                                            if player.houses[i].tiles[k + n - 1][j + m ] == 'OO':
                                                validPlacement = False
                                                continue
                                    elif tile[l][6] == 'R':
                                        # If at left of tile
                                        if m == 0 and j != 0:
                                            if player.houses[i].tiles[k + n][j + m  - 1] == 'OR':
                                                validPlacement = False
                                                continue
                                            
                                        # If at right of tile
                                        if m == tile[l][1] - 1 and j != len(player.houses[i].tiles[0]) - 1:
                                            if player.houses[i].tiles[k][j + 1] == 'OR':
                                                validPlacement = False
                                                continue 
                                            
                                        # If at top of tile
                                        if n == tile[l][2] - 1 and k != len(player.houses[i].tiles) - 1:
                                            if player.houses[i].tiles[k + 1][j] == 'OR':
                                                validPlacement = False
                                                continue    
                                            
                                        # If at bottom of tile
                                        if n == 0 and k != 0:
                                            if player.houses[i].tiles[k - 1][j] == 'OR':
                                                validPlacement = False
                                                continue
                                    
                                # Quit loop if already failed    
                                if validPlacement == False:
                                    continue
                                    
                            if validPlacement:
                                possiblePlacements.append(['HousePlacements',tile[l] + [i, j, k]])
                               
        return possiblePlacements
        
        
        
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
            
        # Loop through possible orange and red tiles (each rotation inlcuded) and loop through each spot
        for i in range(len(player.feastTable)):                                
            # First check free feast slots
            if player.feastTable[i][0] == 'F':                    
                # Loop through tiles
                for j in range(len(tile)):
                    validPlacement = True
                    # Check if there is space. If end of table reached or another tile reached, returns False
                    for k in range(tile[j][1]):
                        if i + k + 2 > len(player.feastTable):
                            validPlacement = False
                            continue
                        elif player.feastTable[i + k + 1][0] != 'F':
                            validPlacement = False
                            continue

                    
                    # Next check if either end is same color. First make sure not at either end of table. Don't do to silver (color = B)
                    if tile[j][3] != 'B':
                        if i != 0:
                            if player.feastTable[i - 1][2] == tile[j][3]:
                                validPlacement = False
                                continue
                            
                        if i < len(player.feastTable) - tile[j][1]:
                            if player.feastTable[i + tile[j][1]][2] == tile[j][3]:
                                validPlacement = False
                                continue
                           
                    # Next check if using horizontal rotaion, if that tile has already been used
                    if tile[j][2] == 'H':
                        # Loop through each Feast Table slot
                        for k in range(len(player.feastTable)):
                            if player.feastTable[k][0] == tile[j][0]:
                                validPlacement = False
                                continue
                            
                    if validPlacement:
                        possiblePlacements.append(['FeastPlacements',tile[j] + [i]])
            
        return possiblePlacements
    
                      
class Player():
    def __init__(self, ID, ai):
        self.ID = ID
        self.vikings = 6
        self.endedTurn = False
        self.madeAction = False
        self.whalingBoats = []
        self.knarrs = []
        self.longships = []
        self.penalty = 0
        self.occupations = []
        self.playedOccupations = []
        self.boards = [PlayerBoard()]
        self.houses = []
        self.emigratePoints = 0
        self.ai = AI(ai)
        self.income = 0
      
        self.resources = {'Silver':0, 'Stone':0, 'Wood':0, 'Ore':0, 'Peas':1, 'Mead':1, 'Flax':1, 'Stockfish':0, 'Beans':1, 'Milk':0, 
                          'Grain':0, 'SaltMeat':0, 'Cabbage':0, 'GameMeat':0, 'Fruits':0, 'WhaleMeat':0, 'Oil':0, 'Runestone':0, 'Hide':0, 'Silverware':0, 'Wool':0, 
                          'Chest':0, 'Linen':0, 'Silk':0, 'SkinAndBones':0, 'Spices':0, 'Fur':0, 'Jewelry':0, 'Robe':0, 'TreasureChest':0, 'Clothing':0, 'SilverHoard':0, 
                          'Sheep':0, 'PregnantSheep':0, 'Cattle':0, 'PregnantCattle':0, 'Sword':0, 'Bow':0, 'Spear':0, 'Snare':0, 'GlassBeads':0, 'Helmet':0, 
                          'Cloakpin':0, 'Belt':0, 'Crucifix':0, 'DrinkingHorn':0, 'AmberFigure':0, 'Horseshoe':0 ,'GoldBrooch':0, 'ForgeHammer':0, 'Fibula':0, 'ThrowingAxe':0,
                          'Chalice':0, 'RoundShield':0, 'EnglishCrown':0}

        # FeastTable slot have Free (F) or occupied (name of tile); slot number; rotation horizontal (H), vertical (V), or both (B); and color Red (R), Orange (O), or Blue (B)
        self.feastTable = [['F','B','B']] * 6
   
class Board():
    def __init__(self):
        pass
     
class PlayerBoard(Board):
    def __init__(self):
        self.name = 'PlayerBoard'
        self.income = 0
        self.bonuses = []
        # Tile definitions: X = not placable, F = free, P = free -1 point, B<resource> = bonus resource, I<number> = income added from occupying, O<color> = occupied by color
        # Tiles are arranged by rows from bottom to top 
        self.tiles = [['Income1','F','F','F','F','F','F','P','X','X','X','X','X'],
                      ['F','Income1','F','F','F','BonusStone','F','P','P','P','P','P','X'],
                      ['F','BonusMead','Income0','F','F','F','F','P','P','P','P','P','X'],
                      ['F','F','F','Income1','F','F','F','P','P','P','P','P','X'],
                      ['F','F','BonusWood','F','Income1','F','BonusRunestone','P','P','P','P','P','X'],
                      ['F','F','F','F','F','Income1','F','P','P','P','P','P','X'],
                      ['BonusOre','F','F','F','F','F','Income1','P','P','P','P','P','X'],
                      ['P','P','P','P','P','P','P','Income1','P','P','P','P','X'],
                      ['P','P','P','P','P','P','P','P','Income2','P','P','P','X'],
                      ['P','P','P','P','P','P','P','P','P','Income3','P','P','F'],
                      ['P','P','P','P','P','P','P','P','P','P','Income3','P','F'],
                      ['P','P','P','P','P','P','P','P','P','P','P','Income3','F']]
        
class ExpBoard(Board):
    def __init__(self, expType):
        self.storedSilver = 0
        self.name = expType
        # Tile definitions: X = not placable, F = free, P = free -1 point, O = occupied, B<resource> = bonus resource, I<number> = income added from occupying
        # Tiles are arranged by rows from bottom to top
        if expType == 'Shetland':
            self.income = 0
            self.points = 6
            self.tiles = [['X','F','F','X','X','X','P','P','F'],
                          ['Income1','F','BonusBeans','X','X','X','P','P','P'],
                          ['F','Income1','F','X','F','P','P','P','F','F','F'],
                          ['F','F','Income1','X','P','P','F','BonusCabbage','F'],
                          ['X','X','X','X','P','P','F','F','F'],
                          ['P','P','P','P','F','F','F','Boil','F'],
                          ['P','BonusGameMeat','P','P','F','F','P','P','F'],
                          ['P','P','P','P','F','BonusSilverware','F','X','X'],
                          ['X','X','X','X','F','F','F','X','X']]
        elif expType == 'FaroeIslands':
            self.income = 0
            self.points = 4
            self.tiles = [['X','X','X','X','X','F','F','P'],
                          ['Income1','F','F','F','X','F','BonusHide','P'],
                          ['BonusPeas','Income0','F','F','X','F','F','P'],
                          ['F','F','Income0','X','F','BonusFlax','P','P','X'],
                          ['X','X','X','Income1','F','F','P','X','F'],
                          ['X','F','F','F','Income0','P','P','P','P'],
                          ['X','P','BonusOil','F','F','Income0','X','F','BonusMilk'],
                          ['X','X','P','P','X','X','Income1','F','P'],
                          ['X','X','X','X','X','P','BonusSheep','Income1','P']]
        elif expType == 'Iceland':
            self.income = 1
            self.points = 16
            self.tiles = [['X','X','P','P','F','X','X','X'],
                          ['F','Income1','P','P','F','BonusOreStone','F','X'],
                          ['F','F','Income1','P','F','F','F','P'],
                          ['BonusOil','F','F','Income1','P','P','P','P'],
                          ['F','F','F','F','Income1','P','P','P','P'],
                          ['X','F','BonusStockfish','F','P','Income1','P','P'],
                          ['P','F','X','F','P','P','Income1','P'],
                          ['F','P','X','P','F','P','P','Income1']]
        elif expType == 'Greenland':
            self.income = 0
            self.points = 12
            self.tiles = [['X','X','X','X','F','F','F','X'],
                          ['X','X','F','Income1','F','F','F','X'],
                          ['X','P','P','P','Income1','X','F','BonusStockfish'],
                          ['F','P','F','P','P','Income1','F','F'],
                          ['F','F','F','P','P','P','Income1','X'],
                          ['F','bWhaleMeat','F','Income1','P','P','P','Income1'],
                          ['F','F','F','X','Income1','P','P','P'],
                          ['P','P','P','F','F','Income1','P','P']]
        elif expType == 'BearIsland':
            self.income = 1
            self.points = 12
            self.tiles = [['X','X','X','X','P','P','X','X'],
                          ['X','X','X','F','P','F','F','X'],
                          ['X','F','F','F','F','F','BonusRunestoneStone','X'],
                          ['X','F','F','F','F','F','P','P','X'],
                          ['X','Income2','X','F','F','P','F','BonusStockfish'],
                          ['F','F','Income1','F','BonusGameMeat','F','P','F'],
                          ['P','P','P','Income1','F','P','F','P'],
                          ['X','P','P','P','X','P','P','P'],
                          ['X','X','X','P','P','P','P','X']]
        elif expType == 'BaffinIsland':
            self.income = 0
            self.points = 12
            self.tiles = [['F','F','F','X','P','F','BonusSkinAndBones','F','P'],
                          ['F','Income1','F','F','P','F','F','X','X'],
                          ['X','F','F','F','P','P','X','X','X'],
                          ['F','F','F','Income2','P','P','P','Boil','P'],
                          ['X','F','F','F','Income2','P','P','X','X'],
                          ['X','P','X','P','F','X','X','X','F'],
                          ['X','F','P','F','P','P','F','BonusWhaleMeat','F'],
                          ['P','P','F','P','P','P','F','F','F'],
                          ['P','F','P','P','BonusOre','X','X','X','X']]
        elif expType == 'Labrador':
            self.income = 0
            self.points = 36
            self.tiles = [['X','P','X','P','F','P','BonusStockfish','P','P'],
                          ['P','BonusLinen','P','F','P','F','P','P','P','P'],
                          ['F','P','F','P','BonusChest','P','X','P','X'],
                          ['P','P','P','F','P','P','P','P','P'],
                          ['X','X','P','P','P','P','P','P','P'],
                          ['X','X','X','BonusGameMeat','P','P','F','P','X'],
                          ['X','X','X','P','F','P','X','X','X'],
                          ['X','X','X','P','P','P','X','X','X'],
                          ['X','X','X','P','P','X','X','X','X']]
        elif expType == 'Newfoundland':
            self.income = 0
            self.points = 38
            self.tiles = [['X','X','X','X','X','P','X','P','P'],
                          ['P','P','P','F','P','P','P','P','P'],
                          ['F','P','F','P','P','P','BonusStoneHouse','P','X'],
                          ['P','BonusCloakpin','P','F','P','F','P','P','P'],
                          ['X','F','P','F','P','P','P','X','X'],
                          ['X','P','BonusSkinAndBones','P','X','P','P','X','X'],
                          ['X','X','P','P','X','X','X','X','X'],
                          ['X','X','P','P','P','X','X','X','X']]

            
class House():
    def __init__(self, houseType):
        self.houseType = houseType
        # Tile definitions: X = not placable, F = free, P = free -1 point, O = occupied, B<resource> = bonus resource, I<number> = income added from occupying
        # Tiles are arranged by rows from bottom to top 
        if houseType == 'Shed':
            self.points = 8            
            self.tiles = [['X']]
            self.WoodSlots = 3
            self.StoneSlots = 3
        elif houseType == 'StoneHouse':
            self.points = 10
            self.tiles = [['X','X','P','F','P'],
                          ['X','P','F','F','P'],
                          ['P','F','BonusHide','P','X'],
                          ['X','F','P','X','X']]
            self.WoodSlots = 1
            self.StoneSlots = 1
        elif houseType == 'LongHouse':
            self.points = 17
            self.tiles = [['F','P','F','P','F','P','F','P','F','P','BonusPeas'],
                          ['P','BonusOil','P','X','P','F','P','X','P','F','P'],
                          ['F','P','F','P','F','BonusBeans','F','P','F','P','X']]
            self.WoodSlots = 0
            self.StoneSlots = 0   

class Boat():
    def __init__(self, boatType):        
        if boatType == 'WhalingBoat':
            self.ore = 1
            self.points = 3
            self.maxOre = 2
        elif boatType == 'Knarr':
            self.ore = 0
            self.points = 5
            self.maxOre = 0
        elif boatType == 'Longship':
            self.ore = 0
            self.points = 8
            self.maxOre = 3
        