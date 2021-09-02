# ESPI Project

Capture images from basler camera and perform consecutive differencing in real time. Intended for use with ESPI setup in CAML Lab at McGill University.

## Description

ESPI stands for Electronic Speckle Pattern Interferometry and is a method that can be used to visualize mode shapes of a vibrating object.

The ESPI system used in the CAML lab was designed by Thomas R. Moore.

Basler Camera model used in CAML lab: a2A3840-45ucBAS 

### Requirements

* Install pylon : https://www.baslerweb.com/en/products/software/basler-pylon-camera-software-suite/
* Install pypylon using the following command (pip info: https://pip.pypa.io/en/stable/): pip3 install pypylon
* Install opencv using the following command: pip install opencv-python
* Install Tkinter using the following command: pip install tk


### Installing

* Download the ESPIFINAL folder to your computer, make sure you note the path to this folder.

### Executing program

* Run the espifinal file in a terminal of your choice using the following command: python3 *path to the espifinal.py file* (ex: python3 C:\Users\calli\Documents\ESPIFINAL\espifinal.py)
* A window will appear with three options: live view, consecutive differencing(in black and white), and consecutive differencing (in color) choose which one applies to you
* Then two more windows will appear. One is the consecutive differencing or live view and the other is control over the different parameters
* Once done, click the esc key to terminate the program


## Authors

Callie Valenzisi 
callie.valenzisi@mail.mcgill.ca

## Acknowledgments

Inspiration, code snippets, etc.
* [Inspiration](https://github.com/drscotthawley/image-capture-opencv)
* [Tkinter Tutorial](https://www.python-course.eu/python_tkinter.php)
* [Single Capture Code](https://github.com/basler/pypylon/blob/master/samples/opencv.py)
