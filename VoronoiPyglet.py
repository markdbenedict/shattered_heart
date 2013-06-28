#setup window
import pyglet
from pyglet import window

class MapWindow(pyglet.window.Window):
    def __init__(self):
        super(MapWindow,self).__init__(visible=False, resizable=True)
        
        img = pyglet.image.load('./resources/ocean.jpg').get_texture(rectangle=True)
        self.background = pyglet.image.TileableTexture.create_for_image(img)
    
        self.width = img.width*4
        self.height = img.height*3
        self.set_visible()
        
    def on_draw(self ):
        self.clear()
        
        self.background.blit_tiled(0, 0, 0, self.width, self.height)
        #draw backgroup
        
        #draw territory boundaries
        #pyglet.gl.GL_LINE_LOOP
        
        #fill territories
        #pyglet.gl.GL_TRIANGLE_FAN
    
        #or
        
        #pyglet.gl.GL_POLYGON

#draw convex hull

#draw cell boundaries, edge list, set() would eliminate double draws but might be too expensive

#to fill in voronoi cells need to draw triangles of type (center, edge[i],edge[i])

if __name__ == "__main__":
    mainWin = MapWindow()
    pyglet.app.run()
    
    