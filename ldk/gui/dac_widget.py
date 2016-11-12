# -*- coding: utf-8 -*-

from pyqtgraph.Qt import QtGui, QtCore
from .slider_widget import SliderWidget
#from PyQt4.QtCore import SIGNAL, pyqtSignal
import numpy as np
from scipy import signal
import collections


class WaveformList(QtGui.QWidget):
    def __init__(self, items=['Sine', 'Triangle', 'Square']):
        super(WaveformList, self).__init__()
        self.layout = QtGui.QVBoxLayout()
        self.items = items
        self.list = []
        for item in self.items:
            self.list.append(QtGui.QRadioButton(item))
        for item in self.list:
            self.layout.addWidget(item)
        self.list[0].setChecked(True)
        self.setLayout(self.layout)

class DacWidget(QtGui.QWidget):
    """
    This widget is used to control the DACs of a driver.
    """

    data_updated_signal = QtCore.pyqtSignal(int)

    def __init__(self, driver, index=0):
        super(DacWidget, self).__init__()

        self.n = driver.sampling.n
        self.fs = driver.sampling.fs

        self.index = index  # used to track which DAC is related to the widget
        self.enable = False
        self.freq = 0
        self.mod_amp = 0
        self.offset = 0
        self.waveform = 'Sine'
        self.waveform_index = 0
        self.data = np.zeros(self.n)

        # Layout
        self.layout = QtGui.QHBoxLayout()
        self.slider_layout = QtGui.QGridLayout()
        # DAC ON/OFF button
        self.dac_on_off_button = QtGui.QPushButton('ON')
        self.dac_on_off_button.setStyleSheet('QPushButton {color: green;}')
        self.dac_on_off_button.setFixedWidth(80)
        self.dac_on_off_button.setCheckable(True)

        # Waveform list
        self.waveform_list = WaveformList()

        self.slider_dict = collections.OrderedDict()
        # Sliders
        self.slider_dict['mod_amp'] = SliderWidget(name='Amplitude (arb. units)', max_slider=1, layout=False)
        self.slider_dict['freq'] = SliderWidget(name='Frequency (MHz)', max_slider=1e-6 * self.fs / 2, step=1e-6 * self.fs / self.n, layout=False)
        self.slider_dict['offset'] = SliderWidget(name='Offset (arb. units)', min_slider = -1.0, max_slider=1, layout=False)

        for i, (name, slider) in enumerate(self.slider_dict.items()):
            self.slider_layout.addWidget(slider.label, i, 0)
            self.slider_layout.addWidget(slider.spin, i, 1)
            self.slider_layout.addWidget(slider.slider, i, 2)

        # Add Widgets to Layout
        self.waveform_list.layout.addWidget(self.dac_on_off_button)
        self.layout.addWidget(self.waveform_list)
        self.layout.addLayout(self.slider_layout)
        self.setLayout(self.layout)

        self.dac_on_off_button.clicked.connect(self.dac_on_off_button_clicked)
        self.slider_dict['mod_amp'].valueChanged.connect(self.change_mod_amp)
        self.slider_dict['freq'].valueChanged.connect(self.change_freq)
        self.slider_dict['offset'].valueChanged.connect(self.change_offset)

        for i in range(len(self.waveform_list.list)):
            self.waveform_list.list[i].toggled.connect(self.update_data)

    def change_freq(self, value):
        value /= 1e-6 * self.fs / self.n
        self.freq = np.floor(value)
        self.update_data()

    def change_mod_amp(self, value):
        self.mod_amp = value
        self.update_data()

    def change_offset(self, value):
        self.offset = value
        self.update_data()

    def dac_on_off_button_clicked(self):
        self.enable = not self.enable
        if self.enable:
            self.update_data()
            self.dac_on_off_button.setStyleSheet('QPushButton {color: red;}')
            self.dac_on_off_button.setText('OFF')
        else:
            self.data = np.zeros(self.n)
            self.data_updated_signal.emit(self.index)
            self.dac_on_off_button.setStyleSheet('QPushButton {color: green;}')
            self.dac_on_off_button.setText('ON')
        self.data_updated_signal.emit(self.index)

    def update_data(self):
        # Compute waveform
        if self.waveform_list.list[0].isChecked():
            # Sine
            self.waveform_index = 0
            self.data = self.offset + self.mod_amp * np.sin(2 * np.pi * self.freq / self.n * np.arange(self.n))
        elif self.waveform_list.list[1].isChecked():
            # Triangle
            self.waveform_index = 1
            self.data = self.offset + self.mod_amp * signal.sawtooth(2 * np.pi * self.freq / self.n * np.arange(self.n), width=0.5)
        elif self.waveform_list.list[2].isChecked():
            # Square
            self.waveform_index = 2
            self.data = self.offset + self.mod_amp * signal.square(2 * np.pi * self.freq / self.n * np.arange(self.n), duty=0.5)
        # Prevent overflow
        self.data[self.data >= +0.999] = +0.999
        self.data[self.data <= -0.999] = -0.999
        self.data_updated_signal.emit(self.index)
