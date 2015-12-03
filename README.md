# DSS

DSS (digital signal segmentation) - a tool developed for a manual segmentation of "heavy signals". I have developed this program to do a segmentation of signals, which have 500 kHz sampling frequency and length about at least 100 seconds. 
To reduce number of points for visualization, I used 3rd-level approximation coefficients of DWT with Daubechy wavelets of the 4th order.

The program takes as and input *.npy files and saves the results to a text file.

The software was developed using python 2.7, and has the following dependencies:
* PyQt
* pyqtgraph
* numpy
* pywavelets
