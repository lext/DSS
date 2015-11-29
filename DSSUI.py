from pyqtgraph.Qt import QtGui, QtCore
from PyQt4.QtCore import pyqtSignal
import numpy as np
import pyqtgraph as pg
pg.setConfigOptions(antialias=True)
pg.setConfigOption('background', 'w')
from scipy.signal import hamming
import sqlite3
from array import array

class DSSUI(QtGui.QMainWindow):

    def __init__(self):
        super(DSSUI, self).__init__()
        self.build_gui()

    def build_gui(self):
        self.setWindowTitle('Digital signal segmentation tool')
        centralwidget = QtGui.QWidget()
        self.openPB = QtGui.QPushButton("Open signal")
        self.savePB = QtGui.QPushButton("Save results")
        self.addPB = QtGui.QPushButton("Add segment")
        self.remPB = QtGui.QPushButton("Remove segment")
        self.segmentsL = QtGui.QLabel("Segments")

        self.segmentsLW = QtGui.QListView()
        #Signal
        self.p1 = pg.PlotWidget()
        # Details of a segment
        self.p2 = pg.PlotWidget()

        self.p1.setMouseEnabled(x=True, y=False)
        self.p2.setMouseEnabled(x=False, y=False)
        self.p1.showGrid(x=True, y=True)
        self.p2.showGrid(x=True, y=True)
        # Region selector
        self.lr = pg.LinearRegionItem()
        self.p1.addItem(self.lr)
        # axis
        self.p1.getAxis('left').setPen((0,0,0))
        self.p1.getAxis('bottom').setPen((0,0,0))
        self.p2.getAxis('left').setPen((0,0,0))
        self.p2.getAxis('bottom').setPen((0,0,0))

        # Layouts
        self.l1 = QtGui.QHBoxLayout(centralwidget)
        self.l11 = QtGui.QVBoxLayout()
        self.l1.addLayout(self.l11)
        self.l11.addWidget(self.p1)
        self.l11.addWidget(self.p2)

        self.l12 = QtGui.QVBoxLayout()
        self.l1.addLayout(self.l12)
        self.l12.addWidget(self.openPB)
        self.l12.addWidget(self.savePB)
        self.l12.addWidget(self.remPB)
        self.l12.addWidget(self.addPB)
        self.l12.addWidget(self.segmentsL)
        self.l12.addWidget(self.segmentsLW)

        # Size policies
        self.segmentsLW.setSizePolicy(QtGui.QSizePolicy.Fixed,\
        QtGui.QSizePolicy.Expanding)

        self.p1.setSizePolicy(QtGui.QSizePolicy.Expanding,\
        QtGui.QSizePolicy.Preferred)

        self.p2.setSizePolicy(QtGui.QSizePolicy.Expanding,\
        QtGui.QSizePolicy.Preferred)

        self.segmentsL.setSizePolicy(QtGui.QSizePolicy.Minimum,\
        QtGui.QSizePolicy.Minimum)

        self.segmentsLW.setMaximumWidth(150)
        self.setMinimumWidth(800)
        self.setMinimumHeight(500)
        # Setting central widget
        self.setCentralWidget(centralwidget)

    def get_selection(self):
        l, r = region = self.lr.getRegion()
        l_ind = int(l/self._dt)
        r_ind = int(r/self._dt)
        return (l_ind, r_ind)

