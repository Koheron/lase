# -*- coding: utf-8 -*-

from pyqtgraph.Qt import QtGui, QtCore

class SelectChannelWidget(QtGui.QWidget):
    def __init__(self, plot_widget):
        super(SelectChannelWidget, self).__init__()
        
        self.plot_widget = plot_widget

        self.layout = QtGui.QGridLayout()        
        
        self.adc_checkbox = []
        self.add_checkbox(self.adc_checkbox, 0, 'ADC', check_state=QtCore.Qt.Checked)

        self.dac_checkbox = []
        self.add_checkbox(self.dac_checkbox, 1, 'DAC')
        
        self.adc_checkbox[0].stateChanged.connect(lambda: self.show_adc(0))
        self.adc_checkbox[1].stateChanged.connect(lambda: self.show_adc(1))
        self.dac_checkbox[0].stateChanged.connect(lambda: self.show_dac(0))
        self.dac_checkbox[1].stateChanged.connect(lambda: self.show_dac(1))

    def add_checkbox(self, checkbox, y_pos, text, check_state=QtCore.Qt.Unchecked):
        for i in range(2):
            checkbox.append(QtGui.QCheckBox(text +' '+str(i+1), self))
            checkbox[i].setCheckState(check_state)
            self.layout.addWidget(checkbox[i], y_pos, i, QtCore.Qt.AlignCenter)

    def show_adc(self, index):
        self.plot_widget.show_adc[index] = self.adc_checkbox[index].isChecked()
        self.plot_widget.dataItem[index].setVisible(self.plot_widget.show_adc[index])        

    def show_dac(self, index):
        self.plot_widget.show_dac[index] = self.dac_checkbox[index].isChecked()
        self.plot_widget.dataItem[2+index].setVisible(self.plot_widget.show_dac[index])
        
    def uncheck_all(self):
        for i in range(2):
            self.adc_checkbox[i].setCheckState(QtCore.Qt.Unchecked)
            self.dac_checkbox[i].setCheckState(QtCore.Qt.Unchecked)

    def save_as_h5(self, f):
        select_channel_grp = f.create_group('select_channel')
        adc_checkbox_dset = f.create_dataset('select_channel/adc_checkbox', (2,), dtype=bool)
        dac_checkbox_dset = f.create_dataset('select_channel/dac_checkbox', (2,), dtype=bool)

        for i in range(2):
            adc_checkbox_dset[i] = self.adc_checkbox[i].isChecked()
            dac_checkbox_dset[i] = self.dac_checkbox[i].isChecked()

    def save_as_zip(self, _dict, dest=''):
        _dict['select_channel'] = {
          'adc_checkbox': [self.adc_checkbox[0].isChecked(), self.adc_checkbox[1].isChecked()],
          'dac_checkbox': [self.dac_checkbox[0].isChecked(), self.dac_checkbox[1].isChecked()]
        }