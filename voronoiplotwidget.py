# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>
import matplotlib
matplotlib.rcParams['backend.qt4']='PySide'
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.image as mpimg
import math
from PySide import QtGui,QtCore
import numpy as np

class VoronoiPlotWidget(FigureCanvas):
 
    def __init__(self, parent=None):
        settings = QtCore.QSettings("MBBH", "RISK")
        self.ScreenDPI = int(settings.value('ScreenDPI','80'))
         
        self.figure = Figure(dpi=self.ScreenDPI)
        self.axes = self.figure.add_axes([0.1,0.1,0.8,0.8],frame_on=False,xticks=[],yticks=[])
        FigureCanvas.__init__(self, self.figure)
        
        #self.figure.canvas.mpl_connect('pick_event',self.on_pick)
        self.setParent(parent)
        self.controller = None
        self.vg=None
        
        self.cell_from=-1
        self.cell_to=-1
        
    def show(self):
        self.Plot()
    
     
    def Plot(self):
        if self.vg!=None:
            self.vg.draw_voronoi(self.axes)
        self.draw()
    
    def resizeEvent(self,event):
        
        height = self.size().height()/float(self.ScreenDPI)
        width = self.size().width()/float(self.ScreenDPI)
        self.figure.set_size_inches(width,height,forward=True)
        
        self.draw()
    
    def pick(self,event,mouse_down):
        win_pos = event.pos()
        inv = self.axes.transData.inverted()
        height = self.figure.get_figheight()*self.figure.dpi
        mpl_pos = inv.transform((win_pos.x(),height - win_pos.y()))
        
        #determine which if any cell was picked
        for cell in self.vg.cells:
            result = cell.contains(mpl_pos)
            if result == True:
                print 'found match in cell',cell.id
                
                if mouse_down:
                    self.cell_from=cell.id
                    cell.color = (0.2,0.9,0.9)
                    for i in cell.neighbors:
                        self.vg.cells[i].color = (0.8,0.8,0.8)
                    
                elif cell.id in self.vg.cells[self.cell_from].neighbors:
                    self.cell_to = cell.id
                    cell.color = (0.2,0.9,0.9)
                self.Plot()
                return True
        
        return False
        
    def mousePressEvent(self,event):
        self.pick(event,True)
        
    def mouseReleaseEvent(self,event):
        if self.pick(event,False):
            self.controller.battle(self.cell_from,self.cell_to)    
    
    
    
    
    
        
    
