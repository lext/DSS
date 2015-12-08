from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
from MassiveDataCurve import *
import os

pg.setConfigOption('background', 'w')
pg.setConfigOptions(antialias=True)

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
        self.pbSave.setEnabled(False)
        self.pbAdd.setEnabled(False)
        self.pbRem.setEnabled(False)

        # Plot widget and Massive Curve Initializtion
        self.p1 = pg.PlotWidget()
        # Details of a segment
        self.p1.setMouseEnabled(x=True, y=False)
        self.p1.showGrid(x=True, y=True)

        # axis
        self.p1.getAxis('left').setPen((0,0,0))
        self.p1.getAxis('bottom').setPen((0,0,0))
        self.p1.getAxis('left').setLabel('Amplitude', units='V')
        self.p1.getAxis('bottom').setLabel('Time [ms]')

        # Layouts
        self.l1 = QtGui.QHBoxLayout(centralwidget)
        self.l11 = QtGui.QVBoxLayout()
        self.l1.addLayout(self.l11)
        self.l11.addWidget(self.p1)

        self.l12 = QtGui.QVBoxLayout()
        self.l1.addLayout(self.l12)
        self.l12.addWidget(self.pbOpen)
        self.l12.addWidget(self.pbSave)
        self.l12.addWidget(self.pbAdd)
        self.l12.addWidget(self.pbRem)
        self.l12.addStretch(1)
        # Size policies

        self.p1.setSizePolicy(QtGui.QSizePolicy.Expanding,\
        QtGui.QSizePolicy.Preferred)

        self.setMinimumWidth(800)
        self.setMinimumHeight(500)
        # Setting central widget
        self.setCentralWidget(centralwidget)

        # segments
        self.segments = []
        self.filename = ""

    def update_plot(self):
        x = self._x
        dt = self._dt
        self._signal_curve.setSignalData(x, dt)
        self.p1.getAxis('bottom').setScale(dt*x.shape[0]/self._signal_curve.x.shape[0])



    def open_signal_slot(self):
        # Getting a filename from the dialog
        if not self.filename:
            filename = QtGui.QFileDialog.getOpenFileName(self, 'Open signal')
        else:
            dirname = os.path.dirname(self.filename)
            filename = QtGui.QFileDialog.getOpenFileName(self, 'Open signal', directory=dirname)
        if not filename:
            return
        # Getting sampling frequency
        sf, state = QtGui.QInputDialog.getInt(self, 'Enter sampling frequency', "SF:", 500)
        if not state:
            return
        self.filename = str(filename)
        # Loading signal to the memory
        self.p1.clear()
        self._signal_curve = MassiveDataCurve()
        self.p1.addItem(self._signal_curve)
        self._x = np.fromfile(self.filename, dtype="<f")
        self._dt = 1/float(sf)
        self.update_plot()
        self.segments = []
        if os.path.isfile(self.filename[:-4]+"_segm.txt"):
            with open(self.filename[:-4]+"_segm.txt", "r") as f:
                for line in f:
                    l_t, r_t = map(float, line.split())
                    lr = pg.LinearRegionItem()
                    self.p1.addItem(lr)
                    self.segments.append(lr)
                    curve_len = self._signal_curve.x.shape[0]
                    l = l_t/(self._dt*self._x.shape[0]/curve_len)
                    r = r_t/(self._dt*self._x.shape[0]/curve_len)
                    lr.setBounds([0, self._x.shape[0]])
                    lr.setRegion([l, r])
        vb = self._signal_curve.getViewBox()
        vb.disableAutoRange()
        self.p1.setYRange(-0.3, 0.3,padding=0)
        self.p1.setXRange(0, self._signal_curve.limit,padding=0)
        self.pbSave.setEnabled(True)
        self.pbAdd.setEnabled(True)
        self.pbRem.setEnabled(True)
        self.setWindowTitle(self.filename)

    def save_segments_slot(self):
        with open(self.filename[:-4]+"_segm.txt", "w") as f:
            for lr in sorted(self.segments, key=lambda x:self.get_region(x)[0]):
                l, r = self.get_region(lr)
                f.write("{0} {1}\n".format(l, r))


    def add_segment_slot(self):
        # Region selector
        lr = pg.LinearRegionItem()
        self.p1.addItem(lr)

        vb = self._signal_curve.getViewBox()
        vbrange = vb.viewRange()[0]
        l = vbrange[0]+int(vbrange[1]-vbrange[0])*0.05
        r = vbrange[1]-int(vbrange[1]-vbrange[0])*0.05

        lr.setBounds([0, self._x.shape[0]])
        lr.setRegion([l, r])

        self.segments.append(lr)

    def get_region(self, lr):
        dt = self._dt
        x = self._x
        curve_len = self._signal_curve.x.shape[0]

        l, r = lr.getRegion()
        l_t = l*dt*x.shape[0]/curve_len
        r_t = r*dt*x.shape[0]/curve_len
        return l_t, r_t

    def rem_segment_slot(self):
        mb = QtGui.QMessageBox(self)
        mb.setText("Not implemented!")
        mb.exec_()

