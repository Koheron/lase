# -*- coding: utf-8 -*-

import os
import numpy as np
from pyqtgraph.Qt import QtGui
from PyQt4.QtCore import SIGNAL, pyqtSignal

from .base_widget import BaseWidget
from .plot_widget import PlotWidget
from .cursor_widget import CursorWidget
from .noise_floor_widget import NoiseFloorWidget
from .lidar_widget import LidarWidget
from .slider_widget import SliderWidget
from .save_widget import SaveWidget

from PyQt4.QtCore import pyqtSignal

class SpectrumWidget(BaseWidget):

    #offset_updated_signal = pyqtSignal(int)

    def __init__(self, spectrum, parent):
        super(SpectrumWidget, self).__init__(spectrum, parent)
        
        self.driver = spectrum

        # Layouts
        self.control_layout = QtGui.QVBoxLayout()

        # Plot widget
        self.init_plot_widget()
        self.set_plot_widget(self.spectrum_plot_widget)

        self.cursor_widget = CursorWidget(self.plot_widget)
        self.calibration_widget = NoiseFloorWidget(self.driver)
        self.lidar_widget = LidarWidget(self)

        # Save
        self.save_widget = SaveWidget('spectrum', self)
        self.save_box = QtGui.QGroupBox("Save")
        self.save_box.setLayout(self.save_widget.layout)

        # Averaging
        self.n_avg_min_slider = SliderWidget(name='Min. # of averages : ',
                                             max_slider=2000, step=1)

        self.avg_on_button = QtGui.QPushButton()
        self.avg_on_button.setStyleSheet('QPushButton {color: red;}')
        self.avg_on_button.setText('Stop averaging')
        self.avg_on_button.setCheckable(True)

        self.control_layout.addWidget(self.cursor_widget)
        self.control_layout.addWidget(self.calibration_widget)
        self.control_layout.addWidget(self.n_avg_min_slider)
        self.control_layout.addWidget(self.avg_on_button)
        self.control_layout.addWidget(self.lidar_widget)
        self.control_layout.addWidget(self.save_box)
        self.control_layout.addStretch(1)

        self.avg_on_button.clicked.connect(self.change_averaging)
        self.connect(self.n_avg_min_slider, SIGNAL("value(float)"), self.change_n_avg_min)

        self.right_panel_widget.setLayout(self.control_layout)

    def update(self):
        super(SpectrumWidget, self).update()
        self.driver.get_spectrum()

        self.spectrum = self.driver.spectrum - 0*self.calibration_widget.noise_floor
        self.lidar_widget.update(self.spectrum)

        self.plot_x = 1e-6 * np.fft.fftshift(self.driver.sampling.f_fft)
        self.plot_y = np.fft.fftshift(self.spectrum)

        if not self.lidar_widget.is_velocity_plot:
            self.plot_widget.dataItem.setData(
                        self.plot_x, self.plot_y,
                        pen=(0,4), clear=True, _callSync='off')

    def refresh_dac(self):
        pass

    def init_plot_widget(self):
        self.spectrum_plot_widget = PlotWidget(name="data")
        self.spectrum_plot_widget.getPlotItem().getAxis('bottom').setLabel('Frequency', units='MHz')
        self.spectrum_plot_widget.getPlotItem().getAxis('left').setLabel('PSD')
        self.spectrum_plot_widget.plotItem.setMouseEnabled(x=False, y=True)
        self.spectrum_plot_widget.plotItem.setLogMode(x=False, y=True)

    def set_plot_widget(self, new_plot_widget):
        self.plot_widget.setParent(None)
        self.plot_widget = new_plot_widget
        self.left_panel_layout.insertWidget(1, self.plot_widget, 1)

    def change_averaging(self):
        self.driver.avg_on = not self.driver.avg_on
        if self.driver.avg_on:
            self.avg_on_button.setStyleSheet('QPushButton {color: red;}')
            self.avg_on_button.setText('Stop averaging')
        else:
            self.avg_on_button.setStyleSheet('QPushButton {color: green;}')
            self.avg_on_button.setText('Start averaging')
        self.driver.set_averaging(self.driver.avg_on)

    def change_n_avg_min(self, value):
        self.driver.set_n_avg_min(int(value))

    def save_as_h5(self, f):
        pass

    def save_as_zip(self, _dict, dest=''):
        data = np.zeros((2, len(self.plot_x)))
        data[0,:] = self.plot_x
        data[1,:] = self.plot_y
        np.save(os.path.join(dest, 'plot_data.npy'), data)

