# -*- coding: utf-8 -*-

from pyqtgraph.Qt import QtGui
import numpy as np
import time

class MonitorWidget(QtGui.QWidget):

    def __init__(self, driver, laser_widget):
        super(MonitorWidget, self).__init__()
        self.driver = driver
        self.laser_widget = laser_widget

        self.laser_current = self.driver.get_laser_current()
        self.laser_power = self.driver.get_laser_power()

        # Layout
        self.layout = QtGui.QGridLayout()

        # Close button
        self.close_button = QtGui.QPushButton('Home')
        self.close_button.setStyleSheet('QPushButton {color: blue;}')
        self.close_button.setFixedWidth(80)

        # Frame rate
        self.frame_rate_label = QtGui.QLabel()
        self.frame_rate_label.setText('Frame rate (Hz) : '+"{:.1f}".format(0))
        # Laser power
        self.laser_power_label = QtGui.QLabel()
        self.laser_power_label.setText('Laser power (u.a.) : '+
                                       "{:.2f}".format(self.driver.get_laser_power()))

        # Laser current measured from the XADC
        self.laser_current_label = QtGui.QLabel()
        self.laser_current_label.setText('Measured current (mA) : '+
            "{:.2f}".format(0.01 * self.driver.get_laser_current()))

        self.layout.addWidget(self.close_button, 0, 0)
        self.layout.addWidget(self.frame_rate_label, 0, 1)
        self.layout.addWidget(self.laser_current_label, 0, 2)
        self.layout.addWidget(self.laser_power_label, 0, 3)

        # Connections
        self.close_button.clicked.connect(self.close_session)

    def update(self, frame_rate = 0):
        self.frame_rate = frame_rate
        self.laser_current = 0.95 * self.laser_current + 0.05 * self.driver.get_laser_current()
        self.laser_power = 0.95 * self.laser_power + 0.05 * self.driver.get_laser_power()

        self.laser_current_label.setText('Measured current (mA): '+
                                         "{:.2f}".format(1000 * self.laser_current))
        self.laser_power_label.setText('Laser power (a. u.): '+
                                       "{:.2f}".format(self.laser_power))
        self.frame_rate_label.setText('Frame rate (Hz): '+
                                      "{:.2f}".format(self.frame_rate))

    def close_session(self):
        try:
            self.laser_widget.stop_laser()
            self.driver.opened = False
        except:
            self.driver.opened = False

    def save_as_h5(self, f):
        monitor_grp = f.create_group('monitor')
        monitor_dset = f.create_dataset('monitor/data', (0,), dtype='f')
        monitor_dset.attrs['FrameRate'] = self.frame_rate
        monitor_dset.attrs['LaserCurrent'] = self.laser_current
        monitor_dset.attrs['LaserPower'] = self.laser_power

    def save_as_zip(self, _dict, dest=''):
        _dict['monitor'] = {
          'FrameRate': self.frame_rate,
          'LaserCurrent': self.laser_current,
          'LaserPower': self.laser_power
        }
