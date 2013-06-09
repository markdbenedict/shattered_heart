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

class MatplotlibWidget(FigureCanvas):
 
    def __init__(self, parent=None):
        settings = QtCore.QSettings("MBBH", "RISK")
        self.ScreenDPI = int(settings.value('ScreenDPI','80'))
         
        self.figure = Figure(dpi=self.ScreenDPI)
        self.axes = self.figure.add_axes([0.1,0.1,0.8,0.8],frame_on=False,xticks=[],yticks=[])
        FigureCanvas.__init__(self, self.figure)
        self.setParent(parent)
        
        
     
    def Plot(self):
        if self.vg!=None:
            self.vg.draw_voronoi(self.axes)
        self.draw()
    
    def resizeEvent(self,event):
        
        height = self.size().height()/float(self.ScreenDPI)
        width = self.size().width()/float(self.ScreenDPI)
        self.figure.set_size_inches(width,height,forward=True)
        
        self.positionCBarEdits()
        self.draw()
        
    def mousePressEvent(self,event):
        if self.zoomInActButton and self.zoomInActButton.isChecked():
            height = self.figure.get_figheight()*self.figure.dpi
            inLeft = self.leftAxes.bbox.contains(event.pos().x(),height-event.pos().y())
            inRight = self.rightAxes.bbox.contains(event.pos().x(),height-event.pos().y())
            if inLeft or inRight:
                if self.rubberBand is None:
                    self.zoomOrigin = event.pos()
                    self.rubberBand = QtGui.QRubberBand(QtGui.QRubberBand.Rectangle, self)
                    rect = QtCore.QRect(self.zoomOrigin,QtCore.QSize())
                    self.rubberBand.setGeometry(rect)
                    pal = QtGui.QPalette()
                    pal.setBrush(QtGui.QPalette.Foreground, QtGui.QBrush(QtCore.Qt.green))
                    pal.setBrush(QtGui.QPalette.Base, QtGui.QBrush(QtCore.Qt.red))
                    
                    pal.setBrush(QtGui.QPalette.Highlight, QtGui.QBrush(QtCore.Qt.red))
                    self.rubberBand.setPalette(pal)
                    self.rubberBand.show()
            
    
    def mouseMoveEvent(self,event):
        if self.zoomInActButton and self.zoomInActButton.isChecked():
            if self.rubberBand is not None:
                pos = event.pos()
                #constrain to aspect ratio of figure, key off Y
                deltaX = event.pos().x() - self.zoomOrigin.x() 
                deltaY = event.pos().y() - self.zoomOrigin.y()
                scaleX = float(deltaY)*self.zoomAspect                
                newPos = QtCore.QPoint(self.zoomOrigin.x()-scaleX,pos.y())
                self.zoomPos = newPos
                self.rubberBand.setGeometry(QtCore.QRect(self.zoomOrigin, newPos).normalized())
 
    def mouseReleaseEvent(self,event):
        height = self.figure.get_figheight()*self.figure.dpi
        if self.zoomInActButton and self.zoomInActButton.isChecked():
            if self.rubberBand is not None:
                pos = self.zoomPos
                endInLeft = self.leftAxes.bbox.contains(pos.x(),height-pos.y())
                endInRight = self.rightAxes.bbox.contains(pos.x(),height-pos.y())
                if endInLeft or endInRight:
                    end = pos
                    start =self.zoomOrigin
                    
                    self.isZoomed=True
                    invFigure = self.figure.transFigure.inverted()
                    start = invFigure.transform((start.x(),start.y()))
                    end = invFigure.transform((end.x(),end.y()))
                    #print start,end
                    self.zoomExtents=(end[0],end[1],start[0],start[1])
                    start2 = self.figure.transFigure.transform(start)
                    end2 = self.figure.transFigure.transform(end)
                    self.zoomFactor=float(self.rightAxes.get_window_extent().height)/abs(end2[1]-start2[1])
                    self.controller.statusBar().showMessage(str(self.zoomFactor))
                else:
                    print 'not in Focus'
                #reset instance variables
                self.zoomInActButton.defaultAction().toggle()
                self.rubberBand.hide()
                self.rubberBand = None #reset rubberband
        self.Plot()
    
    def mouseDoubleClickEvent(self,event):
        #handle addition of watchPoint
        
        if self.watchPointButton and self.watchPointButton.isChecked() and len(self.availWatchID)>0:
            newIcon=WatchPoint(self,self.availWatchID.pop())
            image=newIcon.pixmap()
            newIcon.move(event.x()-image.width()/2.,event.y()-image.height()/2)
            newIcon.show()
            pos = event.pos()
            rinv = self.rightAxes.transData.inverted()
            height = self.figure.get_figheight()*self.figure.dpi
            pos2 = rinv.transform((pos.x(),height - pos.y()))
            newIcon.x = pos2[0] # store values in axes coordinates
            newIcon.y = pos2[1]
            self.watchPointList.append(newIcon)
            newIcon.closed.connect(self.controller.closeWatchPointField)
            newIcon.closed.connect(self.closeWatchPointField)
            newIcon.updatedVal.connect(self.controller.updateWatchPointField)
            newIcon.updatedPos.connect(self.updateWatchPointPos)
            self.controller.addWatchPointField(str(newIcon.watchID),newIcon.watchID)
            newIcon.updateValue(self.getValueAt(newIcon.x,newIcon.y))
            self.watchPointButton.defaultAction().toggle() #turn toolbutton state off after adding watchpoint
            self.unsetCursor()
            
        #handle addition of an annotation
        elif self.annotateButton and self.annotateButton.isChecked():
            newText=Annotation(self,'Type Here')
            newText.move(event.x(),event.y())
            newText.show()
            pos = event.pos()
            rinv = self.rightAxes.transData.inverted()
            height = self.figure.get_figheight()*self.figure.dpi
            pos2 = rinv.transform((pos.x(),height - pos.y()))
            newText.x = pos2[0] # store values in axes coordinates
            newText.y = pos2[1]
            self.annotationList.append(newText)
            
            self.annotateButton.defaultAction().toggle()
            self.unsetCursor()
        
        else:
            pos = event.pos()
            height = self.figure.get_figheight()*self.figure.dpi
            #check to see if either ColorBar was double clicked, if so bring up colomap dialog
            if self.leftCBarAxes.bbox.contains(pos.x(),height - pos.y()):
                self.on_click_cbar(self.leftCBarAxes)
            elif self.rightCBarAxes.bbox.contains(pos.x(),height - pos.y()):
                self.on_click_cbar(self.rightCBarAxes)
    
    #x,y are in axes coordinates, must transform to data coordinates
    #move watchpoint in response to user request via non drag event
    @QtCore.Slot(int)
    def updateWatchPointPos(self,watchID):
        #iterate through list and find right one
        for watchPoint in self.watchPointList:
            if watchPoint.watchID==watchID:
                watchPoint.updateValue(self.getValueAt(watchPoint.x,watchPoint.y))
    
    
    
    
        
    
