# -*- coding: utf-8 -*-

from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import glob
import os


class CalibrationWidget(QtGui.QWidget):

    def __init__(self, driver, data_path=None):
        super(CalibrationWidget, self).__init__()

        self.driver = driver
        self.data_path = data_path

        self.layout = QtGui.QVBoxLayout()
        self.adc_offset_layout = QtGui.QHBoxLayout()
        self.calibration_layout = QtGui.QHBoxLayout()
        self.calibration_list_layout = QtGui.QVBoxLayout()

        self.adc_offset_box = QtGui.QGroupBox("ADC offset")
        self.calibration_box = QtGui.QGroupBox("Optical calibration")

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

        self.adc_offset_layout.addWidget(self.adc_offset_button)
        self.adc_offset_box.setLayout(self.adc_offset_layout)

        self.calibration_layout.addLayout(self.calibration_list_layout)
        self.calibration_layout.addWidget(self.calibration_line)
        self.calibration_layout.addWidget(self.calibration_label)
        self.calibration_layout.addWidget(self.calibration_button)

        self.calibration_box.setLayout(self.calibration_layout)

        self.calibration_button.clicked.connect(self.optical_calibration)

        self.layout.addWidget(self.adc_offset_box)
        self.layout.addWidget(self.calibration_box)
        self.layout.addStretch(1)

        self.setLayout(self.layout)

        # Connections
        self.adc_offset_button.clicked.connect(self.adc_offset)

    def optical_calibration(self, index):
        if self.calibration_list[0].isChecked():
            index = 0
        else:
            index = 1
        if self.calibration_line.text() == '' :
            return
        else:
            self.driver.optical_power[index] *= float(self.calibration_line.text())
            self.driver.power[index] *= np.mean(self.driver.adc[index, :])
            self.calibration_line.setText('')

    def adc_offset(self):
        self.driver.get_adc()
        self.driver.adc_offset[0] += np.mean(self.driver.adc[0, :])
        self.driver.adc_offset[1] += np.mean(self.driver.adc[1, :])