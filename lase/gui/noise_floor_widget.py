# -*- coding: utf-8 -*-

from pyqtgraph.Qt import QtGui
import numpy as np

class NoiseFloorWidget(QtGui.QWidget):

    def __init__(self, driver):
        super(NoiseFloorWidget, self).__init__()
        
        self.driver = driver      
        self.noise_floor = np.zeros(self.driver.sampling.n)
        self.layout = QtGui.QVBoxLayout()    
        self.window_layout = QtGui.QVBoxLayout()
  
        
        self.calibrate_button = QtGui.QPushButton('Calibrate')        
        self.calibrate_button.setStyleSheet('QPushButton {color: orange;}')
        
        self.window = []
        self.window.append(QtGui.QRadioButton('Rectangular'))
        self.window.append(QtGui.QRadioButton('Hanning'))
        self.window.append(QtGui.QRadioButton('Hamming'))
        self.window.append(QtGui.QRadioButton('Blackman'))
        for item in self.window:
            self.window_layout.addWidget(item)
       
       
        self.window_box = QtGui.QGroupBox("Window")
        self.window_box.setLayout(self.window_layout)
        
        self.layout.addWidget(self.calibrate_button)
        self.layout.addWidget(self.window_box)
        self.setLayout(self.layout)
        
        # Connections
        
        self.calibrate_button.clicked.connect(self.calibrate)
        self.window[0].toggled.connect(lambda: self.change_window('Rectangular'))
        self.window[1].toggled.connect(lambda: self.change_window('Hanning'))
        self.window[2].toggled.connect(lambda: self.change_window('Hamming'))
        self.window[3].toggled.connect(lambda: self.change_window('Blackman'))
        
        self.window[1].setChecked(True)
        
    def calibrate(self):
        self.noise_floor = np.zeros(self.driver.sampling.n)
        for i in range(100):
            self.driver.get_spectrum()
            self.noise_floor += self.driver.spectrum
        self.noise_floor /= 100
        
    def change_window(self, window):
        n = self.driver.sampling.n # Number of points in the waveform
        if window == 'Rectangular':
            self.driver.demod[0,:] = 0.5
        elif window == 'Hanning':
            self.driver.demod[0,:] = 0.49 * (1-np.cos(2*np.pi*np.arange(n)/n))
        elif window == 'Hamming':
            self.driver.demod[0,:] = 0.53836 * (0.46164-np.cos(2*np.pi*np.arange(n)/n))
        elif window == 'Blackman':
            self.driver.demod[0,:] = 0.42659-0.42659*np.cos(2*np.pi*np.arange(n)/n) + \
                                     0.076849*np.cos(4*np.pi*np.arange(n)/n)
        self.driver.set_demod()
        
        
    
