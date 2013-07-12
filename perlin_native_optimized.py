import random
import math
from PIL import Image
import numpy as np


    
def noise(freq,octs,size):
    #setup randomized hash table of directions
    perm = np.arange(size)
    np.random.shuffle(perm)
    perm = np.concatenate([perm,perm])
    dirs = [(math.cos(a * 2.0 * math.pi / size),
             math.sin(a * 2.0 * math.pi / size))
             for a in range(size)]
    dirs = np.array(dirs)

    valFBM = np.zeros((size,size))
    for o in range(octs):
        per = int(size*freq*2**o)
        val = np.zeros((size,size))
        X = np.arange(size)* 2**o
        X = X.reshape(size,1)
        Y = np.arange(size) * 2**o
        Y = Y.reshape(1,size)
        floatX = X*freq
        floatY = Y*freq
        intX = floatX.astype(np.int32)
        intY = floatY.astype(np.int32)
        for i in range(2):
            for j in range(2):
                gridX,gridY = intX+i, intY+j
                distX, distY = abs(floatX-gridX), abs(floatY-gridY) #distX, distY must never get larger than 1
                
                polyX = 1 - 6*distX**5 + 15*distX**4 - 10*distX**3
                polyY = 1 - 6*distY**5 + 15*distY**4 - 10*distY**3
                
                hashed = perm[perm[gridX%per] + gridY%per]
                grad = (floatX-gridX)*dirs[hashed,0] + (floatY-gridY)*dirs[hashed,1]
                val+=polyX * polyY * grad 
        
        valFBM += 0.5**o * val
        
    return valFBM


def test_perlin(size = 256,display=True,freq=1/32.0, octs= 2):
    data=noise(freq, octs,size)
    
    if display:
        from matplotlib import pyplot as plt
        plt.imshow(data,cmap='gray')
        plt.colorbar()
        plt.show()

if __name__ == '__main__':
    test_perlin(size=256,display=True)
