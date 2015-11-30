import pyqtgraph as pg
import numpy as np
import pywt

class MassiveDataCurve(pg.PlotCurveItem):
    """
    Massive data curve class based on the DWT compression
    
    """
    def __init__(self, *args, **kwds):
        super(MassiveDataCurve, self).__init__(*args, **kwds)
        self.limit = 400000 # maximum number of samples to be plotted
        self.x = None
        self.dt = None
        
        
        
    def setSignalData(self, x, dt):
        cA3, cD3, cD2, cD1 = pywt.wavedec(x, "db4", level=3)
        self.x = cA3
        self.dt = dt
        self.updatePlot()
        
    def viewRangeChanged(self):
        self.updatePlot()
        
    def updatePlot(self):
        if self.x is None:
            self.setData([])
            return
        vb = self.getViewBox()
        if vb is None:
            return  # no ViewBox yet
        # Determining limits
        vbrange = vb.viewRange()[0]
        start = max(0,int(vbrange[0])-1)
        stop = min(self.x.shape, int(vbrange[1]+2))
        

        self.setData(self.x[start:stop], pen='b') # update the plot
        self.setPos(start, 0) # shift to match starting index
        self.resetTransform()
        self.getViewBox().setLimits(xMin=0, maxXRange=self.limit)
