import os

os.chdir('C:/Users/Dan Desktop/Desktop/OdinBot')

from Odin import *
from AI import *

scores = []
for i in range(100000):
    game = Game(nHumanPlayers = 0, nBotPlayers = 2, ai = ['Random','Random'], occupationSet = ['A','B','C'])
    scores.append(game.play())

print(scores)
#%%