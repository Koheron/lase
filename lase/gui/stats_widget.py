# -*- coding: utf-8 -*-

from pyqtgraph.Qt import QtGui, QtCore
import numpy as np

class StatsWidget(QtGui.QWidget):

    def __init__(self, driver):
        super(StatsWidget, self).__init__()
        
        self.driver = driver       
        
        self.layout = QtGui.QHBoxLayout()
        
        # Measures 
        ## Name
        self.mean_label = QtGui.QLabel('Average')        
        self.amp_label = QtGui.QLabel('Amplitude') 
        self.mean_label.setAlignment(QtCore.Qt.AlignCenter)
        self.amp_label.setAlignment(QtCore.Qt.AlignCenter)       
        
        ## adc_1
        self.mean_1_label = QtGui.QLabel('')        
        self.amp_1_label= QtGui.QLabel('')        
        self.mean_1_label.setAlignment(QtCore.Qt.AlignCenter)
        self.amp_1_label.setAlignment(QtCore.Qt.AlignCenter) 
        ## adc_2
        self.mean_2_label = QtGui.QLabel('')        
        self.amp_2_label = QtGui.QLabel('')
        self.mean_2_label.setAlignment(QtCore.Qt.AlignCenter)
        self.amp_2_label.setAlignment(QtCore.Qt.AlignCenter) 
        
        self.measures_box = QtGui.QGroupBox('Measures')
        self.measures_box.setAlignment(5)
        self.adc_1_box = QtGui.QGroupBox('ADC 1')
        self.adc_1_box.setAlignment(5)
        self.adc_2_box = QtGui.QGroupBox('ADC 2')
        self.adc_2_box.setAlignment(5)
        
        self.name_layout = QtGui.QVBoxLayout()
        
        self.name_layout.addWidget(self.mean_label)
        self.name_layout.addWidget(self.amp_label)
        self.measures_box.setLayout(self.name_layout)
        
        self.adc_1_layout = QtGui.QVBoxLayout()
        self.adc_2_layout = QtGui.QVBoxLayout()
       
        self.adc_1_layout.addWidget(self.mean_1_label)
        self.adc_1_layout.addWidget(self.amp_1_label)
        self.adc_1_box.setLayout(self.adc_1_layout)
        
        self.adc_2_layout.addWidget(self.mean_2_label)
        self.adc_2_layout.addWidget(self.amp_2_label)
        self.adc_2_box.setLayout(self.adc_2_layout)
        
        self.layout.addWidget(self.measures_box)
        self.layout.addWidget(self.adc_1_box)
        self.layout.addWidget(self.adc_2_box)
        

    def update(self):
        if 1e-2 < np.abs(np.mean(self.driver.adc[0,:])) < 1e3:
            self.mean_1_label.setText('{:.2f}'.format(np.mean(self.driver.adc[0,:])))
        else:
            self.mean_1_label.setText('%.2e'%(np.mean(self.driver.adc[0,:])))
        if 1e-2 < np.abs(np.mean(self.driver.adc[1,:])) < 1e3:
            self.mean_2_label.setText('{:.2f}'.format(np.mean(self.driver.adc[1,:])))
        else:
            self.mean_2_label.setText('%.2e'%(np.mean(self.driver.adc[1,:])))
        if 1e-2 < np.abs(np.max(self.driver.adc[0,:])-np.min(self.driver.adc[0,:])) < 1e3:
            self.amp_1_label.setText('{:.2f}'.format(np.max(self.driver.adc[0,:])-np.min(self.driver.adc[0,:])))
        else:        
            self.amp_1_label.setText('%.2e'%(np.max(self.driver.adc[0,:])-np.min(self.driver.adc[0,:])))
        if 1e-2 < np.abs(np.max(self.driver.adc[1,:])-np.min(self.driver.adc[1,:])) < 1e3:
            self.amp_2_label.setText('{:.2f}'.format(np.max(self.driver.adc[1,:])-np.min(self.driver.adc[1,:])))
        else:            
            self.amp_2_label.setText('%.2e'%(np.max(self.driver.adc[1,:])-np.min(self.driver.adc[1,:])))
