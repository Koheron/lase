# -*- coding: utf-8 -*-

from pyqtgraph.Qt import QtGui
import os
import json
import glob
import numpy as np

class SaveWidget(QtGui.QWidget):

    def __init__(self, parent, loadname=''):
        super(SaveWidget, self).__init__()
        
        self.parent = parent
        self.data_path = parent.data_path
        
        self.save_line = QtGui.QLineEdit(self)
        self.save_button = QtGui.QPushButton(self)
        self.save_button.setText('Save')
        
        self.load_combo = QtGui.QComboBox(self)         
        self.load_combo.addItem('') 
        for file in glob.glob(os.path.join(self.data_path,'*.json')): 
            [filepath, filename] = os.path.split(file)               
            self.load_combo.addItem(str(filename).replace('.json',''))
        self.load_button = QtGui.QPushButton()
        self.load_button.setText('Load')
        
        # Layout
        self.layout = QtGui.QVBoxLayout()        
        self.save_file_layout = QtGui.QHBoxLayout()
        self.save_file_layout.addWidget(self.save_line)    
        self.save_file_layout.addWidget(self.save_button)  
        self.load_layout = QtGui.QHBoxLayout()
        self.load_layout.addWidget(self.load_combo,1)    
        self.load_layout.addWidget(self.load_button)        
        self.layout.addLayout(self.save_file_layout)        
        self.layout.addLayout(self.load_layout)
        
        # Connections
        self.save_button.clicked.connect(self.save)
        self.load_button.clicked.connect(self.load)

    def save(self):
        if self.save_line.text() =='' :
            return
        else:
            parameters = {}
            parameters['laser_current'] = str(self.parent.laser_widget.laser_current)
            for i in range(len(self.parent.dac_wid)):
                parameters['mod_amp_'+str(i+1)] = str(self.parent.dac_wid[i].mod_amp)
                parameters['freq_'+str(i+1)] = str(self.parent.dac_wid[i].freq)
                parameters['waveform_index_'+str(i+1)] = str(self.parent.dac_wid[i].waveform_index)
            with open(os.path.join(self.data_path, str(self.save_line.text()) + '.json'), 'w') as fp:
                json.dump(parameters, fp)
            self.load_combo.addItem(self.save_line.text())
            data = np.ones((self.parent.driver.sampling.n,4))
            data[:,0] = self.parent.driver.adc[0,:]
            data[:,1] = self.parent.driver.adc[1,:]
            data[:,2] = self.parent.driver.dac[0,:]
            data[:,3] = self.parent.driver.dac[1,:]
            np.savetxt(os.path.join(self.data_path, str(self.save_line.text()) + '.csv'), data, delimiter=',', header='adc 1 ,adc 2 ,dac 1 ,dac 2')
            self.save_line.setText('')
        
    def load(self):
        if self.load_combo.currentText() == '':
            return
        else:
            json_data=open(os.path.join(self.data_path, str(self.load_combo.currentText()) + '.json')).read()    
            parameters = json.loads(json_data)
            
            self.parent.laser_widget.laser_current = float(parameters['laser_current'])
            self.parent.laser_widget.slider.spin.setValue(self.parent.laser_widget.laser_current)
            self.parent.laser_widget.change_current(self.parent.laser_widget.laser_current)
            
            for i in range(len(self.parent.dac_wid)):
                self.parent.dac_wid[i].waveform_index = int(parameters['waveform_index_'+str(i+1)])
                self.parent.dac_wid[i].waveform_list.list[self.parent.dac_wid[i].waveform_index].setChecked(True)      
                self.parent.dac_wid[i].mod_amp = float(parameters['mod_amp_'+str(i+1)])
                self.parent.dac_wid[i].freq = float(parameters['freq_'+str(i+1)])
                
                self.parent.dac_wid[i].freq_slider.spin.setValue(self.parent.dac_wid[i].freq)
                self.parent.dac_wid[i].mod_amp_slider.spin.setValue(self.parent.dac_wid[i].mod_amp)
                
                self.parent.dac_wid[i].change_freq(self.parent.dac_wid[i].freq)
                self.parent.dac_wid[i].change_mod_amp(self.parent.dac_wid[i].mod_amp)
                
                self.parent.dac_wid[i].update_data()
