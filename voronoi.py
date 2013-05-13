from delaunay import Delaunay
from delaunay import Triangle
from delaunay import ConvexHull

from itertools import combinations

import numpy as np
import matplotlib.pyplot as plt

#need to figure out regions

class Voronoi():
    def __init__(self, delaunay_mesh):
        self.points = list(delaunay_mesh.sites) #central points in voronoi cell
        self.N = len(self.points)
        self.regions = [ [] for i in range(self.N)] #initialize empty voronoi regions
        self.vertices=[]
        #transform the delaunay triangle cicumcenters into
        #an orderded list of vornoi vertices
        for i,tri in enumerate(delaunay_mesh.triList):
            self.vertices.append(tri.cc)
            #add the circumcenter (which is a vornoi cell vertex)
            #to the three voronoi regions that the triangle spans
            for j in range(3):
                self.regions[tri.indices[j]].append(i)
        
        ##iterate through the regions and sort each by computing its convex hull
        ##this give us correct winding on polygons
        #for region in self.regions:
        #    points = []
        #    for vertexIndex in region:
        #        points.append(self.vertices[vertexIndex].tolist())
        #    hull = ConvexHull(points)
        
        
        #create connection map from  Delaunay triangulation
        self.neighbors = []
        for i in range(self.N):
            neighbors = set([])
            for edge in delaunay_mesh.edgeList:
                if i in edge:
                    neighbors.update(edge)
            neighbors.remove(i)
            neighbors = list(neighbors)
            neighbors.sort()
            self.neighbors.append(neighbors)
        
#debugging code
if __name__ == "__main__":
    np.random.seed(1234)
    n=100
    x = np.random.random(n)
    y = np.random.random(n)
    fig = plt.figure()
    ax = fig.add_axes([0.1,0.1,0.8,0.8],aspect='equal')
    d = Delaunay(x,y)
    
    v = Voronoi(d)
    
    d.draw_delaunay(ax)
    fig.canvas.mpl_connect('pick_event',d.on_pick)
    plt.show()
        
    