# DSS

DSS (digital signal segmentation) - is a tool which I use for segmentation of high-frequency signals (sampling freq. 500 kHz) in my doctoral dissertation.

The program takes as and input a raw binary file with floats in lettle-endian format. As a result it produces a text file with a suffix *_segm.txt* in the same folder where the input file is located.

The software was developed using python 2.7, and has the following dependencies:
* PyQt
* pyqtgraph
* numpy
* pywavelets
