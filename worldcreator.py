from math import pi,sin,cos

from direct.showbase.ShowBase import ShowBase
from direct.task import Task

from voronoigraph import VoronoiGraph
import matplotlib.pyplot as plt
import numpy as np
import random

import scipy.stats as stats

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

class WorldCreator():#ShowBase):
    def __init__(self):
        #ShowBase.__init__(self)
        #
        ##load environmental model
        #self.environ = self.loader.loadModel(
        #                '/Developer/Panda3D/models/environment')
        ##reparent the model to the renderer
        #self.environ.reparentTo(self.render)
        ##Apply scale and position transforms to the model
        #self.environ.setScale(0.25,0.25,0.25)
        #self.environ.setPos(-8,42,0)
        #
        #self.taskMgr.add(self.spincameratask, 'spincameratask')
        self.fig = plt.figure()
        self.ax = self.fig.add_axes([0.1,0.1,0.8,0.8])
        self.fig.canvas.mpl_connect('pick_event',self.on_pick)
        
        #self.fig.canvas.mpl_connect('button_press_event',self.on_pick)
        pass
        
    def spincameratask(self, task):
        angleDegrees = task.time *6.0
        angleRadians = angleDegrees * (pi/180.0)
        self.camera.setPos(20* sin(angleRadians),-20.0*cos(angleRadians),3)
        self.camera.setHpr(angleDegrees,0,0)
        return Task.cont
    
    def createPangea(self, numCells=500,relax=0):
        
        x = np.random.random(numCells)
        y = np.random.random(numCells)
        
        self.vg = VoronoiGraph(zip(x,y))
        #perform relax steps of Lloyd relaxation
        for i in range(relax):
            x=np.zeros(numCells)
            y=np.zeros(numCells)
            for i,cell in enumerate(self.vg.cells):
                x[i]=np.mean(cell.vertices[:,0])
                y[i]=np.mean(cell.vertices[:,1])
            self.vg = VoronoiGraph(zip(x,y))
        
        # use this graph to perform Lloyd relaxtion an generate new graphy
        for cell in self.vg.cells:
            cell.name = 'land'
            cell.elevation = 1
            cell.color = biomes['land']
        
    
    def createOceans(self, landToWaterRatio=0.4):
        #hull_points will be the seeds sites for water
        waterList = self.vg.hull_points
        landList = self.vg.interior_points
        for i in waterList:
            self.vg.cells[i].color=biomes['water']
            self.vg.cells[i].name = 'water'
            self.vg.cells[i].elevation = 1
        curr_ratio = self.vg.N-len(self.vg.hull_points)/float(self.vg.N)
        while curr_ratio > landToWaterRatio:
            i = random.choice(waterList) #pick random water cell
            j = random.choice(self.vg.cells[i].neighbors) #pick one of its neighbors at random
            if j in landList:
                self.vg.cells[j].color = biomes['water']
                self.vg.cells[j].name = 'water'
                self.vg.cells[j].elevation = 0
                landList.remove(j)
                waterList.append(j)    
                curr_ratio = len(landList)/float(self.vg.N)  
    
    #need to implement minSize effect
    def erodeTinyIslands(self, minSize=1):
        #erode 1 element islands
        for cell in self.vg.cells:
            island = True
            #check for a land neighbor
            for neigh in cell.neighbors:
                if self.vg.cells[neigh].name == 'land':
                    island = False #its not a size one island
            if island:
                cell.color = biomes['water']
                cell.name = 'water'
                cell.elevation = 0
                
    def smoothCoastlines(self, scale=1):
        pass
    
    def createLakes(self, lakeRatio=0.10,meanSize=3):
        #get a distribution of lake sizes
        numLakeCells = int(lakeRatio*self.vg.N)
        sizes = list(stats.poisson.rvs(meanSize,size=int(numLakeCells/meanSize))+1)
        totalLakes = 0
        while totalLakes < numLakeCells:
            i = random.randint(0,self.vg.N-1)
            cell = self.vg.cells[i]
            if cell.name=='land':
                lakeSize = stats.poisson.rvs(meanSize)+1 #1...INF
                #make lakeSize neighbors into lake
                size = min(lakeSize-1,len(cell.neighbors)) #might be fewer neighbors than lakesize
                cell.name='lake'
                cell.color = biomes['lake']
                totalLakes+=1
                for k in range(size):
                    otherCell = cell.neighbors[k]
                    self.vg.cells[otherCell].name='lake'
                    self.vg.cells[otherCell].color = biomes['lake']
                    totalLakes+=1
        
    def createMountains(self, mountainRatio=0.1,meanSize=7):
        numMtnCells = int(mountainRatio*self.vg.N)
        totalMountains = 0
        while totalMountains < numMtnCells:
            start_cell = random.choice(self.vg.cells)
            if start_cell.name=='land' or  start_cell.name=='high_mountain':
                start_cell.name = 'high_mountain'
                start_cell.color = biomes[start_cell.name]
                #pick a direction for the fault line
                direction = 2*np.pi*np.random.rand() #direction in radians
                #propagate the mountain chain along this direction as much as possible
                for i in range(stats.poisson.rvs(meanSize)):
                    #calculate the directions to neighbors and pick one closest to Dir
                    closestDir = self.vg.closestNeighborInDirection(start_cell,direction)
                    nextInChain = self.vg.cells[start_cell.neighbors[closestDir]] 
                    nextInChain.name = 'high_mountain'
                    nextInChain.color = biomes[nextInChain.name]
                    totalMountains+=1
                    start_cell = nextInChain
        #now elevate all surrounding terrain
        for cell in self.vg.cells:
            if cell.name=='high_mountain':
                #elevate all non mountain neighbors
                for i in cell.neighbors:
                    neighbor = self.vg.cells[i]
                    neighbor.increase_elevation(1)   
    
    def createRivers(self, riverRatio):
        pass
    
    def createForests(self, forestRatio,meanSize=2):
        numForestCells = int(forestRatio*self.vg.N)
        totalForests = 0
        while totalForests < numForestCells:
            start_cell = random.choice(self.vg.cells)
            if start_cell.name=='land' or  start_cell.name=='forest':
                start_cell.name = 'forest'
                start_cell.color = biomes[start_cell.name]
                totalForests+=1
                #grow forests radially from start_cell
                for i in start_cell.neighbors:
                    neighbor = self.vg.cells[i]
                    if neighbor.name =='land':
                        neighbor.name = 'forest'
                        neighbor.color=biomes[neighbor.name]
                        totalForests+=1
    
    def createDeserts(self, desertRatio):
        pass
    
    def createArtic(self, articRatio=0.05):
        pass
    
    def on_pick(self, event):
        print 'in pick'
        artist = event.artist
        print artist
    
    
    
    
    
    
if __name__ == "__main__":
    app = WorldCreator()
    seed=1234
    np.random.seed(seed=seed)
    random.seed(seed)
    app.createPangea(numCells=1260,relax=1)
    app.createOceans()
    #app.createLakes(lakeRatio=0.01,meanSize=2)
    app.createForests(forestRatio=0.09)
    app.createArtic()
    app.erodeTinyIslands()
    app.createMountains(mountainRatio=0.015,meanSize=6)
    
    app.vg.draw_voronoi(app.ax)
    
    x = [ val[0] for val in app.vg.delaunay.points]
    y = [ val[1] for val in app.vg.delaunay.points]
    #app.vg._draw_cell_ids(app.ax)
    #app.vg.draw_delaunay(app.ax)
    #app.ax.plot(x,y,'ro',markersize=5)
    plt.xlim(0,1)
    plt.ylim(0,1)
    plt.show()
    
    #app.run()
