import matplotlib.patches as mpatches
import numpy as np
import matplotlib.nxutils as nx

biomes = {  'water':(0.3,0.4,0.7),
            'land':(238/255.0,207/255.0,161/255.0),
            'mountain':(139/255.0,90/255.0,0),
            'high_mountain':(0.9,0.9,0.9),
            'hill':(0.4,0.4,0.3),
            'lake':(0.3,0.4,0.95),
            'river':(0.3,0.5,0.6),
            'forest':(110/255.0,139/255.0,61/255.0),
            'arctic':(0.9,0.9,0.9),
            'desert':(0.6,0.9,0.9)}

class VoronoiCell():
    def __init__(self):
        self.id=-1
        self.neighbors = []
        self.vertices = np.array((np.inf,np.inf))
        self.center = np.array((np.inf,np.inf))
        self.hull_point=False
        self.color = (0.5,0.7,0.7)#np.random.rand(3)
        self.elevation = 0
        self.name = None

    def neighbors(self):
        pass

    #find the VoronoiCell containg (x,y)
    def contains(self,x,y):
        return nx.pnpoly(x,y,self.vertices)
    
    def draw(self):
        patch = mpatches.Polygon(self.vertices,facecolor = self.color)
        patch.set_picker(True)
        #print self.color
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
        

                 
            