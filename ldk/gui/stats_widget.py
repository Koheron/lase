# -*- coding: utf-8 -*-

from pyqtgraph.Qt import QtGui, QtCore
import numpy as np

class StatsWidget(QtGui.QWidget):

    def __init__(self, driver):
        super(StatsWidget, self).__init__()

        self.driver = driver

        self.layout = QtGui.QGridLayout()

        self.mean_labels = []
        self.ampl_labels = []
        self.ampl_rms_labels = []
        self.n_channels = 2
        self.window_size = 50

        self.average = np.zeros(self.n_channels)
        self.amplitude = np.zeros(self.n_channels)
        self.amplitude_rms = np.zeros(self.n_channels)

        self.average_vec = np.zeros((self.n_channels, self.window_size))
        self.amplitude_vec = np.zeros((self.n_channels, self.window_size))
        self.amplitude_rms_vec = np.zeros((self.n_channels, self.window_size))

        for i in range(self.n_channels):
            self.average_vec[i,:] = self.get_average(i)
            self.amplitude_vec[i,:] = self.get_amplitude(i)
            self.amplitude_rms_vec[i,:] = self.get_amplitude_rms(i)

        for i in range(self.n_channels+1):
            self.mean_labels.append(QtGui.QLabel(''))
            self.ampl_labels.append(QtGui.QLabel(''))
            self.ampl_rms_labels.append(QtGui.QLabel(''))

        self.mean_labels[0].setText('Average')
        self.ampl_labels[0].setText('Peak-Peak')
        self.ampl_rms_labels[0].setText('RMS')

        for i in range(self.n_channels+1):
            self.layout.addWidget(QtGui.QLabel('DAC '+str(i) if i != 0 else ''), 0, i)
            self.layout.addWidget(self.mean_labels[i], 1, i)
            self.layout.addWidget(self.ampl_labels[i], 2, i)
            self.layout.addWidget(self.ampl_rms_labels[i], 3, i)
          
    def get_average(self, channel):
        return np.mean(self.driver.adc[channel,:])

    def get_amplitude(self, channel):
        return np.max(self.driver.adc[channel,:])-np.min(self.driver.adc[channel,:])

    def get_amplitude_rms(self, channel):
        return np.std(self.driver.adc[channel,:])

    def format_value(self, value):
        return '{:.2f}'.format(value) if 1e-2 < abs(value) < 1e4 else '%.4e' % value

    def update(self):
        self.average_vec = np.roll(self.average_vec, 1, axis=1)
        self.amplitude_vec = np.roll(self.amplitude_vec, 1, axis=1)
        self.amplitude_rms_vec = np.roll(self.amplitude_rms_vec, 1, axis=1)

        for i in range(self.n_channels):            
            self.average_vec[i,0] = self.get_average(i)
            self.amplitude_vec[i,0] = self.get_amplitude(i)
            self.amplitude_rms_vec[i,0] = self.get_amplitude_rms(i)

            self.average[i] = np.mean(self.average_vec[i,:])
            mean_text = self.format_value(self.average[i])
            self.mean_labels[i+1].setText(mean_text)

            self.amplitude[i] = np.mean(self.amplitude_vec[i,:])
            ampl_text = self.format_value(self.amplitude[i])
            self.ampl_labels[i+1].setText(ampl_text)

            self.amplitude_rms[i] = np.mean(self.amplitude_rms_vec[i,:])
            ampl_rms_text = self.format_value(self.amplitude_rms[i])
            self.ampl_rms_labels[i+1].setText(ampl_rms_text)

