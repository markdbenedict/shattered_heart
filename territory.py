import matplotlib.patches as mpatches
from voronoicell import VoronoiCell
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

class Territory(VoronoiCell):
    def __init__(self):
        self.elevation = 0
        self.name = None
        self.owner = -1
        self.owner_color = (0,0,0)
        self.value=0 #number of armies

    #find the VoronoiCell containg (x,y)
    def contains(self,pos):
        self.path = Path(self.vertices)
        return self.path.contains_point(pos)
    
    def draw(self):
        if self.owner != -1:
            color = self.owner_color
        else:
            color = self.color
        patch = mpatches.Polygon(self.vertices,ec='none',facecolor = color)
        patch.set_picker(True)
        return patch
    
    #attempts to change the owner.
    def changeOwner(self, newOwnerNum):
        changed = False
        if self.owner == newOwnerNum or self.owner == -1:
            self.owner = newOwnerNum
            changed = True
        return changed
    
    
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
                 
            