# -*- coding: utf-8 -*-

from pyqtgraph.Qt import QtGui, QtCore
import numpy as np

class MathWidget(QtGui.QWidget):

    def __init__(self, driver, plot_widget):
        super(MathWidget, self).__init__()
        
        self.driver = driver
        self.plot_widget = plot_widget
        
        self.n_avg_spectrum = 1
        self.correction  = False
        self.fourier  = False

        self.layout = QtGui.QVBoxLayout()
        self.checkbox_layout = QtGui.QHBoxLayout()
        self.avg_layout = QtGui.QHBoxLayout()
        
        # Correction
        self.correction_checkbox = QtGui.QCheckBox('Correction', self)
        self.correction_checkbox.setCheckState(QtCore.Qt.Unchecked)

        # Plot Fourier Transform
        self.fourier_checkbox = QtGui.QCheckBox('Fourier Transform', self)
        self.fourier_checkbox.setCheckState(QtCore.Qt.Unchecked)
        
        # Select avg
        self.n_avg_label = QtGui.QLabel()  
        self.n_avg_label.setText('N avg')        
        self.avg_spin = QtGui.QSpinBox()
        self.avg_spin.setMaximum(50)        
        self.avg_spin.setMinimum(1)
        self.avg_spin.setValue(1)
        
        # Average on 
        self.avg_on_button = QtGui.QPushButton()
        self.avg_on_button.setStyleSheet('QPushButton {color: green;}')
        self.avg_on_button.setText('Start averaging')
        self.avg_on_button.setCheckable(True)
        
        # Set layout
        
        self.layout.addWidget(self.avg_on_button)
        self.checkbox_layout.addStretch(1)
        self.checkbox_layout.addWidget(self.fourier_checkbox)
        self.checkbox_layout.addStretch(1)
        self.checkbox_layout.addWidget(self.correction_checkbox)
        self.checkbox_layout.addStretch(1)
        self.layout.addLayout(self.checkbox_layout)
        
        self.avg_widget = QtGui.QWidget()
        self.avg_layout.addWidget(self.n_avg_label)
        self.avg_layout.addWidget(self.avg_spin)
        self.avg_layout.addStretch(1)
        self.avg_widget.setLayout(self.avg_layout)
        
        self.layout.addWidget(self.avg_widget)
        self.avg_widget.setVisible(False)
        
        
        self.setLayout(self.layout)
        
        self.avg_on_button.clicked.connect(self.change_averaging)  
        self.correction_checkbox.stateChanged.connect(self.correction_connect)  
        self.fourier_checkbox.stateChanged.connect(self.fourier_connect)           
        self.avg_spin.valueChanged.connect(self.avg_connect)        
        
        
    def change_averaging(self):
        self.driver.avg_on = not self.driver.avg_on    
        if self.driver.avg_on:
            self.avg_on_button.setStyleSheet('QPushButton {color: red;}')
            self.avg_on_button.setText('Stop averaging')
        else:
            self.avg_on_button.setStyleSheet('QPushButton {color: green;}')
            self.avg_on_button.setText('Start averaging')
        self.driver.set_averaging(self.driver.avg_on)

    def correction_connect(self, state):
        if state == QtCore.Qt.Checked:
            self.correction = True
            self.driver.ideal_amplitude_waveform = 1167 * self.driver.optical_power[0] / self.driver.power[0] * self.driver.dac[1]
            self.driver.amplitude_error = self.driver.ideal_amplitude_waveform
            self.driver.dac[1,:] = self.driver.get_correction()
        else:
            self.correction = False  

    def fourier_connect(self, state):
        if state == QtCore.Qt.Checked:    
            self.plot_widget.getPlotItem().getAxis('bottom').setLabel('Frequency (MHz)')
            self.plot_widget.getPlotItem().getAxis('left').setLabel('Spectrum power')
            self.fourier = True
            self.plot_widget.enableAutoRange()
            self.avg_widget.setVisible(True)
        else:    
            self.plot_widget.getPlotItem().getAxis('bottom').setLabel('Time (us)')
            self.plot_widget.getPlotItem().getAxis('left').setLabel('Optical power (u.a.)')
            self.fourier = False
            self.plot_widget.enableAutoRange()
            self.avg_widget.setVisible(False)
            
    def avg_connect(self, val):
        self.n_avg_spectrum = self.avg_spin.value()