from Odin import *
from AI import *

scores = []
for i in range(10):
    game = Game(nHumanPlayers = 0, nBotPlayers = 1, ai = ['Random'], occupationSet = ['A'])
    scores.append(game.play())

print(scores)
#%%