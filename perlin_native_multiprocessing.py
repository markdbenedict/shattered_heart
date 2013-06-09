import random
import math
import numpy as np
from IPython.parallel import Client

perm = range(256)
random.shuffle(perm)
perm += perm
dirs = [(math.cos(a * 2.0 * math.pi / 256),
         math.sin(a * 2.0 * math.pi / 256))
         for a in range(256)]

def surflet(gridX, gridY,x,y,per):
        distX, distY = abs(x-gridX), abs(y-gridY)
        polyX = 1 - 6*distX**5 + 15*distX**4 - 10*distX**3
        polyY = 1 - 6*distY**5 + 15*distY**4 - 10*distY**3
        hashed = perm[perm[int(gridX)%per] + int(gridY)%per]
        grad = (x-gridX)*dirs[hashed][0] + (y-gridY)*dirs[hashed][1]
        return polyX * polyY * grad
    

def noise(x, y, per):
    intX, intY = int(x), int(y)
    return (surflet(intX+0, intY+0,x,y,per) + surflet(intX+1, intY+0,x,y,per) +
            surflet(intX+0, intY+1,x,y,per) + surflet(intX+1, intY+1,x,y,per))


def fBm(i):
    
    freq, octs= 1/32.0, 2
    row = []
    #size=64
    for j in range(size):
        val = 0
        per = int(size*freq)
        x=i%size *freq
        y=i/size *freq
        for o in range(octs):
            val += 0.5**o * noise(x*2**o, y*2**o, per*2**o)
        row.append(val)
    return row

def test_perlin(size = 32,display=True):
    
    data =[]
    c = Client()
    dview=c[:]
    dview.push({'size':size,'noise':noise,'surflet':surflet,'perm':perm,'dirs':dirs})
    data = dview.map_sync(fBm,range(size))
    data = np.array(data)
    
    if display:
        from matplotlib import pyplot as plt
        plt.imshow(data,cmap='gray')
        plt.colorbar()
        plt.show()

if __name__ == '__main__':
    test_perlin(size=256,display=True)