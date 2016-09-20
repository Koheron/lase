# -*- coding: utf-8 -*-

from pyqtgraph.Qt import QtGui, QtCore
from PyQt4.QtCore import SIGNAL, pyqtSignal
from .slider_widget import SliderWidget
import numpy as np

class MathWidget(QtGui.QWidget):

    def __init__(self, driver, plot_widget):
        super(MathWidget, self).__init__()

        self.driver = driver
        self.plot_widget = plot_widget

        self.n_avg_spectrum = 1
        self.correction = False
        self.fourier = False

        self.layout = QtGui.QVBoxLayout()
        self.checkbox_layout = QtGui.QHBoxLayout()
        self.n_avg_min_layout = QtGui.QHBoxLayout()
        self.avg_layout = QtGui.QHBoxLayout()

        # Correction
        self.correction_checkbox = QtGui.QCheckBox('Correction', self)
        self.correction_checkbox.setCheckState(QtCore.Qt.Unchecked)

        # Plot Fourier Transform
        self.fourier_checkbox = QtGui.QCheckBox('Fourier Transform', self)
        self.fourier_checkbox.setCheckState(QtCore.Qt.Unchecked)

        # Select minimum number of averages 
        self.n_avg_min_label = QtGui.QLabel()
        self.n_avg_min_label.setText('Min. # of averages')
        self.n_avg_min_spin = QtGui.QSpinBox()
        self.n_avg_min_spin.setMaximum(10000)
        self.n_avg_min_spin.setMinimum(0)
        self.n_avg_min_spin.setValue(0)

        self.n_avg_min_slider = SliderWidget(name='Min. # of averages : ',
                                             max_slider=1000, step=1)

        # Select avg
        self.n_avg_label = QtGui.QLabel()
        self.n_avg_label.setText('FFT averages')
        self.avg_spin = QtGui.QSpinBox()
        self.avg_spin.setMaximum(1000)
        self.avg_spin.setMinimum(1)
        self.avg_spin.setValue(1)

        # Average on 
        self.avg_on_button = QtGui.QPushButton()
        self.avg_on_button.setStyleSheet('QPushButton {color: green;}')
        self.avg_on_button.setText('Start averaging')
        self.avg_on_button.setCheckable(True)

        # Set layout
        self.layout.addWidget(self.n_avg_min_slider)

        self.layout.addWidget(self.avg_on_button)
        self.checkbox_layout.addStretch(1)
        self.checkbox_layout.addWidget(self.fourier_checkbox)
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
        self.fourier_checkbox.stateChanged.connect(self.fourier_connect)
        self.avg_spin.valueChanged.connect(self.avg_connect)
        self.connect(self.n_avg_min_slider, SIGNAL("value(float)"), self.change_n_avg_min)

    def change_averaging(self):
        self.driver.averaging = not self.driver.averaging
        if self.driver.averaging:
            self.avg_on_button.setStyleSheet('QPushButton {color: red;}')
            self.avg_on_button.setText('Stop averaging')
        else:
            self.avg_on_button.setStyleSheet('QPushButton {color: green;}')
            self.avg_on_button.setText('Start averaging')

    def fourier_connect(self, state):
        if state == QtCore.Qt.Checked:
            self.plot_widget.getPlotItem().\
                 getAxis('bottom').setLabel('Frequency (MHz)')
            self.plot_widget.getPlotItem().\
                 getAxis('left').setLabel('Spectrum power')
            self.fourier = True
            self.plot_widget.enableAutoRange()
            self.avg_widget.setVisible(True)
        else:
            self.plot_widget.getPlotItem().\
                 getAxis('bottom').setLabel('Time (us)')
            self.plot_widget.getPlotItem().\
                 getAxis('left').setLabel('Optical power (u.a.)')
            self.fourier = False
            self.plot_widget.enableAutoRange()
            self.avg_widget.setVisible(False)

    def avg_connect(self):
        self.n_avg_spectrum = self.avg_spin.value()

    def change_n_avg_min(self, value):
        self.driver.n_avg = int(value)

    def save_as_h5(self, f):
        math_grp = f.create_group('math')
        avg_on_button_dset = f.create_dataset('math/avg_on_button', (0,), dtype='f')
        avg_on_button_dset.attrs['StyleSheet'] = unicode(self.avg_on_button.styleSheet())
        avg_on_button_dset.attrs['Text'] = unicode(self.avg_on_button.text())

        avg_spin_dset = f.create_dataset('math/avg_spin', (0,), dtype='f')
        avg_spin_dset.attrs['Minimum'] = self.avg_spin.minimum()
        avg_spin_dset.attrs['Maximum'] = self.avg_spin.maximum()
        avg_spin_dset.attrs['Value'] = self.avg_spin.value()

        fourier_dset = f.create_dataset('math/fourier', (0,), dtype='f')
        fourier_dset.attrs['Status'] = self.fourier

    def save_as_zip(self, _dict, dest=''):
        _dict['math'] = {
          'AvgOnButton': {
            'StyleSheet': unicode(self.avg_on_button.styleSheet()),
            'Text': unicode(self.avg_on_button.text())
          },
          'AvgSpin': {
            'Minimum': self.avg_spin.minimum(),
            'Maximum': self.avg_spin.maximum(),
            'Value': self.avg_spin.value()
          },
          'Fourier': {
            'Status': self.fourier
          }
        }
