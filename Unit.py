import pyglet
import random
import math

class Unit(pyglet.sprite.Sprite):
    def __init__(self, fileName,x=50,y=50,batch=None):
        img = pyglet.resource.image(fileName)
        self.center_anchor(img)
        super(Unit, self).__init__(img,x=x,y=y,batch=batch)
        self.speed = random.randint(1,10)
        self.sdx=0
        self.sdy=0
    
    def center_anchor(self, img):
        img.anchor_x = img.width/2
        img.anchor_y = img.height/2
    
    def hit_test(self,mouse_x,mouse_y):
        #simple radius comparison
        a = mouse_x - self.x
        b = mouse_y - self.y
        dist = math.sqrt(a**2 +b**2)
        if dist < self.width/2:
            return True
        else:
            return False
    
    
    
