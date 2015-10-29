# -*- coding: utf-8 -*-

from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg

class CursorWidget(QtGui.QWidget):

    def __init__(self, plot_widget):
        super(CursorWidget, self).__init__()
        
        self.plot_widget = plot_widget
        
        self.cursor = [False, False]    

        self.position_layout = QtGui.QVBoxLayout()
        self.cursor_1_layout = QtGui.QVBoxLayout()
        self.cursor_2_layout = QtGui.QVBoxLayout()
        self.delta_layout = QtGui.QVBoxLayout()        
        self.Delta_layout = QtGui.QHBoxLayout()
        self.cursor_box_layout = QtGui.QHBoxLayout()  
        self.global_layout = QtGui.QVBoxLayout()
        self.auto_scale_layout = QtGui.QHBoxLayout()
        
        self.layout = QtGui.QVBoxLayout()
        

        self.position_box = QtGui.QGroupBox('Position')
        self.position_box.setAlignment(5)
        self.cursor_1_box = QtGui.QGroupBox('Cursor 1')
        self.cursor_1_box.setAlignment(5)
        self.cursor_2_box = QtGui.QGroupBox('Cursor 2')
        self.cursor_2_box.setAlignment(5)
        self.delta_box = QtGui.QGroupBox('Delta')
        self.delta_box.setAlignment(5)
        
        # Cursor
        
        self.cursor_button = QtGui.QPushButton('ON')      
        self.cursor_button.setStyleSheet('QPushButton {color: green;}')
        self.cursor_button.setCheckable(True)
        self.cursor_X = QtGui.QLabel('X')
        self.cursor_X.setAlignment(QtCore.Qt.AlignCenter) 
        self.cursor_1_X = QtGui.QLabel('')
        self.cursor_1_X.setAlignment(QtCore.Qt.AlignCenter) 
        self.cursor_2_X = QtGui.QLabel('')
        self.cursor_2_X.setAlignment(QtCore.Qt.AlignCenter) 
        self.cursor_Y = QtGui.QLabel('Y')
        self.cursor_Y.setAlignment(QtCore.Qt.AlignCenter) 
        self.cursor_1_Y = QtGui.QLabel('')
        self.cursor_1_Y.setAlignment(QtCore.Qt.AlignCenter) 
        self.cursor_2_Y = QtGui.QLabel('')
        self.cursor_2_Y.setAlignment(QtCore.Qt.AlignCenter) 
        
        self.delta_X = QtGui.QLabel('X')
        self.delta_X.setAlignment(QtCore.Qt.AlignCenter) 
        self.delta_Y = QtGui.QLabel('Y')
        self.delta_Y.setAlignment(QtCore.Qt.AlignCenter) 
        
        #Cursor
               
        self.vLine_1 = pg.InfiniteLine(angle=90, movable=False)
        self.hLine_1 = pg.InfiniteLine(angle=0, movable=False)
        self.plot_widget.addItem(self.vLine_1, ignoreBounds=True)
        self.plot_widget.addItem(self.hLine_1, ignoreBounds=True)
        self.vLine_1.setVisible(self.cursor[0])
        self.hLine_1.setVisible(self.cursor[0])
        
        self.vLine_2 = pg.InfiniteLine(angle=90, movable=False, pen=(3,4))
        self.hLine_2 = pg.InfiniteLine(angle=0, movable=False, pen=(3,4))
        self.plot_widget.addItem(self.vLine_2, ignoreBounds=True)
        self.plot_widget.addItem(self.hLine_2, ignoreBounds=True)
        self.vLine_2.setVisible(self.cursor[1])
        self.hLine_2.setVisible(self.cursor[1])
        self.view_box = self.plot_widget.getViewBox()        
        
        self.layout.addWidget(self.cursor_button)
        
        self.position_layout.addWidget(self.cursor_X)
        self.position_layout.addWidget(self.cursor_Y)
        
        self.cursor_1_layout.addWidget(self.cursor_1_X)
        self.cursor_1_layout.addWidget(self.cursor_1_Y)
        
        self.cursor_2_layout.addWidget(self.cursor_2_X)
        self.cursor_2_layout.addWidget(self.cursor_2_Y)
        
        self.position_box.setLayout(self.position_layout)
        self.cursor_1_box.setLayout(self.cursor_1_layout)
        self.cursor_2_box.setLayout(self.cursor_2_layout)
        
        self.cursor_box_layout.addWidget(self.position_box)        
        self.cursor_box_layout.addWidget(self.cursor_1_box)
        self.cursor_box_layout.addWidget(self.cursor_2_box)
        
        self.delta_layout.addWidget(self.delta_X)
        self.delta_layout.addWidget(self.delta_Y)
        self.delta_box.setLayout(self.delta_layout)
        
        self.Delta_layout.addStretch(1)
        self.Delta_layout.addWidget(self.delta_box)
        self.Delta_layout.addStretch(1)       
        
        self.delta_box.setVisible(self.cursor[1])
        
        self.layout.addLayout(self.cursor_box_layout)   
        self.layout.addLayout(self.Delta_layout)
        
        self.setLayout(self.layout)
        
        # Connections
        self.cursor_button.clicked.connect(self.cursor_on)
        self.plot_widget.scene().sigMouseMoved.connect(self.mouseMoved)
        self.plot_widget.scene().sigMouseClicked.connect(self.mouseClicked)
        
    def auto_scale(self):
            self.plot_widget.enableAutoRange()        
        
    def cursor_on(self):        
        self.cursor[0] = not self.cursor[0]
        if self.cursor[0]:
            self.cursor_button.setStyleSheet('QPushButton {color: red;}')
            self.cursor_button.setText('OFF')
            self.set_visible()
        else:
            self.cursor[1] = False
            self.cursor_button.setStyleSheet('QPushButton {color: green;}')
            self.cursor_button.setText('ON')
            self.set_visible()
            self.reset_text()
            self.delta_box.setVisible(False)
      
    def mouseMoved(self, pos):
        if self.plot_widget.sceneBoundingRect().contains(pos):
            self.mousePoint = self.view_box.mapSceneToView(pos)
            self.vLine_1.setPos(self.mousePoint.x())
            self.hLine_1.setPos(self.mousePoint.y())
            if self.cursor[0]:
                if 1e-2 < np.abs(self.mousePoint.x()) < 1e3:
                    self.cursor_1_X.setText('{:.2f}'.format(self.mousePoint.x()))
                else:
                    self.cursor_1_X.setText('%.2e'%(self.mousePoint.x()))
                if 1e-2 < np.abs(self.mousePoint.y()) < 1e3:
                    self.cursor_1_Y.setText('{:.2f}'.format(self.mousePoint.y()))
                else:
                    self.cursor_1_Y.setText('%.2e'%(self.mousePoint.y()))
                if self.cursor[1] == True:
                    if 1e-2 < np.abs(self.mousePoint.x() - self.cursor_2_x) < 1e3:
                        self.delta_X.setText('X   ' + '{:.2f}'.format(self.mousePoint.x() - self.cursor_2_x))
                    else:
                        self.delta_X.setText('X   ' + '%.2e'%(self.mousePoint.x() - self.cursor_2_x))                        
                    if 1e-2 < np.abs(self.mousePoint.y() - self.cursor_2_y) < 1e3:
                        self.delta_Y.setText('Y   ' + '{:.2f}'.format(self.mousePoint.y() - self.cursor_2_y))
                    else:
                        self.delta_Y.setText('Y   ' + '%.2e'%(self.mousePoint.y() - self.cursor_2_y))
                        
        else:
            self.reset_text()
            self.delta_X.setText('X') 
            self.delta_Y.setText('Y') 
            self.delta_box.setVisible(False)
            
    def mouseClicked(self, evt):
        if self.cursor[0]:
            self.cursor_2_x = self.mousePoint.x()
            self.cursor_2_y = self.mousePoint.y()
            self.vLine_2.setPos(self.mousePoint.x())
            self.hLine_2.setPos(self.mousePoint.y())
            self.cursor[1] = True
            self.delta_box.setVisible(True)
            self.vLine_2.setVisible(self.cursor[1])
            self.hLine_2.setVisible(self.cursor[1])
            if 1e-2 < np.abs(self.mousePoint.x()) < 1e3:
                self.cursor_2_X.setText('{:.2f}'.format(self.mousePoint.x()))
            else:
                self.cursor_2_X.setText('%.2e'%(self.mousePoint.x()))
            if 1e-2 < np.abs(self.mousePoint.y()) < 1e3:
                self.cursor_2_Y.setText('{:.2f}'.format(self.mousePoint.y()))
            else:
                self.cursor_2_Y.setText('%.2e'%(self.mousePoint.y()))
            
    def set_visible(self):
        self.vLine_1.setVisible(self.cursor[0])
        self.hLine_1.setVisible(self.cursor[0])
        self.vLine_2.setVisible(self.cursor[1])
        self.hLine_2.setVisible(self.cursor[1])
            
    def reset_text(self):
        self.cursor_1_X.setText('')
        self.cursor_1_Y.setText('')
        self.cursor_2_X.setText('')
        self.cursor_2_Y.setText('')
