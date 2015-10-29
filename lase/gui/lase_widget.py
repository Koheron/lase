# -*- coding: utf-8 -*-


from pyqtgraph.Qt import QtGui, QtCore
from monitor_widget import MonitorWidget
from laser_widget import LaserWidget
from dac_widget import DacWidget
import os

class LaseWidget(QtGui.QWidget):
    """
    This widget serves as the base widget for `OscilloWidget` and 
    `SpectrumWidget`.
    
    """
    
    def __init__(self, driver, parent):
        super(LaseWidget, self).__init__()
    
        self.data_path = parent.data_path
        self.img_path = parent.img_path
        self.opened = True
        self.frame_rate = 0
        self.show_right_panel = True
        self.left_arrow = QtGui.QIcon(os.path.join(self.img_path, 'left_arrow.png'))
        self.right_arrow = QtGui.QIcon(os.path.join(self.img_path, 'right_arrow.png'))
        
        self.driver = driver
        
        
        # Initialize driver
        self.driver.set_dac()
        self.power_offset = self.driver.get_laser_power()
  
        # Layout
        self.init_layout()
        
        # Monitor widget
        self.monitor_widget = MonitorWidget(self. driver)

        # Plot widget   

        # Laser Widget
        self.laser_widget = LaserWidget(self.driver)       
        self.laser_box = QtGui.QGroupBox("Laser control")
        self.laser_box.setLayout(self.laser_widget.layout)

        # DAC Widgets
        self.dac_tabs = QtGui.QTabWidget()
        self.dac_wid = []
        n_dac = 2
        for i in range(n_dac):
            self.dac_wid.append(DacWidget(self.driver, index = i))
            self.dac_wid[i].data_updated_signal.connect(self.update_dac)
            self.dac_tabs.addTab(self.dac_wid[i],"DAC "+str(i+1))

        self.left_panel_layout.addLayout(self.monitor_widget.layout)
        self.left_panel_layout.addWidget(self.laser_box)   
        self.left_panel_layout.addWidget(self.dac_tabs)

        # Show/Hide button    
        self.right_panel_button = QtGui.QPushButton()
        self.right_panel_button.setStyleSheet('QPushButton {color: green;}')
        self.right_panel_button.setIcon(self.right_arrow)
        self.right_panel_button.setIconSize(QtCore.QSize(30,30))
        
        self.right_panel = QtGui.QVBoxLayout()         
        self.right_panel_widget = QtGui.QWidget()
        
        self.lay.addLayout(self.left_panel_layout,1)        
        self.lay.addWidget(self.right_panel_button)
        self.lay.addWidget(self.right_panel_widget)
               
        # Connections
        self.right_panel_button.clicked.connect(self.right_panel_connect)
        
    def init_layout(self):
        self.lay = QtGui.QHBoxLayout()
        self.setLayout(self.lay)
        # Sub Layout
        self.left_panel_layout = QtGui.QVBoxLayout()       

    def update(self):
        self.driver.update() # Used in simulation
        self.monitor_widget.update(frame_rate=self.frame_rate)

    def update_dac(self, index):
        self.driver.dac[index,:] = self.dac_wid[index].data
        self.driver.set_dac()
        self.refresh_dac()
        
    def refresh_dac():              # Abstract method, defined by convention only
        raise NotImplementedError("Subclass must implement abstract method")
        
    def right_panel_connect(self):
        self.show_right_panel = not self.show_right_panel
        self.right_panel_widget.setVisible(self.show_right_panel)
        if self.show_right_panel:            
            self.right_panel_button.setIcon(self.right_arrow)
        else:
            self.right_panel_button.setIcon(self.left_arrow)


        
