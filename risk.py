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
        if (cell.name in acceptable):
            if cell.changeOwner(self.currPlayer):
                cell.value+=1
                cell.owner_color = self.player_list[self.currPlayer]['color']
                self.player_list[self.currPlayer]['unassigned']-=1
                if self.player_list[self.currPlayer]['unassigned'] <= 0:
                    self.deployMode = False
    
    #function deploys troops for NPC players
    def selectTerritory(self): 
        #pick properties for each players to put armies on
        print 'deploying player %i armies'%self.currPlayer
        self.statusBar().showMessage('Player %s Choosing Territory...'% self.currPlayer)
        acceptable = ('arctic','land','forest')
        while self.player_list[self.currPlayer]['unassigned'] > 0:
            start_cell = random.choice(self.vg.cells) 
            if start_cell.name in acceptable:
                if start_cell.changeOwner(self.currPlayer):
                    numArmy = self.player_list[self.currPlayer]['unassigned']
                    if numArmy > 2:
                        numArmy = 2
                    start_cell.value += numArmy
                    start_cell.owner_color = self.player_list[self.currPlayer]['color']
                    self.player_list[self.currPlayer]['unassigned'] -= numArmy
                    numArmy = self.player_list[self.currPlayer]['unassigned']
                    neighbors = list(start_cell.neighbors)
                    random.shuffle(neighbors)
                    while len(neighbors) > 0:
                        i = neighbors.pop()
                        neighbor = self.vg.cells[i]
                        if neighbor.name in acceptable and numArmy > 0:
                            changed = neighbor.changeOwner(self.currPlayer)
                            if changed:
                                neighbor.value+=1
                                numArmy -= 1
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
            start = time.time()
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
            
            end = time.time()
            print end - start
    
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
                    pass
                    '''self.currPlayer=playerNum
                    QtGui.QMessageBox.information(None,'Test1','Place your initial troops')
                    app=QtGui.QApplication.instance()
                    self.deployMode = True
                    while self.player_list[self.currPlayer]['unassigned'] > 0:
                        app.processEvents() #wait until user selects tiles'''
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
    pixmap = QtGui.QPixmap(r"/resources/risk.jpg")
    splash = QtGui.QSplashScreen(pixmap,
            QtCore.Qt.FramelessWindowHint|QtCore.Qt.WindowStaysOnTopHint)
    splash.show()
    alphorn = QtGui.QSound(r'/resources/alph_3.m4a')
    alphorn.play()
    time.sleep(.2)
    splash.close()
    
    riskWin = RiskGUI()    
    riskWin.show()
    app.setActiveWindow(riskWin)
    riskWin.start_newgame()
   
    sys.exit(app.exec_())