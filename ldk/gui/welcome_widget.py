# -*- coding: utf-8 -*-

from pyqtgraph.Qt import QtGui, QtCore
import time
import os
import sys

if sys.version_info[0] == 3:
    import urllib.request
else:
    import urllib
# http://stackoverflow.com/questions/17960942/attributeerror-module-object-has-no-attribute-urlretrieve


from ..drivers import Oscillo, Spectrum
from .oscillo_widget import OscilloWidget
from .spectrum_widget import SpectrumWidget
from .connect_widget import ConnectWidget
from koheron import connect

class WelcomeWidget(QtGui.QWidget):
    """ This widget allows to connect to one of the available drivers.
    """
    def __init__(self, parent, ip_path):
        super(WelcomeWidget, self).__init__()

        self.parent = parent
        self.app_list = self.parent.app_list
        self.instrument_list = [''] * len(self.app_list)

        self.ip_path = ip_path
        self.opened = True
        self.select_opened = True

        # Define layouts
        self.lay = QtGui.QHBoxLayout()
        self.left_layout = QtGui.QVBoxLayout()
        self.right_layout = QtGui.QVBoxLayout()

        # Connection (ip address and password)
        self.connect_layout = QtGui.QVBoxLayout()
        self.connect_widget = ConnectWidget(self, self.ip_path)
        self.connect_layout.addWidget(self.connect_widget)

        # Select between drivers
        self.drivers_layout = QtGui.QVBoxLayout()

        self.app_buttons = []
        for i, app in enumerate(self.instrument_list):
            self.app_buttons.append(self.set_button(''))
            self.drivers_layout.addWidget(self.app_buttons[i], 1, QtCore.Qt.AlignCenter)
            def make_callback(i):
                return lambda : self.app_onclick(i)
            self.app_buttons[i].clicked.connect(make_callback(i))
        self.update_buttons()

        # Left Layout


        # Right layout
        self.right_layout.addLayout(self.connect_layout)
        self.right_layout.addLayout(self.drivers_layout)
        self.right_layout.addStretch(1)
        self.right_frame = QtGui.QFrame(self)
        self.right_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.right_frame.setLayout(self.right_layout)

        # Add layouts to main layout
        self.lay.addLayout(self.left_layout, 1)
        self.lay.addWidget(self.right_frame)
        self.setLayout(self.lay)

    def update(self):
        pass

    def set_button(self, name):
        button = QtGui.QPushButton(name)
        button.setStyleSheet('QPushButton {color: green;}')
        button.setFixedWidth(200)
        button.setFixedHeight(150)
        return button

    def update_buttons(self):
        for i, button in enumerate(self.app_buttons):
            button.setText(self.parent.app_list[i].capitalize() +
                           (' not available ' if (self.instrument_list[i] == '') else ''))

    def app_onclick(self, app_idx):
        app = self.app_list[app_idx]
        instrument = self.instrument_list[app_idx]
        if instrument != '':
            QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
            self.connect_widget.client = connect(self.connect_widget.host, name=instrument)
            driver = globals()[app.capitalize()](self.connect_widget.client)
            driver.init()
            QtGui.QApplication.restoreOverrideCursor()
            index = self.parent.stacked_widget.addWidget(globals()[app.capitalize()+'Widget'](driver, self.parent))
            self.parent.stacked_widget.setCurrentIndex(index)
