from random import*
import matplotlib as plt
import numpy as np

class Die(object):
    def __init__(self, sides = 6):
        self.sides = sides
        
    def roll(self):
        return randint(1, self.sides)
    
    def drawDie(self):
        pass
    
#Tests the die class.
d = Die(12);
d.roll()
print d.roll()

#Graph in progress.
#plt.plot([d.roll])
#plt.show()
    