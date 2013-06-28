#implements Watsons algorithm to calculate the Delaunay Triangulation
#complexity O(n**1.5)

import matplotlib.patches as mpatches
import numpy as np
import matplotlib.nxutils as nx
import matplotlib.pyplot as plt
from matplotlib import collections
from matplotlib.patches import Circle
from itertools import combinations

class Triangle(object):
    def __init__(self, vertices,indices):
        self.vertices  = np.array(vertices)
        self.indices = list(indices) #position in global array
        self.indices.sort()#important to keep list sorted
        self.cc = (0,0) #circum ceneter
        self.cr = 0.0 #circumradius
        
        self.calcCircumCircle()
        self.complete = False
        self.color = (0.6,0.7,0.8)
        
    def calcCircumCircle(self):
        v = self.vertices
        Dca = np.dot( (v[2]-v[0]), (v[1]-v[0]) )
        Dba = np.dot( (v[2]-v[1]), (v[0]-v[1]) )
        Dcb = np.dot( (v[0]-v[2]), (v[1]-v[2]) )
        
        n1 = Dba*Dcb
        n2 = Dcb*Dca
        n3 = Dca*Dba
        
        if (n1+n2+n3)==0:
            print 'no way! CO-LINEAR!!!'
        self.crsq = (Dca+Dba)*(Dba+Dcb)*(Dcb+Dca) / (n1+n2+n3) /4.0
        self.cr = np.sqrt(self.crsq)
        self.cc = (n2+n3)*v[0] + (n3+n1)*v[1] + (n1+n2)*v[2]
        self.cc /= 2*(n1+n2+n3)
        
    def draw(self):
        self.patch = mpatches.Polygon(self.vertices,facecolor = self.color,alpha=0.3)
        self.patch.set_picker(True)
        return self.patch

class ConvexHull():
    
    
    def __init__(self, points):
        """Computes the convex hull of a set of 2D points.
     
        Input: an iterable sequence of (x, y) pairs representing the points.
        Output: a list of vertices of the convex hull in counter-clockwise order,
          starting from the vertex with the lexicographically smallest coordinates.
        Implements Andrew's monotone chain algorithm. O(n log n) complexity.
        """
        # 2D cross product of OA and OB vectors, i.e. z-component of their 3D cross product.
        # Returns a positive value, if OAB makes a counter-clockwise turn,
        # negative for clockwise turn, and zero if the points are collinear.
        def cross(o, a, b):
            return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
        # Sort the points lexicographically (tuples are compared lexicographically).
        points.sort()
     
        # Boring case: no points or a single point, possibly repeated multiple times.
        if len(points) <= 1:
            self.hull_points = points
     
        # Build lower hull 
        lower = []
        for p in points:
            while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
                lower.pop()
            lower.append(p)
     
        # Build upper hull
        upper = []
        for p in reversed(points):
            while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
                upper.pop()
            upper.append(p)
     
        # Concatenation of the lower and upper hulls gives the convex hull.
        # Last point of each list is omitted because it is repeated at the beginning of the other list. 
        self.hull_points = lower[:-1] + upper[:-1]  


