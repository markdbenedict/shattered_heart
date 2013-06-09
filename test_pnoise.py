import perlin

perlin.init()

import numpy as np
def test_perlin(size = 128,display=True,alpha=2,beta=2,n=2):
    data = np.zeros((size,size))
    denom = float(size)
    for x in range(size):
        for y in range(size):
            data[x,y]=perlin.PerlinNoise2D(x/denom,y/denom,alpha,beta,n)
    if display:
        from matplotlib import pyplot as plt
        plt.imshow(data,cmap='gray')
        plt.colorbar()
        plt.show()
