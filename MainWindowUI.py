# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindowUI.ui'
#
# Created: Sun Jun  9 13:01:09 2013
#      by: pyside-uic 0.2.13 running on PySide 1.1.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.NationStatusTable = QtGui.QTableView(self.centralwidget)
        self.NationStatusTable.setGeometry(QtCore.QRect(625, 20, 161, 201))
        self.NationStatusTable.setObjectName("NationStatusTable")
        self.VoronoiPlot = VoronoiPlotWidget(self.centralwidget)
        self.VoronoiPlot.setGeometry(QtCore.QRect(10, 10, 601, 511))
        self.VoronoiPlot.setObjectName("VoronoiPlot")
        self.BattleTable = QtGui.QTableWidget(self.centralwidget)
        self.BattleTable.setGeometry(QtCore.QRect(625, 240, 161, 192))
        self.BattleTable.setObjectName("BattleTable")
        self.BattleTable.setColumnCount(0)
        self.BattleTable.setRowCount(0)
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(630, 0, 91, 16))
        self.label.setObjectName("label")
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(630, 220, 91, 16))
        self.label_2.setObjectName("label_2")
        self.NextButton = QtGui.QPushButton(self.centralwidget)
        self.NextButton.setGeometry(QtCore.QRect(650, 510, 114, 32))
        self.NextButton.setObjectName("NextButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar()
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Nations Status", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Battle Results", None, QtGui.QApplication.UnicodeUTF8))
        self.NextButton.setText(QtGui.QApplication.translate("MainWindow", "Next Turn", None, QtGui.QApplication.UnicodeUTF8))

from voronoiplotwidget import VoronoiPlotWidget
