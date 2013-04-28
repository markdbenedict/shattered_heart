import numpy as np
import matplotlib.pyplot as plt
from matplotlib import collections
import matplotlib.patches as mpatches
import random

from pyhull.delaunay import DelaunayTri
from pyhull.convex_hull import ConvexHull
from pyhull.voronoi import VoronoiTess

from voronoicell import VoronoiCell

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

class VoronoiGraph():
    def __init__(self,point_array):
        self.hull = ConvexHull(point_array)
        self.delaunay = DelaunayTri(point_array)
        self.vor = VoronoiTess(point_array)
        self.N = len(self.vor.regions)
        
        self.hull_points = [a[0] for a in self.hull.vertices]
        self.interior_points = set(range(self.N))
        for point in self.hull_points:
            self.interior_points.discard(point)
        
        #create a position dependant list of VoronoiCells
        adj_list = self._create_adj_matrix()
        self.cells = []
        for i in range(self.N):
            theCell = VoronoiCell()
            theCell.id = i
            theCell.center = self.vor.points[i]
            cleanVerts = list(self.vor.regions[i])
            if 0 in cleanVerts: cleanVerts.remove(0)
            theVerts = np.array([self.vor.vertices[vert] for vert in cleanVerts])
            theCell.vertices = theVerts
            theCell.neighbors = list(adj_list[i])
            if i in self.hull_points:
                theCell.hull_point = True
            self.cells.append(theCell)

    
    #find the VoronoiCell containg (x,y)
    def contains(self,x,y):
        pass

    def draw_voronoi(self,mpl_axis):
        for cell in self.cells:
            mpl_axis.add_patch(cell.draw())
      
    def draw_delaunay(self,mpl_axis):
        #plot the delaunay graph, simplices are triangles
       
        for tri in self.delaunay.simplices:
            x = []
            y = []
            coords = tri.coords
            for i in range(3):
                x.append(coords[i][0])
                y.append(coords[i][1])
                mpl_axis.plot(x,y,color='g',linestyle='--',linewidth = 1.5)
       
      

    def draw_hull(self,mpl_axis):
        #plot the convex hull
        segList=[]
        for seg in self.hull.simplices:
            a = np.array(seg.coords)
            segList.append(((a[0][0],a[0][1]),(a[1][0],a[1][1])))
            
        col = collections.LineCollection(segList,linewidth=3.0)
        mpl_axis.add_collection(col)
    
    def closestNeighborInDirection(self,start_cell,direction):
        dirs=[]
        for n in start_cell.neighbors:
            cell = self.cells[n]
            nDir = (cell.center[0] - start_cell.center[0],cell.center[1] - start_cell.center[1])
            dirs.append(np.arctan2(nDir[1],nDir[0]))
        a = np.array(dirs)
        a -= direction
        a = np.abs(a)
        closestDir = a.argmin()
        return closestDir    

    #internal function to create adjancey lists for dealunay graph
    #1:1 correspondence between vor.region index and delaunay.points
    def _create_adj_matrix(self):
        adjList = []
        for i in range(self.N):
            neighbors = []
            for item in self.delaunay.vertices:
                if i in item:
                    for j in item:
                        if j!=i:
                            neighbors.append(j)
            adjList.append(set(neighbors))
        return adjList
    
    #function to help label points and cells for algorithm visual debugging
    def _draw_cell_ids(self,mpl_axis):
        for i,item in enumerate(self.delaunay.points):
            mpl_axis.text(item[0],item[1],str(i))
            
if __name__ == "__main__":
    n=500
    #np.random.seed(seed=1234)
    x = np.random.random(n)
    y = np.random.random(n)
    fig = plt.figure()
    ax = fig.add_axes([0.1,0.1,0.8,0.8])
    vg = VoronoiGraph(zip(x,y))
    
    
    waterColor = (0.3,0.4,0.7)
    landColor = (0.5,0.7,0.7)
    land_ratio = 0.4  #land / water
    
    #hull_points will be the seeds sites for water
    waterList = vg.hull_points
    landList = vg.interior_points
    for i in waterList:
        vg.cells[i].color=biomes['water'] 
    curr_ratio = vg.N-len(vg.hull_points)/float(vg.N)
    while curr_ratio > land_ratio:
        i = random.choice(waterList) #pick random water cell
        j = random.choice(vg.cells[i].neighbors) #pick one of its neighbors at random
        if j in landList:
            vg.cells[j].color = biomes['water']
            landList.remove(j)
            waterList.append(j)    
            curr_ratio = len(landList)/float(vg.N)
            
    #erode 1 element islands
    for cell in vg.cells:
        island = True
        i=0
        #check for a land neighbor
        for i in cell.neighbors:
            if vg.cells[i].color[0] == biomes['land'][0]:
                i+=1
                island = False
        if island:
            cell.color = biomes['water']
    print i,vg.N

    vg.draw_voronoi(ax)
    vg.draw_delaunay(ax)
    ax.plot(x,y,'ro',markersize=3)
    plt.xlim(0,1)
    plt.ylim(0,1)
    plt.show()
    
    
        
    