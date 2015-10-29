# -*- coding: utf-8 -*-

from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import glob, os

class CalibrationWidget(QtGui.QWidget):

    def __init__(self, driver, data_path=None):
        super(CalibrationWidget, self).__init__()
        
        self.driver = driver
        self.data_path = data_path    
        
        self.layout = QtGui.QVBoxLayout()     
        self.adc_offset_layout = QtGui.QHBoxLayout() 
        self.calibration_layout = QtGui.QHBoxLayout()   
        self.calibration_list_layout = QtGui.QVBoxLayout()      
        
        self.transfer_layout = QtGui.QVBoxLayout() 
        self.transfer_list_layout = QtGui.QHBoxLayout()         
        self.get_transfer_layout = QtGui.QVBoxLayout()    
        self.save_transfer_layout = QtGui.QHBoxLayout()  
        self.load_transfer_layout = QtGui.QHBoxLayout()      
        
        self.adc_offset_box = QtGui.QGroupBox("ADC offset")        
        self.calibration_box = QtGui.QGroupBox("Optical calibration")
        self.transfer_box = QtGui.QGroupBox("Transfer function")
        
        # Calibration 
        
        self.adc_offset_button = QtGui.QPushButton('Calibrate')        
        self.adc_offset_button.setStyleSheet('QPushButton {color: orange;}')
        
        self.calibration_button = []
        self.calibration_line = []
        self.calibration_label = []
        
        self.calibration_list = []
        self.calibration_list.append(QtGui.QRadioButton('ADC 1'))
        self.calibration_list.append(QtGui.QRadioButton('ADC 2'))
        for item in self.calibration_list:
            self.calibration_list_layout.addWidget(item)
            
        self.calibration_list[0].setChecked(True)
        
        self.calibration_button = (QtGui.QPushButton('Calibrate'))     
        self.calibration_button.setStyleSheet('QPushButton {color: orange;}')        
        self.calibration_line = (QtGui.QLineEdit(self))              
        self.calibration_label = (QtGui.QLabel('mW'))
        
        self.transfer_button = QtGui.QPushButton('Get transfer function')        
        self.transfer_button.setStyleSheet('QPushButton {color: orange;}')
        
        
        self.transfer_list = []
        self.transfer_list.append(QtGui.QRadioButton('DAC 1'))
        self.transfer_list.append(QtGui.QRadioButton('DAC 2'))
        for item in self.transfer_list:
            self.transfer_list_layout.addStretch(1)
            self.transfer_list_layout.addWidget(item)
        
        self.transfer_list_layout.addStretch(1)
        self.transfer_list[0].setChecked(True)
        
        self.adc_offset_layout.addWidget(self.adc_offset_button)
        self.adc_offset_box.setLayout(self.adc_offset_layout)
        
        
        self.save_line = QtGui.QLineEdit(self)
        self.save_button = QtGui.QPushButton(self)
        self.save_button.setText('Save')
        
        self.load_combo = QtGui.QComboBox(self)         
        self.load_combo.addItem('') 
        for file in glob.glob(os.path.join(self.data_path,'*_transfer_function.csv')): 
            [filepath, filename] = os.path.split(file)               
            self.load_combo.addItem(str(filename).replace('_transfer_function.csv',''))
        self.load_button = QtGui.QPushButton()
        self.load_button.setText('Load')
        
        
        self.calibration_layout.addLayout(self.calibration_list_layout)
        self.calibration_layout.addWidget(self.calibration_line)
        self.calibration_layout.addWidget(self.calibration_label)
        self.calibration_layout.addWidget(self.calibration_button)   
        
        self.calibration_box.setLayout(self.calibration_layout)       
        
        
        self.get_transfer_layout.addLayout(self.transfer_list_layout)
        self.get_transfer_layout.addWidget(self.transfer_button)               
        
        self.transfer_layout.addLayout(self.get_transfer_layout)
        
        self.save_transfer_layout.addWidget(self.save_line, 1)
        self.save_transfer_layout.addWidget(self.save_button)
        self.load_transfer_layout.addWidget(self.load_combo, 1)   
        self.load_transfer_layout.addWidget(self.load_button)        
       
       
        self.transfer_layout.addLayout(self.save_transfer_layout)
        self.transfer_layout.addLayout(self.load_transfer_layout)
        self.transfer_box.setLayout(self.transfer_layout)
        
        self.calibration_button.clicked.connect(self.optical_calibration)
        
        self.save_button.clicked.connect(self.save)
        self.load_button.clicked.connect(self.load)
        
        self.layout.addWidget(self.adc_offset_box)
        self.layout.addWidget(self.calibration_box)        
        self.layout.addWidget(self.transfer_box)       
        self.layout.addStretch(1)
        
        self.setLayout(self.layout)
        
        # Connections
        self.adc_offset_button.clicked.connect(self.adc_offset)
        self.transfer_button.clicked.connect(self.get_amplitude_transfer_function)
              
        
    def optical_calibration(self, index):
        if self.calibration_list[0].isChecked():
            index = 0
        else:
            index = 1
        if self.calibration_line.text() == '' :
            return
        else :
            self.driver.optical_power[index] *= float(self.calibration_line.text())
            self.driver.power[index] *= np.mean(self.driver.adc[index,:])
            self.calibration_line.setText('')


    def adc_offset(self):
        self.driver.get_adc()
        self.driver.adc_offset[0] += np.mean(self.driver.adc[0,:])   
        self.driver.adc_offset[1] += np.mean(self.driver.adc[1,:])    
            
    def get_amplitude_transfer_function(self):
        if self.transfer_list[0].isChecked():
            channel_dac = 0
        else:
            channel_dac = 1
        self.driver.get_amplitude_transfer_function(channel_dac)
        
    def save(self):
        if self.save_line.text() =='' :
            return
        else:            
            data = np.zeros((2,self.driver.n))
            data[0,:] = np.abs(self.driver.amplitude_transfer_function)
            data[1,:] = np.angle(self.driver.amplitude_transfer_function)
            np.savetxt(os.path.join(self.data_path, str(self.save_line.text()) + '_transfer_function' + '.csv'),\
                np.transpose(data[:,1:]), delimiter=',', header='gain, phase')            
            self.load_combo.addItem(str(self.save_line.text()))
            self.save_line.setText('')
            
    def load(self):
        if self.load_combo.currentText() == '':
            return
        else:
            data = np.zeros((2,self.driver.n))
            data[:,0] = 1
            data[:,1:] = np.transpose(np.loadtxt(os.path.join(self.data_path, str(self.load_combo.currentText()) + '_transfer_function' + '.csv'),\
                skiprows=1, delimiter=','))
            self.driver.set_amplitude_transfer_function(data[0,:] * np.exp(1j*data[1,:]))
            self.load_combo.setCurrentIndex(0)

