from Odin import *
import random

class AI():
    def __init__(self, aiType):
        self.aiType = aiType
    
    def takeAction(self, player, validActions):
         if self.aiType == 'Random':
             return validActions[random.randint(0, len(validActions) - 1)]
         elif self.aiType == 'Human':
             print('What action will player ' + str(player.ID + 1) + ' take:')
             return input()
         

