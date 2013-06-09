import random
import math
from PIL import Image
import numpy as np

perm = range(256)
random.shuffle(perm)
perm += perm
dirs = [(math.cos(a * 2.0 * math.pi / 256),
         math.sin(a * 2.0 * math.pi / 256))
         for a in range(256)]

def noise(x, y, per):
    def surflet(gridX, gridY):
        distX, distY = abs(x-gridX), abs(y-gridY)
        polyX = 1 - 6*distX**5 + 15*distX**4 - 10*distX**3
        polyY = 1 - 6*distY**5 + 15*distY**4 - 10*distY**3
        hashed = perm[perm[int(gridX)%per] + int(gridY)%per]
        grad = (x-gridX)*dirs[hashed][0] + (y-gridY)*dirs[hashed][1]
        return polyX * polyY * grad
    intX, intY = int(x), int(y)
    return (surflet(intX+0, intY+0) + surflet(intX+1, intY+0) +
            surflet(intX+0, intY+1) + surflet(intX+1, intY+1))

def fBm(x, y, per, octs):
    val = 0
    for o in range(octs):
        no = noise(x*2**o, y*2**o, per*2**o)
        val += 0.5**o * no
    return val

def test_perlin(size = 128,display=True):
    freq, octs= 1/32.0, 2
    data = np.zeros((size,size))
    for y in range(size):
        for x in range(size):
            data[x,y]=fBm(x*freq, y*freq, int(size*freq), octs)
    
    if display:
        from matplotlib import pyplot as plt
        plt.imshow(data,cmap='gray')
        plt.colorbar()
        plt.show()

if __name__ == '__main__':
    test_perlin(size=256,display=True)