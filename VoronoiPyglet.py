#setup window
import pyglet
from voronoigraph import VoronoiGraph
from worldcreator import WorldCreator
import random
import numpy as np
import time

from pyglet.gl import *
from Unit import Unit

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
                
        self.unit_batch = pyglet.graphics.Batch()
        self.unit_list=[]
        for i in range(5):
            x = random.randint(0,self.width)
            y = random.randint(0,self.height)
            unit = Unit('resources/test_sprite.png',x=x,y=y,batch=self.unit_batch)
            unit.sdx = random.randint(-5,5)
            unit.sdy = random.randint(-5,5)
            self.unit_list.append(unit)
        self.selected_unit = None
                
        self.width = img.width*3
        self.height = img.height*3
        self.set_visible()
    
        pyglet.clock.schedule_interval(self.update_pos,1/30.0)
        
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
        
        #draw units
        self.unit_batch.draw()
        
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
        
        for unit in self.unit_list:
            if unit.hit_test(x,y):    
                self.selected_unit = unit

    def on_mouse_release(self,x,y,button,modifiers):
        self.selected_unit = None
    
    def on_mouse_drag(self,x,y,dx,dy,buttons,modfiers ):
        print "mouse drag",x,y,dx,dy
        if self.selected_unit:
            self.selected_unit.x +=dx
            self.selected_unit.y +=dy
    
    def update_pos(self, dt):
        for unit in self.unit_list:
            unit.x+=unit.speed*unit.sdx*dt
            unit.y+=unit.speed*unit.sdy*dt
            
            #perform 2D screen wrapping
            if unit.x - unit.width/2 > self.width:
                unit.x -= unit.width +self.width
            elif unit.x + unit.width/2 < 0:
                unit.x += unit.width +self.width
            if unit.y - unit.height/2 > self.height:
                unit.y -= unit.height +self.height
            elif unit.y + unit.height/2 < 0:
                unit.y += unit.height +self.height
                
            
    
    
    
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
    
    