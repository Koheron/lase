# -*- coding: utf-8 -*-

from pyqtgraph.Qt import QtGui, QtCore 
from connect_widget import ConnectWidget
from PyQt4.QtWebKit import QWebView
from ..drivers import Oscillo, Spectrum
from ..drivers import OscilloSimu, SpectrumSimu
from oscillo_widget import OscilloWidget
from spectrum_widget import SpectrumWidget
import time
import os


class WelcomeWidget(QtGui.QWidget):
    """
    This widget allows to connect to one of the available drivers.
    
    Note:
        When the connection is established, the drivers are `Oscillo` and 
        `Spectrum`. Otherwise the drivers are in simulation mode (`OscilloSimu`
        and `SpectrumSimu`). A web page is also displayed on the left side.
    
    """
    
    def __init__(self, parent, ip_path):
        super(WelcomeWidget, self).__init__()
        
        self.parent = parent
        self.ip_path = ip_path
        self.lay = QtGui.QHBoxLayout()
        self.left_layout = QtGui.QVBoxLayout()
        self.right_layout = QtGui.QVBoxLayout()    
        self.ip_layout = QtGui.QVBoxLayout()
        self.stacked_widget_layout = QtGui.QVBoxLayout()
        
        self.opened = True
        self.select_opened = True        
        
        self.setLayout(self.lay)
        
        self.oscillo_button = self.set_button('Oscillo (Simu)')
        self.spectrum_button = self.set_button('Spectrum (Simu)')
      
        self.ip_box = QtGui.QGroupBox("IP address")
        self.connect_widget = ConnectWidget(self, self.ip_path)
        self.ip_layout.addWidget(self.connect_widget)
        self.ip_box.setLayout(self.ip_layout)     
       
        # Create and fill a QWebView
        self.view = QWebView()
        
        self.view.load(QtCore.QUrl.fromLocalFile(
                       os.path.join(self.parent.static_path, 'welcome.html')))        
       
        self.left_layout.addWidget(self.view)

        self.right_layout.addWidget(self.ip_box,0)
        self.right_layout.addWidget(self.oscillo_button,1,QtCore.Qt.AlignCenter)
        self.right_layout.addWidget(self.spectrum_button,1,QtCore.Qt.AlignCenter)
        self.right_layout.addStretch(1)
        
        self.right_frame = QtGui.QFrame(self)
        self.right_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        
        self.right_frame.setLayout(self.right_layout)
        self.lay.addLayout(self.left_layout, 1)
        self.lay.addWidget(self.right_frame)
        
        # Connections
        self.oscillo_button.clicked.connect(self.oscillo_on)
        self.spectrum_button.clicked.connect(self.spectrum_on)
       
    def update(self):
        pass
    
    def set_button(self, name):
        button = QtGui.QPushButton(name)
        button.setStyleSheet('QPushButton {color: green;}')
        button.setFixedWidth(200)
        button.setFixedHeight(150)
        return button
        
    def connected(self):
        self.oscillo_button.setText('Oscillo')
        self.spectrum_button.setText('Spectrum')
        
    def disconnected(self):
        self.oscillo_button.setText('Oscillo (Simu)')
        self.spectrum_button.setText('Spectrum (Simu)')
        
    def oscillo_on(self):
        if self.connect_widget.is_connected:
            time.sleep(0.01)
            self.connect_widget.ssh.load_pl(
                os.path.join(self.parent.bitstreams_path, 'oscillo.bit'))
            time.sleep(0.01)        
            driver = Oscillo(self.connect_widget.client, current_mode='pwm')
        else:
            driver = OscilloSimu()
        index = self.parent.stacked_widget.addWidget(
            OscilloWidget(driver, self.parent))
        self.parent.stacked_widget.setCurrentIndex(index)
        
    def spectrum_on(self):
        if self.connect_widget.is_connected:
            time.sleep(0.01)
            self.connect_widget.ssh.load_pl(
                os.path.join(self.parent.bitstreams_path, 'spectrum.bit'))
            time.sleep(0.01)        
            driver = Spectrum(self.connect_widget.client, current_mode='pwm')
        else:
            driver = SpectrumSimu()
        index = self.parent.stacked_widget.addWidget(
            SpectrumWidget(driver, self.parent))
        self.parent.stacked_widget.setCurrentIndex(index)
        

