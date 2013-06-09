from PySide import QtGui,QtCore
from voronoigraph import VoronoiGraph
import matplotlib.pyplot as plt
from  voronoiplotwidget import VoronoiPlotWidget
from worldcreator import WorldCreator
import MainWindowUI
import numpy as np
import sys
import time

player_colors = {
            0:(0.2,0.8,0.8,0.2),
            1:(0.8,0.2,0.2,0.2),
            2:(0.8,0.8,0.2,0.2),
            3:(0.8,0.8,0.8,0.2)}


class RiskGUI(QtGui.QMainWindow):
    def __init__(self,vg):
        super(RiskGUI,self).__init__()
        self.ui =  MainWindowUI.Ui_MainWindow()
        self.ui.setupUi(self)
        self.vg = vg
        self.manualUISetup()
        self.setupMap()
    
    def manualUISetup(self):
        self.statusBar().showMessage('Ready')
       
        self.vgwidget=self.findChild(VoronoiPlotWidget,'VoronoiPlot')
        self.vgwidget.vg=self.vg
        self.vgwidget.controller = self
        self.vgwidget.Plot()
        
        self.next_button=self.findChild(QtGui.QPushButton,'NextButton')
        self.next_button.clicked.connect(self.nextTurn)

    
    def setupMap(self): 
        #start with a default of three cpu players, 1 human
        self.player_list =  [
                                {'name':'One','owns':[],'color':player_colors[0]},
                                {'name':'Two','owns':[],'color':player_colors[1]},
                                {'name':'Three','owns':[],'color':player_colors[2]}
                            ]
        #allow
        
        #pick properties for each players to put armies on
        for player in self.player_list:
            self.statusBar().showMessage('Player %s Choosing Territory...'% player['name'])
    
        self.statusBar().showMessage('')
        
    def reinforce(self, player):
        pass
    
    def attack(self, player):
        pass
    
    def battle(self, cell_from, cell_to):
        pass
    
    @QtCore.Slot()
    def nextTurn(self):
        self.statusBar().showMessage('Calculating Next Moves...')
        for player in self.player_list:
            self.statusBar().showMessage('Player %s Acting...'% player['name'])
            self.attack(player)        
        
        
if __name__ == "__main__":
    world = WorldCreator()
    seed=3284
    np.random.seed(seed=seed)
    world.createPangea(numCells=500,relax=1)
    world.createOceans()
    world.createMountains(mountainRatio=0.012,meanSize=12)
    world.createForests(forestRatio=0.07)
    world.createLakes(lakeRatio=0.01,meanSize=4)
    
    #app.createArtic()
    world.erodeTinyIslands()    
    

    app=QtGui.QApplication.instance() # checks if QApplication already exists 
    if not app: # create QApplication if it doesnt exist 
        app = QtGui.QApplication(sys.argv)
    pixmap = QtGui.QPixmap("risk.jpg")
    splash = QtGui.QSplashScreen(pixmap)
    splash.show()
    time.sleep(.2)
    splash.close()
    
    riskWin = RiskGUI(world.vg)    
    riskWin.show()
    app.setActiveWindow(riskWin)
    
    sys.exit(app.exec_())