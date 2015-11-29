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
 
		#Signal
		self.p1 = pg.PlotWidget()
		# Details of a segment
		self.p2 = pg.PlotWidget()
		self.p1.setMouseEnabled(x=True, y=False)
		self.p2.setMouseEnabled(x=False, y=False)
		self.p1.showGrid(x=True, y=True)
		self.p2.showGrid(x=True, y=True)
		#self.lr = pg.LinearRegionItem()
		#self.p1.addItem(self.lr)
		# axis
		self.p1.getAxis('left').setPen((0,0,0))
		self.p1.getAxis('bottom').setPen((0,0,0))
		self.p2.getAxis('left').setPen((0,0,0))
		self.p2.getAxis('bottom').setPen((0,0,0))

		self.dbb = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Apply | QtGui.QDialogButtonBox.Close)
		self.dbb.setOrientation(QtCore.Qt.Vertical)


		self.l1 = QtGui.QHBoxLayout(centralwidget)
		self.l11 = QtGui.QVBoxLayout()
		self.l1.addLayout(self.l11)
		self.l12 = QtGui.QVBoxLayout()
		self.l1.addLayout(self.l12)
		self.l11.addWidget(self.p1)
		self.l11.addWidget(self.p2)
		self.l12.addStretch(1)

		self.setCentralWidget(centralwidget)

