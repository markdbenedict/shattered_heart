import matplotlib.patches as mpatches
import numpy as np
from matplotlib.path import Path

class VoronoiCell():
    def __init__(self):
        self.id=-1
        self.neighbors = []
        self.path = None
        self.vertices = np.array((np.inf,np.inf))
        self.center = np.array((np.inf,np.inf))
        self.hull_point=False
        self.color = (128,200,200)#np.random.rand(3)

    #find the VoronoiCell containg (x,y)
    def contains(self,pos):
        self.path = Path(self.vertices)
        return self.path.contains_point(pos)
    
    def draw(self):
        patch = mpatches.Polygon(self.vertices,ec='none',facecolor = self.color)
        patch.set_picker(True)
        return patch
        
    
                 
            