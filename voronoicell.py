import matplotlib.patches as mpatches
import numpy as np
from matplotlib.path import Path


biomes = {  'water':(0.3,0.4,0.7),
            'land':(238/255.0,207/255.0,161/255.0),
            'mountain':(139/255.0,90/255.0,0),
            'high_mountain':(0.9,0.85,0.85),
            'hill':(0.4,0.4,0.3),
            'lake':(0.3,0.4,0.95),
            'river':(0.3,0.5,0.6),
            'forest':(110/255.0,139/255.0,61/255.0),
            'arctic':(0.95,0.95,0.95),
            'desert':(0.6,0.9,0.9),
            'select':(0.5,0.9,0.9)}

class VoronoiCell():
    def __init__(self):
        self.id=-1
        self.neighbors = []
        self.path = None
        self.vertices = np.array((np.inf,np.inf))
        self.center = np.array((np.inf,np.inf))
        self.hull_point=False
        self.color = (0.5,0.7,0.7)#np.random.rand(3)
        self.elevation = 0
        self.name = None
        self.value = 0

    #find the VoronoiCell containg (x,y)
    def contains(self,pos):
        self.path = Path(self.vertices)
        return self.path.contains_point(pos)
    
    def draw(self):
        patch = mpatches.Polygon(self.vertices,ec='none',facecolor = self.color)
        patch.set_picker(True)
        return patch
    
    def increase_elevation(self, increment):    
        if self.name == 'water':
            self.name = 'land'
            self.elevation+=increment
        if self.name == 'lake':
            self.name = 'land'
            self.elevation+=increment
        elif self.name == 'land':
            self.name = 'mountain'
            self.elevation+=increment
        self.color = biomes[self.name]
        
    def __lt__(self, other):
         return self.center[1] < other.center[1]
                 
            