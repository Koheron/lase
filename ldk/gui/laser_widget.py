# -*- coding: utf-8 -*-

from pyqtgraph.Qt import QtGui
from .slider_widget import SliderWidget
from PyQt4.QtCore import SIGNAL, pyqtSignal
import numpy as np

class LaserWidget(QtGui.QWidget):

    laser_updated_signal = pyqtSignal(int)

    def __init__(self, driver, laser_on=False, laser_current=0):
        super(LaserWidget, self).__init__()

        self.driver = driver
        self.laser_on = laser_on
        self.laser_current = laser_current

        self.driver.laser_current = self.laser_current * self.laser_on

        # Layout
        self.layout = QtGui.QHBoxLayout()
        # Laser ON/OFF button
        self.on_button = QtGui.QPushButton()
        self.on_button.setStyleSheet('QPushButton {color: green;}')
        self.on_button.setText('Start laser')
        self.on_button.setCheckable(True)
        self.on_button.setFixedWidth(80)
        # Laser current slider
        self.slider = SliderWidget(name='Laser current (mA) : ',
                                   max_slider=self.driver.max_current)

        self.layout.addWidget(self.on_button, 0)
        self.layout.addWidget(self.slider)

        self.connect(self.slider, SIGNAL("value(float)"), self.change_current)
        self.on_button.clicked.connect(self.stop_laser)

    def stop_laser(self):
        self.laser_on = not self.laser_on
        if self.laser_on:
            self.on_button.setStyleSheet('QPushButton {color: red;}')
            self.on_button.setText('Stop laser')
            self.driver.start_laser()
        else:
            self.on_button.setStyleSheet('QPushButton {color: green;}')
            self.on_button.setText('Start laser')
            self.driver.stop_laser()

    def change_current(self, value):
        self.laser_current = value
        self.driver.laser_current = self.laser_current

    def save_as_h5(self, f):
        laser_grp = f.create_group('laser')
        laser_dset = f.create_dataset('laser/data', (0,), dtype='f')
        laser_dset.attrs['LaserCurrent'] = self.laser_current
        laser_dset.attrs['LaserON'] = self.laser_on

    def save_as_zip(self, _dict, dest=''):
        _dict['laser'] = {
          'LaserCurrent': self.laser_current,
          'LaserON': self.laser_on
        }