#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg

from lase_widget import LaseWidget
from save_widget import SaveWidget
from cursor_widget import CursorWidget
from stats_widget import StatsWidget
from select_channel_widget import SelectChannelWidget
from math_widget import MathWidget
from calibration_widget import CalibrationWidget

class OscilloWidget(LaseWidget):
    def __init__(self, oscillo, parent):
        super(OscilloWidget, self).__init__(oscillo, parent)
        
        self.driver = oscillo
        self.avg_on = False

        self.counter = 0
        
        self.data_path = parent.data_path
        
        # Layouts          
        self.splitterV_1 = QtGui.QVBoxLayout() 
        self.auto_scale_layout = QtGui.QHBoxLayout()
        
        self.tabs = QtGui.QTabWidget() 
        self.control = QtGui.QWidget()
        self.tabs.addTab(self.control,"Control")
        
        self.calibration_widget = CalibrationWidget(self.driver, 
                                                    data_path=self.data_path)
        self.tabs.addTab(self.calibration_widget,"Calibration")
        
        self.plotWid = KPlotWidget(self.driver, name="data")   
        
        # Widgets : Buttons, Sliders, PlotWidgets
                
        self.save_box = QtGui.QGroupBox("Save")
        
        self.auto_scale_button = QtGui.QPushButton('Auto scale')        
        self.auto_scale_button.setStyleSheet('QPushButton {color: green;}')
        self.auto_scale_button.setFixedWidth(312)
      
        # Add Widgets to layout
        self.set_axis()
        self.left_panel_layout.insertWidget(1, self.plotWid, 1)        
        self.select_channel_widget = SelectChannelWidget(self.plotWid)
        self.display_box = QtGui.QGroupBox("Display")
        self.display_box.setLayout(self.select_channel_widget.layout)
       
        self.math_widget = MathWidget(self.driver, self.plotWid)
        self.math_box = QtGui.QGroupBox("Math")
        self.math_box.setLayout(self.math_widget.layout)
        
        self.stats_widget = StatsWidget(self.driver)
        
        
        self.cursors_box = QtGui.QGroupBox('Cursors')
        self.cursor_widget = CursorWidget(self.plotWid)
        self.cursors_box.setLayout(self.cursor_widget.layout)
        
        # Save widget        
        self.save_widget = SaveWidget(self)
        self.save_box.setLayout(self.save_widget.layout)       
        
        self.auto_scale_layout.addWidget(self.auto_scale_button, QtCore.Qt.AlignCenter)
        self.splitterV_1.addWidget(self.display_box)
        self.splitterV_1.addLayout(self.stats_widget.layout)
        self.splitterV_1.addWidget(self.cursors_box)
        self.splitterV_1.addLayout(self.auto_scale_layout)
        self.splitterV_1.addWidget(self.math_box)
        self.splitterV_1.addWidget(self.save_box)        
        self.splitterV_1.addStretch(1)        
        self.control.setLayout(self.splitterV_1)
        
        self.right_panel.addWidget(self.tabs)

        self.right_panel_widget.setLayout(self.right_panel)
        
        self.auto_scale_button.clicked.connect(self.auto_scale)
   
    def update(self):
        super(OscilloWidget, self).update()
        self.driver.get_adc()
        self.stats_widget.update()
        
        if (self.counter == 20):
            if self.math_widget.correction == True:            
                self.driver.optimize_amplitude(channel = 1)
                self.driver.set_dac(warning=True) 
                self.refresh_dac() 
                               
            self.counter = 0
            
        self.counter += 1

        # This should be in the KPlotWidget class
        if self.math_widget.fourier: 
            self.driver.get_avg_spectrum(self.math_widget.n_avg_spectrum)                      
            self.plotWid.dataItem[0].setData(
                1e-6 * self.driver.sampling.f_fft[1: self.driver.sampling.n/2], 
                10*np.log10((self.driver.avg_spectrum[0,1:])**2)
            )
            self.plotWid.dataItem[1].setData(
                1e-6 * self.driver.sampling.f_fft[1: self.driver.sampling.n/2],
                10*np.log10((self.driver.avg_spectrum[1,1:])**2)
            )
        else:
            self.plotWid.dataItem[0].setData(1e6*self.driver.sampling.t,
                                             self.driver.adc[0,:])
            self.plotWid.dataItem[1].setData(1e6*self.driver.sampling.t,
                                             self.driver.adc[1,:])   
                 
    def update_dac(self, index):
        if self.dac_wid[index].button.text() == 'OFF':
            if self.math_widget.correction == False:
                self.driver.dac[index,:] = self.dac_wid[index].data
                self.driver.set_dac()
                self.refresh_dac()
            else:
                self.driver.ideal_amplitude_waveform \
                    = 1167 * self.driver.optical_power[0] / self.driver.power[0] * self.dac_wid[1].data
    
                self.driver.amplitude_error = self.driver.ideal_amplitude_waveform
                self.driver.dac[1,:] = self.driver.get_correction()            
                self.driver.set_dac()
                self.refresh_dac()
             
    def refresh_dac(self):
        self.plotWid.dataItem[2].setData(1e6*self.driver.sampling.t, 8192*self.driver.dac[0,:])
        self.plotWid.dataItem[3].setData(1e6*self.driver.sampling.t, 8192*self.driver.dac[1,:])
    
    def set_axis(self):
        self.plotWid.getPlotItem().getAxis('bottom').setLabel('Time (us)')
        self.plotWid.getPlotItem().getAxis('left').setLabel('Optical power (u.a.)')
        self.plotWid.getViewBox().setMouseMode(self.plotWid.getViewBox().PanMode)
        
    def auto_scale(self):
        self.plotWid.enableAutoRange()
    
    
class KPlotWidget(pg.PlotWidget):
    def __init__(self, driver, *args, **kwargs):
        super(KPlotWidget, self).__init__(*args, **kwargs)
        
        self.driver = driver
        
        # Right part
        self.show_adc = [True, True]
        self.show_dac = [False, False]        
        
        # Plot Widget   
        self.dataItem = []
        self.dataItem.append(pg.PlotDataItem(1e6*self.driver.sampling.t,
                                             self.driver.adc[0,:], 
                                             pen=(0,4)))
        self.dataItem.append(pg.PlotDataItem(1e6*self.driver.sampling.t,
                                             self.driver.adc[1,:], 

                                             pen=(1,4)))
        self.dataItem.append(pg.PlotDataItem(1e6*self.driver.sampling.t,
                                             self.driver.dac[0,:], 
                                             pen=(0,4)))
        self.dataItem.append(pg.PlotDataItem(1e6*self.driver.sampling.t,
                                             self.driver.dac[1,:], 
                                             pen=(1,4)))     
        
        for item in self.dataItem:
            self.addItem(item)

        self.dataItem[0].setVisible(self.show_adc[0])
        self.dataItem[1].setVisible(self.show_adc[1])
        self.dataItem[2].setVisible(self.show_dac[0])
        self.dataItem[3].setVisible(self.show_dac[1])
        
        self.plotItem = self.getPlotItem()
        self.plotItem.setMouseEnabled(x=False, y = True)
         
