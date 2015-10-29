# -*- coding: utf-8 -*-

from pyqtgraph.Qt import QtGui
from koheron_slider import KoheronSlider
from PyQt4.QtCore import SIGNAL, pyqtSignal
import numpy as np
from scipy import signal

class WaveformList(QtGui.QWidget):
    def __init__(self, items = ['Sine', 'Triangle', 'Square']):
        super(WaveformList, self).__init__()
        layout = QtGui.QVBoxLayout()
        self.items = items
        self.list = []
        for item in self.items:
            self.list.append(QtGui.QRadioButton(item))
        for item in self.list:
            layout.addWidget(item)
        self.list[0].setChecked(True)
        self.setLayout(layout)
            
class DacWidget(QtGui.QWidget):
    """
    This widget is used to control the DACs of a driver. 
    """
    
    data_updated_signal = pyqtSignal(int)  
    
    def __init__(self, driver, index=0):
        super(DacWidget, self).__init__()
        
        self.n = driver.sampling.n
        self.fs = driver.sampling.fs
        
        self.index = index # used to track which DAC is related to the widget
        self.enable = False
        self.freq = 0
        self.mod_amp = 0
        self.waveform = 'Sine'
        self.data = np.zeros(self.n)

        # Layout
        self.layout = QtGui.QHBoxLayout()
        self.slider_layout = QtGui.QVBoxLayout()
        # DAC ON/OFF button
        self.button = QtGui.QPushButton('ON')        
        self.button.setStyleSheet('QPushButton {color: green;}') 
        self.button.setFixedWidth(80)
        self.button.setCheckable(True)
        # Waveform list
        self.waveform_list = WaveformList()  
        # Sliders
        self.freq_slider = KoheronSlider(name = 'Modulation frequency (MHz) : ', max_slider = 1e-6*self.fs/2, step = 1e-6*self.fs/self.n, alpha = 1)
        self.mod_amp_slider = KoheronSlider(name = 'Modulation amplitude (u.a.)   : ', max_slider = 1)
        # Add Widgets to Layout
        self.layout.addWidget(self.button)
        self.slider_layout.addWidget(self.mod_amp_slider)
        self.slider_layout.addWidget(self.freq_slider)
        self.layout.addWidget(self.waveform_list)
        self.layout.addLayout(self.slider_layout)
        self.setLayout(self.layout)
        
        self.button.clicked.connect(self.button_clicked)
        self.connect(self.freq_slider, SIGNAL("value(float)"), self.change_freq)
        self.connect(self.mod_amp_slider, SIGNAL("value(float)"), self.change_mod_amp)
        for i in range(len(self.waveform_list.list)):
            self.waveform_list.list[i].toggled.connect(self.update_data)
        
    def change_freq(self, value):
        value /= 1e-6*self.fs/self.n
        self.freq = np.floor(value)
        self.update_data()
   
    def change_mod_amp(self, value):
        self.mod_amp = value
        self.update_data()
        
    def button_clicked(self):
        self.enable = not self.enable   
        if self.enable:
            self.update_data()
            self.button.setStyleSheet('QPushButton {color: red;}')
            self.button.setText('OFF')
        else:
            self.data = np.zeros(self.n)
            self.data_updated_signal.emit(self.index)
            self.button.setStyleSheet('QPushButton {color: green;}')
            self.button.setText('ON')
        self.data_updated_signal.emit(self.index)
        
    def update_data(self):
        if self.waveform_list.list[0].isChecked():
            self.waveform_index = 0 
            self.data = self.mod_amp * np.cos(2*np.pi* self.freq/self.n*np.arange(self.n))
        elif self.waveform_list.list[1].isChecked():
            self.waveform_index = 1
            self.data = self.mod_amp * signal.sawtooth(2*np.pi* self.freq/self.n*np.arange(self.n), width = 0.5)            
        elif self.waveform_list.list[2].isChecked():
            self.waveform_index = 2
            self.data = self.mod_amp * signal.square(2*np.pi* self.freq/self.n*np.arange(self.n),duty=0.5)
        self.data_updated_signal.emit(self.index)
    
    
