# -*- coding: utf-8 -*-

from pyqtgraph.Qt import QtGui, QtCore
from .monitor_widget import MonitorWidget
from .plot_widget import PlotWidget
from .laser_widget import LaserWidget
from .dac_widget import DacWidget

import os

class BaseWidget(QtGui.QWidget):
    """ This widget serves as the base widget for `OscilloWidget` and
        `SpectrumWidget`.
    """

    def __init__(self, driver, parent):
        super(BaseWidget, self).__init__()
    
        self.data_path = parent.data_path
        self.img_path = parent.img_path
        self.opened = True
        self.frame_rate = 0
        self.show_right_panel = True

        # Icons
        self.left_arrow_icon = QtGui.QIcon(os.path.join(self.img_path, 'left_arrow.png'))
        self.right_arrow_icon = QtGui.QIcon(os.path.join(self.img_path, 'right_arrow.png'))

        self.zoom_x_icon = QtGui.QIcon(os.path.join(self.img_path, 'zoom_x.png'))
        self.zoom_y_icon = QtGui.QIcon(os.path.join(self.img_path, 'zoom_y.png'))

        self.autoscale_icon = QtGui.QIcon(os.path.join(self.img_path, 'autoscale.png'))

        self.driver = driver

        # Initialize driver
        self.driver.set_dac()
        self.power_offset = self.driver.get_laser_power()

        # Layout
        self.init_layout()

        # Laser Widget
        self.laser_widget = LaserWidget(self.driver)
        self.laser_box = QtGui.QGroupBox("Laser control")
        self.laser_box.setLayout(self.laser_widget.layout)
        
        # Monitor widget
        self.monitor_widget = MonitorWidget(self.driver, self.laser_widget)

        self.plot_widget = PlotWidget(name="data")

        # DAC Widgets
        self.dac_tabs = QtGui.QTabWidget()
        self.dac_wid = []
        n_dac = 2
        for i in range(n_dac):
            self.dac_wid.append(DacWidget(self.driver, index=i))
            self.dac_wid[i].data_updated_signal.connect(self.update_dac)
            self.dac_tabs.addTab(self.dac_wid[i], "DAC " + str(i + 1))

        self.left_panel_layout.addLayout(self.monitor_widget.layout)
        self.left_panel_layout.addWidget(self.laser_box)
        self.left_panel_layout.addWidget(self.dac_tabs)

        # Toolbar
        self.toolbar_layout = QtGui.QVBoxLayout()
        
        self.right_panel_button = QtGui.QPushButton()
        self.right_panel_button.setStyleSheet('QPushButton {color: green;}')
        self.right_panel_button.setIcon(self.right_arrow_icon)
        self.right_panel_button.setIconSize(QtCore.QSize(30, 30))

        self.zoom_button = QtGui.QPushButton()
        self.zoom_button.setStyleSheet('QPushButton {color: green;}')
        self.zoom_button.setIcon(self.zoom_y_icon)
        self.zoom = 'Y'
        self.zoom_button.setIconSize(QtCore.QSize(30,30))

        self.autoscale_button = QtGui.QPushButton()
        self.autoscale_button.setStyleSheet('QPushButton {color: green;}')
        self.autoscale_button.setIcon(self.autoscale_icon)
        self.autoscale_button.setIconSize(QtCore.QSize(30,30))

        self.right_panel = QtGui.QVBoxLayout()
        self.right_panel_widget = QtGui.QWidget()

        self.toolbar_layout.addWidget(self.right_panel_button)
        self.toolbar_layout.addWidget(self.zoom_button)
        self.toolbar_layout.addWidget(self.autoscale_button)
        self.toolbar_layout.addStretch(1)

        self.lay.addLayout(self.left_panel_layout, 1)
        self.lay.addLayout(self.toolbar_layout)

        self.lay.addWidget(self.right_panel_widget)

        self.left_panel_layout.insertWidget(1, self.plot_widget, 1)

        # Connections
        self.right_panel_button.clicked.connect(self.right_panel_connect)
        self.zoom_button.clicked.connect(self.toggle_zoom)
        self.autoscale_button.clicked.connect(self.autoscale)

    def init_layout(self):
        self.lay = QtGui.QHBoxLayout()
        self.setLayout(self.lay)
        # Sub Layout
        self.left_panel_layout = QtGui.QVBoxLayout()

    def update(self):
        self.driver.update()  # Used in simulation
        self.monitor_widget.update(frame_rate=self.frame_rate)

    def update_dac(self, index):
        self.driver.dac[index, :] = self.dac_wid[index].data
        self.driver.set_dac()
        self.refresh_dac()
        
    def refresh_dac(self):
        """ Refresh the DAC plots

            Abstract method, defined by convention only
        """
        pass

    def right_panel_connect(self):
        self.show_right_panel = not self.show_right_panel
        self.right_panel_widget.setVisible(self.show_right_panel)
        if self.show_right_panel:
            self.right_panel_button.setIcon(self.right_arrow_icon)
        else:
            self.right_panel_button.setIcon(self.left_arrow_icon)

    def toggle_zoom(self):
        if self.zoom == 'Y':
            self.zoom_button.setIcon(self.zoom_x_icon)
            self.plot_widget.setMouseEnabled(x=True, y=False)
            self.zoom = 'X'
        else:
            self.zoom_button.setIcon(self.zoom_y_icon)
            self.plot_widget.setMouseEnabled(x=False, y=True)
            self.zoom = 'Y'

    def autoscale(self):
        self.plot_widget.enableAutoRange()
