#setup window
import pyglet
from voronoigraph import VoronoiGraph
from worldcreator import WorldCreator
import random
import numpy as np
import time

from pyglet.gl import *

biomes = {  'water':(0.3,0.4,0.7),
            'land':(238/255.0,207/255.0,161/255.0),
            'mountain':(139/255.0,90/255.0,0),
            'high_mountain':(0.9,0.85,0.85),
            'hill':(0.4,0.4,0.3),
            'lake':(0.3,0.4,0.95),
            'river':(0.3,0.5,0.6),
            'forest':(110/255.0,139/255.0,61/255.0),
            'arctic':(0.95,0.95,0.95),
            'desert':(0.6,0.9,0.9)}

class MapWindow(pyglet.window.Window):
    def __init__(self,vg):
        config = Config(sample_buffers=1, samples=6, 
                    depth_size=16, double_buffer=True,)
        super(MapWindow,self).__init__(visible=False, resizable=True,config=config)
        self.vg=vg
        img = pyglet.image.load('./resources/ocean.jpg').get_texture(rectangle=True)
        self.background = pyglet.image.TileableTexture.create_for_image(img)
        self.batch = pyglet.graphics.Batch()
        self.translate_vg()
        
        self.width = img.width*3
        self.height = img.height*3
        self.set_visible()
    
    
    def refresh_draw_list(self):
        start = time.time()
        self.batch1 = pyglet.graphics.Batch()
        self.batch2 = pyglet.graphics.Batch()
        water = ('water','lake')
        for territory in self.vg.cells:
            if territory.name not in water:
                verts = territory.vertices*self.width
                verts=verts.ravel().tolist()
                self.batch1.add(len(verts)//2, pyglet.gl.GL_LINE_LOOP,None,('v2f/static',verts))
                self.batch2.add(len(verts)//2, pyglet.gl.GL_POLYGON,None,('v2f/static',verts))
        
        print 'calc time = ',time.time()-start
    
    
    def on_draw(self ):
        start = time.time()
        self.clear()
        
        self.background.blit_tiled(0, 0, 0, self.width, self.height)
        
        pyglet.gl.glEnable (GL_BLEND)                                                            
        pyglet.gl.glEnable (GL_LINE_SMOOTH);                                                     
                
        water = ('water','lake')
        for territory in self.vg.cells:
            if territory.name not in water:
                verts = territory.vertices*self.width
                verts=verts.ravel().tolist()
                
                #pyglet.gl.glColor4f(0.0,0,0,1.0)                                                                                    
                glPointSize(3)
                pyglet.graphics.draw(len(verts)//2, pyglet.gl.GL_POINTS,('v2f',verts),('c3B',[0,0,0]*(len(verts)//2)))
                pyglet.gl.glLineWidth (3)                     
                
                pyglet.graphics.draw(len(verts)//2, pyglet.gl.GL_LINE_LOOP,('v2f',verts),('c3B',[0,0,0]*(len(verts)//2)))
               
                pyglet.graphics.draw(len(verts)//2, pyglet.gl.GL_POLYGON,('v2f',verts),
                                     ('c3f',territory.color*(len(verts)//2)))

        print 'draw time = ',time.time()-start
        
    def translate_vg(self ):
        #self.refresh_draw_list()
        pass
    
#draw convex hull

#draw cell boundaries, edge list, set() would eliminate double draws but might be too expensive

#to fill in voronoi cells need to draw triangles of type (center, edge[i],edge[i])

if __name__ == "__main__":
    
    world = WorldCreator()
    seed=327
    np.random.seed(seed=seed)
    random.seed(seed)
    
    world.createPangea(numCells=800,relax=1)
    world.createOceans()
    world.createMountains(mountainRatio=0.006,meanSize=3)
    world.createForests(forestRatio=0.07)
    world.createLakes(lakeRatio=0.01,meanSize=4)
    
    world.createArctic_v2()
    world.erodeTinyIslands()
    
    mainWin = MapWindow(world.vg)
    pyglet.app.run()
    
    