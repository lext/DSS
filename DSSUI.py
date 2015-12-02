from pyqtgraph.Qt import QtGui, QtCore
from PyQt4.QtCore import pyqtSignal
import numpy as np
import pyqtgraph as pg
from MassiveDataCurve import *

pg.setConfigOption('background', 'w')
pg.setConfigOptions(antialias=True)
from scipy.signal import hamming
import sqlite3
from array import array

class DSSUI(QtGui.QMainWindow):

    def __init__(self):
        super(DSSUI, self).__init__()
        self.build_gui()

        self.connect(self.pbOpen, QtCore.SIGNAL('clicked()'), self.open_signal_slot)
        self.connect(self.pbSave, QtCore.SIGNAL('clicked()'), self.save_segments_slot)
        self.connect(self.pbAdd, QtCore.SIGNAL('clicked()'), self.add_segment_slot)
        self.connect(self.pbRem, QtCore.SIGNAL('clicked()'), self.rem_segment_slot)

        self._x = None
        self._dt = None
        self._t = None

    def build_gui(self):
        self.setWindowTitle('Digital signal segmentation tool')
        centralwidget = QtGui.QWidget()
        self.pbOpen = QtGui.QPushButton("Open signal")
        self.pbSave = QtGui.QPushButton("Save results")
        self.pbAdd = QtGui.QPushButton("Add segment")
        self.pbRem = QtGui.QPushButton("Remove segment")
        self.lSegments = QtGui.QLabel("Segments")
        # ListView of segments
        self.lwSegments = QtGui.QListView()
        #Signal
        self.p1 = pg.PlotWidget()
        # Details of a segment
        self.p2 = pg.PlotWidget()
        self._signal_curve = MassiveDataCurve()
        self.p1.addItem(self._signal_curve)
        self._fragment_curve = MassiveDataCurve()
        self.p2.addItem(self._fragment_curve)
        self.p1.setMouseEnabled(x=True, y=False)
        self.p2.setMouseEnabled(x=False, y=False)
        self.p1.showGrid(x=True, y=True)
        self.p2.showGrid(x=True, y=True)

        # axis
        self.p1.getAxis('left').setPen((0,0,0))
        self.p1.getAxis('bottom').setPen((0,0,0))
        self.p1.getAxis('left').setLabel('Amplitude', units='V')
        self.p1.getAxis('bottom').setLabel('Time [ms]')

        self.p2.getAxis('left').setPen((0,0,0))
        self.p2.getAxis('bottom').setPen((0,0,0))
        self.p2.getAxis('left').setLabel('Amplitude', units='V')
        self.p2.getAxis('bottom').setLabel('Time [ms]')

        # Layouts
        self.l1 = QtGui.QHBoxLayout(centralwidget)
        self.l11 = QtGui.QVBoxLayout()
        self.l1.addLayout(self.l11)
        self.l11.addWidget(self.p1)
        self.l11.addWidget(self.p2)

        self.l12 = QtGui.QVBoxLayout()
        self.l1.addLayout(self.l12)
        self.l12.addWidget(self.pbOpen)
        self.l12.addWidget(self.pbSave)
        self.l12.addWidget(self.pbRem)
        self.l12.addWidget(self.pbAdd)
        self.l12.addWidget(self.lSegments)
        self.l12.addWidget(self.lwSegments)

        # Size policies
        self.lwSegments.setSizePolicy(QtGui.QSizePolicy.Fixed,\
        QtGui.QSizePolicy.Expanding)

        self.p1.setSizePolicy(QtGui.QSizePolicy.Expanding,\
        QtGui.QSizePolicy.Preferred)

        self.p2.setSizePolicy(QtGui.QSizePolicy.Expanding,\
        QtGui.QSizePolicy.Preferred)

        self.lSegments.setSizePolicy(QtGui.QSizePolicy.Minimum,\
        QtGui.QSizePolicy.Minimum)

        self.lwSegments.setMaximumWidth(150)
        self.setMinimumWidth(800)
        self.setMinimumHeight(500)
        # Setting central widget
        self.setCentralWidget(centralwidget)

        # segments
        self.segments = []

    def get_selection(self):
        l, r = self.lr.getRegion()
        l_ind = int(l/self._dt)
        r_ind = int(r/self._dt)
        return (l_ind, r_ind)

    def update_plot(self):
        x = self._x
        dt = self._dt

        self._signal_curve.setSignalData(x, dt)
        self.p1.getAxis('bottom').setScale(dt*x.shape[0]/self._signal_curve.x.shape[0])
        #self.lr.setBounds([t.min(), t.max()])
        #self.lr.setRegion([t.min(), t.max()])



    def open_signal_slot(self):
        # Getting a filename from the dialog
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open signal')
        if not filename:
            return
        # Getting sampling frequency
        sf, state = QtGui.QInputDialog.getInt(self, 'Enter sampling frequency', "SF:", 500)
        if not state:
            return
        # Loading signal to the memory
        self._x = np.load(str(filename))
        self._dt = 1/float(sf)

        self.update_plot()

    def save_segments_slot(self):
        print "Save"

    def add_segment_slot(self):
        # Region selector
        lr = pg.LinearRegionItem()
        self.p1.addItem(lr)

        vb = self._signal_curve.getViewBox()
        vbrange = vb.viewRange()[0]
        l = vbrange[0]+int(vbrange[1]-vbrange[0])*0.07
        r = vbrange[1]-int(vbrange[1]-vbrange[0])*0.07

        lr.setBounds([0, self._x.shape[0]])
        lr.sigRegionChangeFinished.connect(self.region_changed)
        lr.setRegion([l, r])

        self.segments.append(lr)

    def region_changed(self, lr):
        dt = self._dt
        x = self._x
        curve_len = self._signal_curve.x.shape[0]

        l, r = lr.getRegion()
        l_t = l*dt*x.shape[0]/curve_len
        r_t = r*dt*x.shape[0]/curve_len
        print l_t, r_t
    def rem_segment_slot(self):
        print "Remove"

