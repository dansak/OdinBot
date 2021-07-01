from Odin import *


game = Game(nPlayers = 1, occupationSet = ['A'])

print('\nMountains:')
print(game.mountains)
print('\nAvailable Mountains:')
print(game.availableMountains)


print('\nP1 Silver:')
print(game.players[0].resources['Silver'])
print('\nP1 Peas:')
print(game.players[0].resources['Peas'])

game.buildShed(game.players[0])

print('\nShed Points:')
print(game.players[0].houses[0].points)

print('\nAvailable Exploration Boards:')
print(game.availableExplorationBoards)

game.round = 3
game.explorationPhase()

print('\nAvailable Exploration Boards:')
print(game.availableExplorationBoards)

game.round = 4
game.explorationPhase()

print('\nAvailable Exploration Boards:')
print(game.availableExplorationBoards)

game.round = 5
game.explorationPhase()

print('\nAvailable Exploration Boards:')
print(game.availableExplorationBoards)

game.round = 6
game.explorationPhase()

print('\nAvailable Exploration Boards:')
print(game.availableExplorationBoards)