class Delaunay():
    def __init__(self,sites):
        self.sites = list(sites) 
        self.sites.sort()
        self.triList = []
        x = [a[0] for a in sites]
        y = [a[1] for a in sites]
        #determine 3 vertices that bound the pointList
        self.N = len(x)
        xlim = (min(x),max(x))
        ylim = (min(y),max(y))
        dx = xlim[1]-xlim[0]
        dy = ylim[1]-ylim[0]
        #add a the super triangle to the tri list
        v1 = (xlim[0]-1.1*dx,ylim[0]-0.1*dy)
        v2 = (xlim[0]+0.5*dx,ylim[0]+1.5*1.2*dy)
        v3 = (xlim[1]+1.1*dx,ylim[0]-0.1*dy) 
        super_verts = np.array((v1,v2,v3))
        self.sites.append(v1)
        self.sites.append(v2)
        self.sites.append(v3)
        self.triList.append(Triangle(super_verts,[self.N,self.N+1,self.N+2])) 
        #pop first value off pointList
        
        for i in range(len(self.sites)-3): #dont iterate over superverts
            #self._graphical_debug()
            point = self.sites[i]
            triRemovalList = []
            edgeList = []
            for tri in self.triList:
                if not tri.complete:
                    dx_sq = (point[0]-tri.cc[0])**2
                    if dx_sq > tri.crsq:
                        tri.complete = True
                    else:
                        d_sq = dx_sq + (point[1]-tri.cc[1])**2
                        if d_sq < tri.crsq:
                            #point inside this tri's circumcircle
                            triRemovalList.append(tri)                            
                            edgeCombo = combinations(tri.indices,2)
                            for edge in edgeCombo:
                                edgeList.append(edge)   
            #delete all edges that occur exactly twice (they are interior)
            removalList=[]
            for edge in edgeList:
                if edgeList.count(edge)>1:
                    removalList.append(edge)
            for item in removalList:
                edgeList.remove(item)
            
            #connect this point to all edges in edgelist, creating new triangles
            for edge in edgeList:
                newTri = Triangle(( (self.sites[edge[0]]),(self.sites[edge[1]]),(self.sites[i]) ),
                                                                                [edge[0],edge[1],i])
                self.triList.append(newTri)
            
            #now that we are out of the loop, remove tri from the list
            for tri in triRemovalList:
                self.triList.remove(tri)
           
        #remove any triangle containing vertices from inital bounding superTriangle
        triRemovalList = []
        super_set = set(range(self.N,self.N+3))
        for tri in self.triList:
            if super_set.intersection(tri.indices): #if any of tri.indices in super_triangle
                triRemovalList.append(tri)
        for tri in triRemovalList:
                self.triList.remove(tri)
                
        #now decompose triangles into an edge list
        self.edgeList = []
        for tri in self.triList:
            edgeCombo = combinations(tri.indices,2)
            for edge in edgeCombo:
                self.edgeList.append(edge)
        
        self.edgeList = list(set(self.edgeList))
        #remove super triangle points
        self.sites.remove(v1)
        self.sites.remove(v2)
        self.sites.remove(v3)
        
    def draw(self,mpl_axes):
        #draw filled polygons
        for tri in self.triList:
            mpl_axes.add_patch(tri.draw())
        #draw edges
        lines =[]
        for edge in self.edgeList:
            lines.append( [ (self.sites[edge[0]][0],self.sites[edge[0]][1]),
                            (self.sites[edge[1]][0],self.sites[edge[1]][1]) ] )
        
        col = collections.LineCollection(lines,linewidth=3.0,color='r')
        mpl_axes.add_collection(col)
         
        #draw sites
        x = [val[0] for val in self.sites]
        y = [val[1] for val in self.sites]
        mpl_axes.plot(x,y,'bo',markersize = 8.5)
    
    def on_pick(self, event):
        print 'in pick'
        artist = event.artist
        for tri in self.triList:
            if artist==tri.patch:
                print 'bingo'
                tri.color = (1.0,0,0)
                #now color all tri sharing any of the vertices
                for other_tri in self.triList:
                    for index in other_tri.indices:
                        if (index in tri.indices) and not (other_tri is tri):
                            other_tri.color = (0.5,0,1.0)
        ax = plt.gca()
        ax.clear()
        self.draw(ax)
        plt.show()
        print artist
    
    
    #visualize the current state of the graph
    def _graphical_debug(self):
        fig = plt.figure()
        ax = fig.add_axes([0.1,0.1,0.8,0.8],aspect='equal')
        
        x = [a[0] for a in sites]
        y = [a[1] for a in sites]
        
        #draw triangles
        segList=[]
        circleList =[]
        for i,tri in enumerate(self.triList):
            ax.text(tri.cc[0],tri.cc[1],str(i),color='y')
            v=tri.vertices
            segList.append(((v[0][0],v[0][1]),(v[1][0],v[1][1])))
            segList.append(((v[1][0],v[1][1]),(v[2][0],v[2][1])))
            segList.append(((v[2][0],v[2][1]),(v[0][0],v[0][1])))
            circleList.append(Circle(tri.cc,tri.cr))
        col = collections.LineCollection(segList,linewidth=3.0,color='r')
        ax.add_collection(col)
         #draw circumcircles
        col2 = collections.PatchCollection(circleList,linewidth=3.5,color='g',alpha=0.2,
                                           edgecolors='k')
        ax.add_collection(col2)
        
        ax.plot(x,y,'o')
        for i,val in enumerate(self.sites):
            ax.text(val[0],val[1],str(i))
        
        plt.show()  
    
#debugging code
if __name__ == "__main__":
    np.random.seed(1234)
    n=100
    x = np.random.random(n)
    y = np.random.random(n)
    
    fig = plt.figure()
    ax = fig.add_axes([0.1,0.1,0.8,0.8],aspect='equal')
    sites = zip(list(x),list(y))
    sites.sort()
    sites = np.loadtxt('sites2.txt')
    sites = sites.tolist()
    d = Delaunay(sites)  
    d.draw(ax)
    fig.canvas.mpl_connect('pick_event',d.on_pick)
    plt.show()
            