import random
import itertools

class Game():
    def __init__(self, nHumanPlayers = 1, nBotPlayers = 0, occupationSet = ['A']):
        # Available exploration boards and stored silver
        self.availableExplorationBoards = {'Shetland':0,'FaroeIslands':0,'Iceland':0,'Greenland':0} 
        
        # Available Sepcial Tiles and their silver cost
        self.availableSpecialTiles = {'GlassBeads':0,'Helmet':1,'Cloakpin':1,'Belt':2,'Crucifix':2,'DrinkingHorn':2,'AmberFigure':2,
                                      'Horesshoe':2,'GoldBrooch':3,'ForgeHammer':4,'Fibula':4,'ThrowingAxe':4,'Chalice':5,'RoundShield':6,'EnglishCrown':9999}
        
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
        self.availableActions = ['BuildShed','BuildWhalingBoat','HuntingGameOne','HuntStockfish','BuyStockfish','BuySaltMeat','WeeklyMarketOne','ProductsOne','CraftLinen','CraftRunestone',
                                 'MountainTwo','MountainOneUpgradeOne','UpgradeTwo','UpgradeGreensOne','Raiding','ExplorationOne','DrawOccupation','PlayOccupationsOne','BuildStoneHouse',
                                 'BuildKnarr','HuntingGameTwo','LaySnare','BuySheep','BuyCattle','WeeklyMarketTwo','ProductsTwo','CraftClothing','CraftChest','WoodPerPlayer','MountainThreeUpgradeOne',
                                 'UpgradeThree','UpgradeGreensTwo','PillagingOne','ExplorationTwo','EmigrateOne','PlayOccupationsTwo','BuildLongHouse','BuildLongship','WhalingOne','BuySheepOrCattle',
                                 'WeeklyMarketThree','ProductsThree','CraftSpecial','CraftChestRunestone','MountainThreeTwo','UpgradeThreeWeapons','UpgradeFour','BuySpecials','PillagingTwo',
                                 'ExplorationThree','EmigrateTwo','PlayOccupationsThree','BuildHouseBoat','WhalingTwo','BuySheepAndCattle','WeeklyMarketFour','CraftingRoberSilverware',
                                 'MountainFourUpgradeTwoTwice','MountainOrUpgrade','Plundering','EmigrateThree']
        
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
         
        # List all possible single upgrades
        self.availableSingleUpgrades = {'Peas':['Mead'],
                                        'Flax':['Stockfish'],
                                        'Beans':['Milk'],
                                        'Grain':['SaltMeat'],
                                        'Cabbage':['GameMeat'],
                                        'Fruits':['WhaleMeat'],
                                        'Mead':['Oil'],
                                        'Stockfish':['Hide'],
                                        'Milk':['Wool'],
                                        'SaltMeat':['Linen'],
                                        'GameMeat':['SkinAndBones'],
                                        'Sheep':['Fur'],
                                        'PregnantSheep':['Fur'],
                                        'WhaleMeat':['Robe'],
                                        'Cattle':['Clothing'],
                                        'PregnantCattle':['Clothing'],
                                        'Oil':['Runestone'],
                                        'Hide':['Silverware'],
                                        'Wool':['Chest'],
                                        'Linen':['Silk'],
                                        'SkinAndBones':['Spices'],
                                        'Fur':['Jewelry'],
                                        'Robe':['TreasureChest'],
                                        'Clothing':['SilverHoard']}
         
        # List all possible double upgrades
        self.availableDoubleUpgrades = {'Peas':['Oil'],
                                  'Flax':['Hide'],
                                  'Beans':['Wool'],
                                  'Grain':['Linen'],
                                  'Cabbage':['SkinAndBones'],
                                  'Fruits':['Robe'],
                                  'Mead':['Runestone'],
                                  'Stockfish':['Silverware'],
                                  'Milk':['Chest'],
                                  'SaltMeat':['Silk'],
                                  'GameMeat':['Spices'],
                                  'Sheep':['Jewelry'],
                                  'PregnantSheep':['Jewelry'],
                                  'WhaleMeat':['TreasureChest'],
                                  'Cattle':['SilverHoard'],
                                  'PregnantCattle':['SilverHoard']}  
        
        # List all possible green upgrades
        self.availableGreenUpgrades = {'Oil':['Runestone'],
                                       'Hide':['Silverware'],
                                       'Wool':['Chest'],
                                       'Linen':['Silk'],
                                       'SkinAndBones':['Spices'],
                                       'Fur':['Jewelry'],
                                       'Robe':['TreasureChest'],
                                       'Clothing':['SilverHoard']}
        
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
            
    def placeHouseTile(self, player, ID, color, coords):
        for i in coords:
            player.houses[ID].tiles[i[1]][i[0]] = 'O' + color
    
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
            
        # Option to pass the turn to next player. Otherwise can play action
        if player.madeAction:
            validActions.append(['PassTurn',['PassTurn']])
        else:        
            # One viking actions
            if player.vikings >= 1:
                # Build Shed
                if player.resources['Wood'] >= 2 and 'Shed' in self.availableHouses and 'BuildShed' in self.availableActions:
                    validActions.append('BuildShed',['BuildShed'])
                
                # Build Whaling Boat
                if player.resources['Wood'] >= 1 and player.whalingBoats < 3 and 'BuildWhalingBoat' in self.availableActions:
                    validActions.append('BuildWhalingBoat',['BuildWhalingBoat'])
                    
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
                        validActions.append(['UpgradeTwo',[i[0], 'None']])
                
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
                        validActions.append('ExplorationOne',['Shetland'])
                    if 'FaroeIslands' in self.availableExplorationBoards:
                        validActions.append('ExplorationOne',['FaroeIslands'])
                        
                # Take Occupation
                if 'TakeOccupation' in self.availableActions:
                    validActions.append(['TakeOccupation',['TakeOccupation']])
                
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
                        validActions.append(['UpgradeThree',[i[0], i[1], 'None']])
                    # Create list of one combinations
                    for i in set(list(itertools.combinations(upgradeableSingles, 1))):
                        validActions.append(['UpgradeThree',[i[0], 'None', 'None']])
                     
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
                        validActions.append(['PlayOccupationsTwo',[i[0], 'None']])
            
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
                if player.resources['Stone'] >= 2 and player.resources['Stone'] >= 2 and 'CraftChestRunestones' in self.availableActions:
                    validActions.append(['CraftChestRunestones',['CraftChestRunestones']])
                if 'CraftChestRunestones' in self.availableActions:
                    validActions.append(['CraftChestRunestones',['None']])
                    
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
                        validActions.append(['UpgradeThreeWeapons',[i[0], i[1], 'None']])
                    # Create list of one combinations
                    for i in set(list(itertools.combinations(upgradeableSingles, 1))):
                        validActions.append(['UpgradeThreeWeapons',[i[0], 'None', 'None']])
                    # Option to upgrade none
                    validActions.append(['UpgradeThreeWeapons',['None', 'None', 'None']])
                    
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
                        validActions.append(['UpgradeFour',[i[0], i[1], i[2], 'None']])
                    # Create list of two combinations
                    for i in set(list(itertools.combinations(upgradeableSingles, 2))):
                        validActions.append(['UpgradeFour',[i[0], i[1], 'None', 'None']])
                    # Create list of one combinations
                    for i in set(list(itertools.combinations(upgradeableSingles, 1))):
                        validActions.append(['UpgradeFour',[i[0], 'None', 'None', 'None']])
                    # Option to upgrade none
                    validActions.append(['UpgradeFour',['None', 'None', 'None', 'None']])
                    
                # Buy special tiles
                if len(player.knarrs) >= 1 and 'BuySpecials' in self.availableActions:
                    for i in self.availableSpecialTiles:
                        for j in self.availableSpecialTiles:
                            # Buy two specials
                            if i != j and player.resources['Silver'] >= self.availableSpecialTiles[i] + self.availableSpecialTiles[j] :
                                validActions.append(['BuySpecials',[i,j]])
                        # Buy one special
                        if player.resources['Silver'] >= self.availableSpecialTiles[i]:
                            validActions.append(['BuySpecials',[i,'None']])
                if 'BuySpecials' in self.availableActions:
                    validActions.append(['BuySpecials',['None','None']])
                    
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
                        validActions.append(['PlayOccupationsThree',[i[0],i[1],i[2],'None']])
                    # Playing two occupations
                    for i in list(itertools.combinations(player.occupations + ['Drawn'], 2)):
                        validActions.append(['PlayOccupationsThree',[i[0],i[1],'None','None']])
                    # Playing one occupation
                    for i in list(itertools.combinations(player.occupations + ['Drawn'], 1)):
                        validActions.append(['PlayOccupationsThree',[i[0],'None','None','None']])
                    validActions.append(['PlayOccupationsThree',['None','None','None','None']])
                    
            # Four viking actions. These will also have an option to just play an occupation if they have one
            if player.vikings >= 4:
                # Build house and boat
                if player.resources['Stone'] >= 2 and player.resources['Wood'] >= 2 and 'BuildHouseBoat' in self.availableActions:
                    for i in player.occupations + 'None':
                        if 'StoneHouse' in self.availableHouses and len(player.longships) + len(player.knarrs) < 4:
                            validActions.append(['BuildHouseBoat',['StoneHouseLongship',i]])
                        if 'LongHouse' in self.availableHouses and len(player.longships) + len(player.knarrs) < 4:
                            validActions.append(['BuildHouseBoat',['LongHouseKnarr',i]])
                        if 'StoneHouse' in self.availableHouses:
                            validActions.append(['BuildHouseBoat',['StoneHouse',i]])
                        if 'LongHouse' in self.availableHouses:
                            validActions.append(['BuildHouseBoat',['LongHouse',i]])
                        if len(player.longships) + len(player.knarrs) < 4:
                            validActions.append(['BuildHouseBoat',['Knarr',i]])
                            validActions.append(['BuildHouseBoat',['Longship',i]])
                if len(player.occupations) >= 1 and 'BuildHouseBoat' in self.availableActions:
                    for i in player.occupations:
                        validActions.append(['BuildHouseBoat',['None',i]])
                        
                # Whaling two
                if len(player.whalingBoats) >= 1 and 'WhalingTwo' in self.availableActions:
                    for i in player.occupations + ['None']:
                        validActions.append(['WhalingTwo',['WhalingTwo',i]])
                if len(player.occupations) >= 1 and 'WhalingTwo' in self.availableActions:
                    for i in player.occupations:
                        validActions.append(['WhalingTwo',['None',i]])
                        
                # Buy sheep and cattle            
                if player.resources['Silver'] >= 3 and 'BuySheepAndCattle' in self.availableActions:
                    for i in player.occupations + ['None']:
                        validActions.append(['BuySheepAndCattle',['BuySheepAndCattle',i]])
                if len(player.occupations) >= 1 and 'BuySheepAndCattle' in self.availableActions:
                    for i in player.occupations:
                        validActions.append(['BuySheepAndCattle',['None',i]])
                        
                # Weekly market four
                if 'WeeklyMarketFour' in self.availableActions:
                    for i in player.occupations + ['None']:
                        validActions.append(['WeeklyMarketFour',['WeeklyMarketFour',i]])
                if len(player.occupations) >= 1 and 'WeeklyMarketFour' in self.availableActions:
                    for i in player.occupations:
                        validActions.append(['WeeklyMarketFour',['None',i]])
                        
                # Crafting four
                if 'CraftingFour' in self.availableActions:
                    for i in player.occupations + ['None']:
                        validActions.append(['CraftingFour',['CraftingFour',i]])
                if len(player.occupations) >= 1 and 'CraftingFour' in self.availableActions:
                    for i in player.occupations:
                        validActions.append(['CraftingFour',['None',i]])
                        
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
                                    validActions.append(['MountainFourUpgradeTwoTwice',[k, 4] + j + [i]])
                                if len(self.mountains[k]) >= 3:
                                    validActions.append(['MountainFourUpgradeTwoTwice',[k, 3] + j + [i]])
                                if len(self.mountains[k]) >= 2:
                                    validActions.append(['MountainFourUpgradeTwoTwice',[k, 2] + j + [i]])
                                if len(self.mountains[k]) >= 1:
                                    validActions.append(['MountainFourUpgradeTwoTwice',[k, 1] + j + [i]])                              
                            validActions.append(['MountainFourUpgradeTwoTwice',[0, 0] + j + [i]])  
                validActions.remove(['MountainFourUpgradeTwoTwice', [0, 0, 'None', 'None', 'None']])               
            
            
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
                            validActions.append(['MountainOrUpgrade',['Upgrade',i] + j])
                            
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
                                validActions.append(['MountainOrUpgrade',['Mountain',i,m[0][0],m[0][1],m[1][0],m[1][1],m[2][0],m[2][1],m[3][0],m[3][1]]])
                            if len(m) == 3:
                                validActions.append(['MountainOrUpgrade',['Mountain',i,m[0][0],m[0][1],m[1][0],m[1][1],m[2][0],m[2][1],0,0]])
                            if len(m) == 2:
                                validActions.append(['MountainOrUpgrade',['Mountain',i,m[0][0],m[0][1],m[1][0],m[1][1],0,0,0,0]])
                            if len(m) == 1:
                                validActions.append(['MountainOrUpgrade',['Mountain',i,m[0][0],m[0][1],0,0,0,0,0,0]])
                if len(player.occupations) >= 1 and 'MountainOrUpgrade' in self.availableActions:
                    for i in player.occupations:
                        validActions.append(['MountainOrUpgrade',['None',i]])
                        
                # Plundering
                if len(player.longships) >= 2 and len(player.occupations) >= 1 and 'Plundering' in self.availableActions:
                    for i in player.occupations:
                        validActions.append(['Plundering',['Plundering',i]]) 
                if len(player.occupations) >= 1 and 'Plundering' in self.availableActions:
                    for i in player.occupations:
                        validActions.append(['Plundering',['None',i]])           
                        
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
        for i in [player.playerBoard] + player.expBoards:               
            # Loop through board length
            for j in range(len(i.tiles[0])):
                # Loop through board height
                for k in range(len(i.tiles)):                        
                    # Loop through each tile
                    for l in range(len(tile)):   
                        # Check if spot is free, Bonus, or Income
                        if i.tiles[k][j] in ['F','P'] or i.tiles[k][j][0:5] == 'Bonus' or i.tiles[k][j][0:6] == 'Income' or [0,0] in tile[l][3]:
                            validPlacement = True   
                            # Loop through length of tile
                            for m in range(tile[l][1]):
                                # Loop through height of tile
                                for n in range(tile[l][2]):
                                    # Check if its on the board
                                    if len(i.tiles[0]) <= j + m or len(i.tiles) <= k + n:
                                        validPlacement = False
                                        continue
                                    
                                    # Reject if spot is not free or Bonus. Include special tile logic
                                    if i.tiles[k + n][j + m] not in ['F','P'] and i.tiles[k + n][j + m][0:5] != 'Bonus' and i.tiles[k + n][j + m][0:6] != 'Income' and [m, n] not in tile[l][3]: 
                                        validPlacement = False
                                        continue
                                    
                                    # Checks for greens
                                    if tile[l][6] == 'G':
                                        # If at left of tile
                                        if m == 0 and j + m != 0:
                                            if i.tiles[k + n][j + m - 1] == 'OG':
                                                validPlacement = False
                                                continue
                                            
                                        # If at right of tile
                                        if m == tile[l][1] - 1 and j + m != len(i.tiles[0]) - 1:
                                            if i.tiles[k + n][j + m  + 1] == 'OG':
                                                validPlacement = False
                                                continue 
                                            
                                        # If at top of tile
                                        if n == tile[l][2] - 1 and k + n != len(i.tiles) - 1:
                                            if i.tiles[k + n + 1][j + m ] == 'OG':
                                                validPlacement = False
                                                continue    
                                            
                                        # If at bottom of tile
                                        if n == 0 and k + n != 0:
                                            if i.tiles[k + n - 1][j + m ] == 'OG':
                                                validPlacement = False
                                                continue
                                                                        
                                    # Check for valid income by checking if every spot below and to left of income is filled or being filled
                                    if i.tiles[k + n][j + m][0:6] == 'Income':
                                        # Loop through left of income
                                        for o in range(j + m + 1):
                                            # Loop through bottom of income
                                            for p in range(k + n + 1):
                                                # Check if tile is not free or if not occupied                                                                                                
                                                if (i.tiles[p][o] in ['F','P'] or i.tiles[p][o][0:6] == 'Income') and not (o < j + tile[l][1] and o >= j and p < k + tile[l][2] and p >= k and [o - j, p - k] not in tile[l][3]):
                                                    validPlacement = False
                                                    break       
                                            # Quit loop if already failed    
                                            if validPlacement == False:
                                                break
                                                
                                # Quit loop if already failed    
                                if validPlacement == False:
                                    break
                                    
                            if validPlacement:
                                possiblePlacements.append(['BoardPlacements',[tile[l][0], i.name, j, k, tile[l][4], tile[l][5], tile[l][6]]])
                               
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
        for i in player.houses:
            # If wood slots, append these as possible options
            if player.resources['Wood'] > 0 and i.WoodSlots > 0:
                possiblePlacements.append(['Wood',i.houseType,i.ID,0,0,'H',False,'B'])
            if player.resources['Stone'] > 0 and i.StoneSlots > 0:
                possiblePlacements.append(['Stone',i.houseType,i.ID,0,0,'H',False,'B'])
                
            # Loop through house length
            for j in range(len(i.tiles[0])):
                # Loop through house height
                for k in range(len(i.tiles)):                        
                    # Loop through each tile
                    for l in range(len(tile)):   
                        # Check if spot is free or is Bonus
                        if i.tiles[k][j] in ['F','P'] or i.tiles[k][j][0:5] == 'Bonus' or [0,0] in tile[l][3]:
                            validPlacement = True   
                            # Loop through length of tile
                            for m in range(tile[l][1]):
                                # Loop through height of tile
                                for n in range(tile[l][2]):
                                    # Check if its on the board
                                    if len(i.tiles[0]) <= j + m or len(i.tiles) <= k + n:
                                        validPlacement = False
                                        continue
                                    
                                    # Reject if spot is not free or Bonus. Include special tile logic
                                    if i.tiles[k + n][j + m] not in ['F','P'] and i.tiles[k + n][j + m][0:5] != 'Bonus' and [m, n] not in tile[l][3]: 
                                        validPlacement = False
                                        continue
                                    
                                    # Checks for reds/oranges
                                    if tile[l][6] == 'O':
                                        # If at left of tile
                                        if m == 0 and j + m != 0:
                                            if i.tiles[k + n][j + m - 1] == 'OO':
                                                validPlacement = False
                                                continue
                                            
                                        # If at right of tile
                                        if m == tile[l][1] - 1 and j + m != len(i.tiles[0]) - 1:
                                            if i.tiles[k + n][j + m  + 1] == 'OO':
                                                validPlacement = False
                                                continue 
                                            
                                        # If at top of tile
                                        if n == tile[l][2] - 1 and k + n != len(i.tiles) - 1:
                                            if i.tiles[k + n + 1][j + m ] == 'OO':
                                                validPlacement = False
                                                continue    
                                            
                                        # If at bottom of tile
                                        if n == 0 and k + n != 0:
                                            if i.tiles[k + n - 1][j + m ] == 'OO':
                                                validPlacement = False
                                                continue
                                    elif tile[l][6] == 'R':
                                        # If at left of tile
                                        if m == 0 and j != 0:
                                            if i.tiles[k + n][j + m  - 1] == 'OR':
                                                validPlacement = False
                                                continue
                                            
                                        # If at right of tile
                                        if m == tile[l][1] - 1 and j != len(i.tiles[0]) - 1:
                                            if i.tiles[k][j + 1] == 'OR':
                                                validPlacement = False
                                                continue 
                                            
                                        # If at top of tile
                                        if n == tile[l][2] - 1 and k != len(i.tiles) - 1:
                                            if i.tiles[k + 1][j] == 'OR':
                                                validPlacement = False
                                                continue    
                                            
                                        # If at bottom of tile
                                        if n == 0 and k != 0:
                                            if i.tiles[k - 1][j] == 'OR':
                                                validPlacement = False
                                                continue
                                    
                                # Quit loop if already failed    
                                if validPlacement == False:
                                    continue
                                    
                            if validPlacement:
                                possiblePlacements.append(['HousePlacements',[tile[l][0], i.ID, j, k, tile[l][4], tile[l][5], tile[l][6]]])
                               
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
                            
                    if validPlacement:
                        possiblePlacements.append(['FeastPlacements',[tile[j][0], player.feastTable[i][1], tile[j][2]]])
            
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
        self.emigratePoints = 0
      
        self.resources = {'Silver':0, 'Stone':0, 'Wood':0, 'Ore':0, 'Peas':1, 'Mead':1, 'Flax':1, 'Stockfish':0, 'Beans':1, 'Milk':0, 
                          'Grain':0, 'SaltMeat':0, 'Cabbage':0, 'GameMeat':0, 'Fruits':0, 'WhaleMeat':0, 'Oil':0, 'Runestone':0, 'Hide':0, 'Silverware':0, 'Wool':0, 
                          'Chest':0, 'Linen':0, 'Silk':0, 'SkinAndBones':0, 'Spices':0, 'Fur':0, 'Jewelry':0, 'Robe':0, 'TreasureChest':0, 'Clothing':0, 'SilverHoard':0, 
                          'Sheep':0, 'PregnantSheep':0, 'Cattle':0, 'PregnantCattle':0, 'Sword':0, 'Bow':0, 'Spear':0, 'Snare':0, 'GlassBeads':0, 'Helmet':0, 
                          'Cloakpin':0, 'Belt':0, 'Crucifix':0, 'DrinkingHorn':0, 'AmberFigure':0, 'Horseshoe':0 ,'GoldBrooch':0, 'ForgeHammer':0, 'Fibula':0, 'ThrowingAxe':0,
                          'Chalice':0, 'RoundShield':0, 'EnglishCrown':0}

        # FeastTable slot have Free (F) or occupied (name of tile); slot number; rotation horizontal (H), vertical (V), or both (B); and color Red (R), Orange (O), or Blue (B)
        self.feastTable = [['F',1,'B','B'],
                           ['F',2,'B','B'],
                           ['F',3,'B','B'],
                           ['F',4,'B','B'],
                           ['F',5,'B','B'],
                           ['F',6,'B','B']]
        
class PlayerBoard():
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
                      ['F','F','BonusWood','F','Income1','F','BonusRuneStone','P','P','P','P','P','X'],
                      ['F','F','F','F','F','Income1','F','P','P','P','P','P','X'],
                      ['BonusOre','F','F','F','F','F','Income1','P','P','P','P','P','X'],
                      ['P','P','P','P','P','P','P','Income1','P','P','P','P','X'],
                      ['P','P','P','P','P','P','P','P','Income2','P','P','P','X'],
                      ['P','P','P','P','P','P','P','P','P','Income3','P','P','F'],
                      ['P','P','P','P','P','P','P','P','P','P','Income3','P','F'],
                      ['P','P','P','P','P','P','P','P','P','P','P','Income3','F']]
        
class ExpBoard():
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
                          ['X','F','F','F','F','F','BRuneStoneStone','X'],
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
    def __init__(self, ID, houseType):
        self.houseType = houseType
        self.ID = ID   
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
            self.ponts = 17
            self.tiles = [['F','P','F','P','F','P','F','P','F','P','BonusPeas'],
                          ['P','BonusOil','P','X','P','F','P','X','P','F','P'],
                          ['F','P','F','P','F','BonusBeans','F','P','F','P','X']]
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
        