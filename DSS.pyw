#! /usr/bin/env python2
#
import sys
from PyQt4 import QtCore, QtGui
import DSSUI

def main():
	app = QtGui.QApplication(sys.argv)
	app.setApplicationName('Digital Signal Segmenter')
	form = DSSUI.DSSUI()
	form.showMaximized()
	app.exec_()

if __name__ == "__main__":
	sys.exit(main())
