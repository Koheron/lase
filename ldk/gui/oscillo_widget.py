#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import os

from .base_widget import BaseWidget
from .cursor_widget import CursorWidget
from .stats_widget import StatsWidget
from .select_channel_widget import SelectChannelWidget
from .math_widget import MathWidget
from .save_widget import SaveWidget

class OscilloWidget(BaseWidget):
    def __init__(self, oscillo, parent):
        super(OscilloWidget, self).__init__(oscillo, parent)

        self.driver = oscillo
        self.avg_on = False
        self.data_path = parent.data_path

        # Layouts
        self.control_layout = QtGui.QVBoxLayout()

        # Plot widget
        self.init_plot_widget()
        self.set_axis()

        # Tab widget
        self.tabs = QtGui.QTabWidget()
        # Control
        self.control = QtGui.QWidget()
        self.tabs.addTab(self.control, "Control")

        # Display
        self.select_channel_widget = SelectChannelWidget(self.plot_widget)
        self.display_box = QtGui.QGroupBox("Display")
        self.display_box.setLayout(self.select_channel_widget.layout)
        # Stats
        self.stats_widget = StatsWidget(self.driver)
        # Cursors
        self.cursors_box = QtGui.QGroupBox('Cursors')
        self.cursor_widget = CursorWidget(self.plot_widget)
        self.cursors_box.setLayout(self.cursor_widget.layout)

        # Math
        self.math_widget = MathWidget(self.driver, self.plot_widget)
        self.math_box = QtGui.QGroupBox("Math")
        self.math_box.setLayout(self.math_widget.layout)

        # Save
        self.save_widget = SaveWidget('oscillo', self)
        self.save_box = QtGui.QGroupBox("Save")
        self.save_box.setLayout(self.save_widget.layout)

        # Add widgets to control layout
        self.control_layout.addWidget(self.display_box)
        self.control_layout.addLayout(self.stats_widget.layout)
        self.control_layout.addWidget(self.cursors_box)
        self.control_layout.addWidget(self.math_box)
        self.control_layout.addWidget(self.save_box)
        self.control_layout.addStretch(1)
        self.control.setLayout(self.control_layout)

        self.right_panel.addWidget(self.tabs)
        self.right_panel_widget.setLayout(self.right_panel)

    def init_plot_widget(self):
        # Right part
        self.plot_widget.show_adc = [True, True]
        self.plot_widget.show_dac = [False, False]

        # Plot Widget
        self.plot_widget.dataItem = []
        for i in range(2):
            self.plot_widget.dataItem.append(pg.PlotDataItem(1e6*self.driver.sampling.t,
                                             self.driver.adc[i, :], pen=(i, 4)))
        for i in range(2):
            self.plot_widget.dataItem.append(pg.PlotDataItem(1e6*self.driver.sampling.t,
                                             self.driver.dac[i, :], pen=(i, 4)))

        for item in self.plot_widget.dataItem:
            self.plot_widget.addItem(item)
        
        for i in range(2):
            self.plot_widget.dataItem[i].setVisible(self.plot_widget.show_adc[i])
            self.plot_widget.dataItem[i+2].setVisible(self.plot_widget.show_dac[i])

        self.plot_widget.plotItem.setMouseEnabled(x=False, y=True)

        self.plot_widget.plotItem = self.plot_widget.getPlotItem()


    def update(self):
        super(OscilloWidget, self).update()
        self.driver.get_adc()
        self.stats_widget.update()
        if self.math_widget.fourier:
            self.update_fourier()
        else:
            self.refresh_adc()

    def update_fourier(self):
        self.driver.get_avg_spectrum(self.math_widget.n_avg_spectrum)
        for i in range(2):
            self.plot_widget.dataItem[i].setData(
                    1e-6 * self.driver.sampling.f_fft[1: int(self.driver.sampling.n / 2)],
                    10 * np.log10((self.driver.avg_spectrum[i, 1:]) ** 2))

    def refresh_adc(self):
        for i in range(2):
            self.plot_widget.dataItem[i].setData(1e6 * self.driver.sampling.t,
                                                 self.driver.adc[i, :])

    def refresh_dac(self):
        for i in range(2):
            self.plot_widget.dataItem[i+2].setData(1e6 * self.driver.sampling.t, 
                                                   8192 * self.driver.dac[i, :])

    def set_axis(self):
        self.plot_widget.getPlotItem().getAxis('bottom').setLabel('Time (us)')
        self.plot_widget.getPlotItem().getAxis('left').setLabel('Optical power (arb. units)')
        self.plot_widget.getViewBox().setMouseMode(self.plot_widget.getViewBox().PanMode)

    def get_data_to_save(self):
        if not self.math_widget.fourier:
            wfm_size = self.driver.wfm_size
        else:
            wfm_size = self.driver.wfm_size/2 - 1

        data_x = np.zeros((2, wfm_size))
        data_y = np.zeros((2, wfm_size))
        data_x[0,:], data_y[0,:] = self.plot_widget.dataItem[0].getData()
        data_x[1,:], data_y[1,:] = self.plot_widget.dataItem[1].getData()
        return data_x, data_y, wfm_size

    def save_as_h5(self, f):
        data_x, data_y, wfm_size = self.get_data_to_save()
        plot_grp = f.create_group('plot')
        plot_data_x_dset = f.create_dataset('plot/data_x', (2, wfm_size), dtype='f')
        plot_data_x_dset[...] = data_x
        plot_data_y_dset = f.create_dataset('plot/data_y', (2, wfm_size), dtype='f')
        plot_data_y_dset[...] = data_y

    def save_as_zip(self, _dict, dest=''):
        data_x, data_y, wfm_size = self.get_data_to_save()
        data = np.zeros((4, wfm_size))
        data[0,:] = data_x[0,:]
        data[1,:] = data_x[1,:]
        data[2,:] = data_y[0,:]
        data[3,:] = data_y[1,:]
        np.save(os.path.join(dest, 'plot_data.npy'), data)
