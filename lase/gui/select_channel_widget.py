# -*- coding: utf-8 -*-

from pyqtgraph.Qt import QtGui, QtCore

class SelectChannelWidget(QtGui.QWidget):
    def __init__(self, plot_widget):
        super(SelectChannelWidget, self).__init__()
        
        self.plot_widget = plot_widget

        self.layout = QtGui.QGridLayout()        
        
        self.adc_checkbox = []
        for i in range(2):
            self.adc_checkbox.append(QtGui.QCheckBox('ADC '+str(i+1), self))
            self.adc_checkbox[i].setCheckState(QtCore.Qt.Checked)
            self.layout.addWidget(self.adc_checkbox[i],0,i,QtCore.Qt.AlignCenter)
            
        self.dac_checkbox = []
        for i in range(2):
            self.dac_checkbox.append(QtGui.QCheckBox('DAC '+str(i+1), self))
            self.dac_checkbox[i].setCheckState(QtCore.Qt.Unchecked)
            self.layout.addWidget(self.dac_checkbox[i],1,i,QtCore.Qt.AlignCenter)
            
        # Connections
        self.adc_checkbox[0].stateChanged.connect(lambda: self.show_adc(0))
        self.adc_checkbox[1].stateChanged.connect(lambda: self.show_adc(1))  
        self.dac_checkbox[0].stateChanged.connect(lambda: self.show_dac(0))
        self.dac_checkbox[1].stateChanged.connect(lambda: self.show_dac(1))
       
    def show_adc(self, index):
        if self.adc_checkbox[index].isChecked():    
            self.plot_widget.show_adc[index] = True
        else:
            self.plot_widget.show_adc[index] = False
        self.plot_widget.dataItem[index].setVisible(self.plot_widget.show_adc[index])        
        self.plot_widget.enableAutoRange()

    def show_dac(self, index):
        if self.dac_checkbox[index].isChecked():    
            self.plot_widget.show_dac[index] = True
        else:
            self.plot_widget.show_dac[index] = False
        self.plot_widget.dataItem[2+index].setVisible(self.plot_widget.show_dac[index])
        self.plot_widget.enableAutoRange()
        
    def uncheck_all(self):
        for i in range(2):
            self.adc_checkbox[i].setCheckState(QtCore.Qt.Unchecked)
            self.dac_checkbox[i].setCheckState(QtCore.Qt.Unchecked)
    