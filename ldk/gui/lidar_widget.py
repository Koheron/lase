# -*- coding: utf-8 -*-

from pyqtgraph.Qt import QtGui

from .plot_widget import PlotWidget
from .plot_widget import RollingPlot
from .slider_widget import SliderWidget
import numpy as np
import collections

class LidarWidget(QtGui.QWidget):
    def __init__(self, spectrum_widget):
        super(LidarWidget, self).__init__()
        self.spectrum_widget = spectrum_widget
        self.driver = spectrum_widget.driver

        self.layout = QtGui.QVBoxLayout()
        self.lidar_layout = QtGui.QVBoxLayout()
        self.slider_layout = QtGui.QGridLayout()

        self.slider_dict = collections.OrderedDict()
        self.slider_dict['f_min'] = SliderWidget(name='Min frequency (MHz) : ',
                                                 max_slider=self.driver.sampling.fs/2*1e-6)
        self.slider_dict['f_max'] = SliderWidget(name='Max frequency (MHz) : ',
                                                 max_slider=self.driver.sampling.fs/2*1e-6)

        for i, (name, slider) in enumerate(self.slider_dict.items()):
            self.slider_layout.addWidget(slider.label, i, 0)
            self.slider_layout.addWidget(slider.spin, i, 1)
            self.slider_layout.addWidget(slider.slider, i, 2)

        self.velocity_label = QtGui.QLabel()
        self.velocity_label.setText('Velocity (m/s) : '+"{:.2f}".format(0))

        self.velocity_plot_button = QtGui.QPushButton('Velocity')
        self.velocity_plot_button.setStyleSheet('QPushButton {color: blue;}')
        self.velocity_plot_button.setCheckable(True)

        self.lidar_layout.addLayout(self.slider_layout)
        self.lidar_layout.addWidget(self.velocity_label)
        self.lidar_layout.addWidget(self.velocity_plot_button)

        self.lidar_box = QtGui.QGroupBox("Lidar")
        self.lidar_box.setLayout(self.lidar_layout)

        self.layout.addWidget(self.lidar_box)
        self.setLayout(self.layout)

        self.velocity_plot_button.clicked.connect(self.swap_plots)
        self.is_velocity_plot = False

        self.rolling_plot = RollingPlot()
        self.rolling_plot.getPlotItem().getAxis('bottom').setLabel('Time')
        self.rolling_plot.getPlotItem().getAxis('left').setLabel('Velocity', units='m/s')
        self.rolling_plot.set_axis()

        self.velocity = 0

        self.slider_dict['f_min'].valueChanged.connect(self.change_fmin)
        self.slider_dict['f_max'].valueChanged.connect(self.change_fmax)

    def update(self, spectrum):
        self.velocity = self.driver.get_peak_values() * self.driver.sampling.df * 1e-6 * 1.29
        self.velocity_label.setText('Velocity (m/s) : '+"{:.2f}".format(np.mean(self.velocity))                                  )
        self.rolling_plot.update(self.velocity)

    def swap_plots(self):
        if self.is_velocity_plot:  # switch to spectrum plot
            self.is_velocity_plot = False
            self.velocity_plot_button.setText('Velocity')
            self.spectrum_widget.set_plot_widget(self.spectrum_widget.spectrum_plot_widget)
        else:  # switch to velocity plot
            self.is_velocity_plot = True
            self.velocity_plot_button.setText('Spectrum')
            self.spectrum_widget.set_plot_widget(self.rolling_plot)
            self.rolling_plot.set_axis()

        self.spectrum_widget.plot_widget.getPlotItem().enableAutoRange()
        self.spectrum_widget.plot_widget.set_axis()

    def change_fmin(self, value):
        self.driver.set_address_range(np.uint32(value*1e6/self.driver.sampling.df),
                                      np.uint32(self.slider_dict['f_max'].value*1e6/self.driver.sampling.df))

    def change_fmax(self, value):
        self.driver.set_address_range(np.uint32(self.slider_dict['f_min'].value*1e6/self.driver.sampling.df),
                                      np.uint32(value*1e6/self.driver.sampling.df))
