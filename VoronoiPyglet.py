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


class Camera(object):

    def __init__(self, win, zoom=1.0):
        self.win = win
        self.zoom = zoom

    def worldProjection(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        widthRatio = self.win.width / self.win.height
        gluOrtho2D(
            -self.zoom * widthRatio,
            self.zoom * widthRatio,
            -self.zoom,
            self.zoom)

    def hudProjection(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, self.win.width, 0, self.win.height)

class MapWindow(pyglet.window.Window):
    def __init__(self,vg):
        config = Config(sample_buffers=1, samples=6, 
                    depth_size=16, double_buffer=True,)
        super(MapWindow,self).__init__(visible=False, resizable=True,config=config)
        self.vg=vg
        
        
        img = pyglet.image.load('./resources/ocean.jpg').get_texture(rectangle=True)
        self.background = pyglet.image.TileableTexture.create_for_image(img)
        
        self.texture  = pyglet.image.load('./resources/test.jpg').get_texture()
        
        self.points_batch = pyglet.graphics.Batch()
        self.line_list = []
        self.poly_list =[]
        
        self.refresh_draw_list()
                
        self.width = img.width*3
        self.height = img.height*3
        self.set_visible()
    
        
    def on_draw(self ):
        start = time.time()
        self.clear()
        
        self.background.blit_tiled(0, 0, 0, self.width, self.height)
        
        #pyglet.gl.glEnable (GL_BLEND)
        #glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        pyglet.gl.glEnable (GL_LINE_SMOOTH);
        #glActiveTexture(GL_TEXTURE0)
        #glClientActiveTexture(GL_TEXTURE0)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
        
        glEnable(self.texture.target)
        glBindTexture(self.texture.target,self.texture.id)
        for poly in self.poly_list:
            poly.draw(GL_POLYGON)
        glDisable(self.texture.target)
        
        glPointSize(2)
        self.points_batch.draw()
        glLineWidth (2)
        for vertex_array in self.line_list:
            vertex_array.draw(GL_LINE_LOOP)
        
        print 'draw time = ',time.time()-start
        
                
    def refresh_draw_list(self):
        start = time.time()
       
        water = ('water','lake')
        for territory in self.vg.cells:
            if territory.name not in water:
                verts = territory.vertices*self.width
                t_vertsX = (verts[:,0]-verts[:,0].min())/verts[:,0].ptp()
                t_vertsY = (verts[:,1]-verts[:,1].min())/verts[:,1].ptp()
                tverts = np.array(zip(t_vertsX,t_vertsY)).ravel().tolist()
                verts=verts.ravel().tolist()
                self.points_batch.add(len(verts)//2, pyglet.gl.GL_POINTS,None,('v2f',verts),('c3B',[0,0,0]*(len(verts)//2)))                
                vert_list = pyglet.graphics.vertex_list(len(verts)//2,('v2f/static',verts),('c3B/static',[0,0,0]*(len(verts)//2)))
                self.line_list.append(vert_list)
                poly = pyglet.graphics.vertex_list(len(verts)//2,('v2f/static',verts),('c3f/static',territory.color*(len(verts)//2)),
                                     ('t2f/static',tverts) )
                self.poly_list.append(poly)
        print 'parse time = ',time.time()-start
        
    def on_mouse_press(self,x, y, button, modifiers):
        print 'mouse pressed',x,y,button
        pass

    def on_mouse_release(self,x,y,button,modifiers):
        pass
    
    def on_mouse_drag(self,x,y,dx,dy,buttons,modfiers ):
        print "mouse drag",x,y,dx,dy
        pass
    
    
    
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
    
    