from pyqtgraph.Qt import QtGui, QtCore

import time
import h5py
import numpy as np

class SaveWidget(QtGui.QWidget):
    def __init__(self, oscillo_widget):
        super(SaveWidget, self).__init__()
        self.layout = QtGui.QVBoxLayout()
        self.oscillo_widget = oscillo_widget

        self.save_button = QtGui.QPushButton()
        self.save_button.setStyleSheet('QPushButton {color: green;}')
        self.save_button.setText('Save')
        self.layout.addWidget(self.save_button)
        self.save_button.clicked.connect(self.save_data)

    def save_data(self):
        filename = QtGui.QFileDialog.getSaveFileName(self, 'Dialog Title')

        if filename:
            with h5py.File(unicode(filename), 'w') as f:
                self.save_metadata(f)
                self.oscillo_widget.stats_widget.save_as_h5(f)
                self.oscillo_widget.math_widget.save_as_h5(f)
                self.oscillo_widget.select_channel_widget.save_as_h5(f)
                self.oscillo_widget.save_as_h5(f)
                self.oscillo_widget.monitor_widget.save_as_h5(f)
                self.oscillo_widget.laser_widget.save_as_h5(f)

    def save_metadata(self, f):
        metadata_grp = f.create_group('h5_file_metadata')
        metadata_dset = f.create_dataset('h5_file_metadata/data', (0,), dtype='f')
        metadata_dset.attrs['Date'] = unicode(time.strftime("%d/%m/%Y"))
        metadata_dset.attrs['Time'] = unicode(time.strftime("%H:%M:%S"))
        # TODO save bitstream_id, server commit
