from PySide import QtGui,QtCore
from voronoigraph import VoronoiGraph
import matplotlib.pyplot as plt
from  voronoiplotwidget import VoronoiPlotWidget
from worldcreator import WorldCreator
import MainWindowUI
import numpy as np
import sys
import time
import random


player_colors = {
            0:(0.1,0.6,0.6),
            1:(0.6,0.2,0.2),
            2:(0.6,0.6,0.1),
            3:(0.4,0.4,0.4)}


class RiskGUI(QtGui.QMainWindow):
    def __init__(self):
        super(RiskGUI,self).__init__()
        self.ui =  MainWindowUI.Ui_MainWindow()
        self.ui.setupUi(self)
        self.manualUISetup()
        
        #global mode flags
        self.deployMode = False
        self.moveMode = False
        self.attackMode = False        
    
    def manualUISetup(self):
        self.statusBar().showMessage('Ready')
       
        self.vgwidget=self.findChild(VoronoiPlotWidget,'VoronoiPlot')
        
        self.next_button=self.findChild(QtGui.QPushButton,'NextButton')
        self.next_button.clicked.connect(self.nextTurn)

    #function is called when you click the mouse to assign troops
    def placeTroops(self, cell):
        acceptable = ('arctic','land','forest')
        if (cell.name in acceptable) and (cell.owner in [self.currPlayer,-1] ):
            cell.owner = self.currPlayer
            cell.value+=1
            cell.owner_color = self.player_list[self.currPlayer]['color']
            self.player_list[self.currPlayer]['unassigned']-=1
    
    #function deploys troops for NPC players
    def selectTerritory(self): 
        #pick properties for each players to put armies on
        print 'deploying player %i armies'%self.currPlayer
        self.statusBar().showMessage('Player %s Choosing Territory...'% self.currPlayer)
        acceptable = ('arctic','land','forest')
        while self.player_list[self.currPlayer]['unassigned'] > 0:
            start_cell = random.choice(self.vg.cells) 
            if start_cell.name in acceptable:
                valid = start_cell.owner in [self.currPlayer,-1]
                if valid:
                    start_cell.value+=2
                    start_cell.owner_color = self.player_list[self.currPlayer]['color']
                    self.player_list[self.currPlayer]['unassigned'] -= 2
                    for i in start_cell.neighbors:
                        neighbor = self.vg.cells[i]
                        valid = neighbor.owner in [self.currPlayer,-1]
                        if neighbor.name in acceptable and valid:
                            if self.player_list[self.currPlayer]['unassigned'] > 0:
                                neighbor.value+=1
                                neighbor.owner_color = self.player_list[self.currPlayer]['color']
                                self.player_list[self.currPlayer]['unassigned'] -= 1
                
        self.vgwidget.Plot()
        
    def reinforce(self, player):
        pass
    
    def attack(self, player):
            pass
    
    def battle(self, cell_from, cell_to):
            pass
    
    def start_newgame(self):
            world = WorldCreator()
            seed=327
            np.random.seed(seed=seed)
            random.seed(seed)
            world.createPangea(numCells=600,relax=1)
            world.createOceans()
            world.createMountains(mountainRatio=0.006,meanSize=3)
            world.createForests(forestRatio=0.07)
            world.createLakes(lakeRatio=0.01,meanSize=4)
            
            world.createArctic_v2()
            world.erodeTinyIslands()
            
            self.vg = world.vg
            self.vgwidget.vg=self.vg
            self.vgwidget.controller = self
            self.vgwidget.Plot()
            
            self.player_list = [
                {'name':'One','owns':[],'unassigned':10,'color':player_colors[0]},
                {'name':'Two','owns':[],'unassigned':10,'color':player_colors[1]},
                {'name':'Three','owns':[],'unassigned':10,'color':player_colors[2]},
                {'name':'Four','owns':[],'unassigned':10,'color':player_colors[3]}
            ]
            
            order = [0,1,2,3]
            random.shuffle(order)
            print order
            for playerNum in order:
                if playerNum == 0: #non-NPC
                    self.currPlayer=playerNum
                    QtGui.QMessageBox.information(None,'Test1','Place your initial troops')
                    app=QtGui.QApplication.instance()
                    self.deployMode = True
                    while self.player_list[self.currPlayer]['unassigned'] > 0:
                        app.processEvents() #wait until user selects tiles
                else:
                    self.currPlayer=playerNum
                    self.selectTerritory()
    
    @QtCore.Slot()
    def nextTurn(self):
        self.statusBar().showMessage('Calculating Next Moves...')
        for player in self.player_list:
            self.statusBar().showMessage('Player %s Acting...'% player['name'])
            self.attack(player)        
        
        


if __name__ == "__main__":   

    app=QtGui.QApplication.instance() # checks if QApplication already exists 
    if not app: # create QApplication if it doesnt exist 
        app = QtGui.QApplication(sys.argv)
    pixmap = QtGui.QPixmap("risk.jpg")
    splash = QtGui.QSplashScreen(pixmap,
            QtCore.Qt.FramelessWindowHint|QtCore.Qt.WindowStaysOnTopHint)
    splash.show()
    alphorn = QtGui.QSound('alph_3.m4a')
    alphorn.play()
    time.sleep(2)
    splash.close()
    
    riskWin = RiskGUI()    
    riskWin.show()
    app.setActiveWindow(riskWin)
    
    riskWin.start_newgame()
    
    sys.exit(app.exec_())