from random import*
import matplotlib.pyplot as plt
import numpy as np

class Die(object):
    def __init__(self, sides = 6):
        self.sides = sides
        
    def roll(self):
        return randint(1, self.sides)
    
    def drawDie(self):
        pass

if __name__ == "__main__":      
    #Tests the die class.
    d = Die(12);
    sample=[ ]
    for i in range(10000):
        sample.append(d.roll())
    
    #Graph in progress.
    plt.hist(sample,bins=12)
    plt.show()
    