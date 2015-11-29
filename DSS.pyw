#! /usr/bin/env python3
#
import sys
from PyQt4 import QtCore, QtGui
import DSSUI

def main():
	app = QtGui.QApplication(sys.argv)
	app.setApplicationName('EGEGrouper')
	form = DSSUI.DSSUI()
	form.showMaximized()
	app.exec()

if __name__ == "__main__":
	sys.exit(main())
