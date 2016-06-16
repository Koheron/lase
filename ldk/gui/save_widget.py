from pyqtgraph.Qt import QtGui, QtCore

import os
import uuid
import time
import json
import zipfile
import shutil
import numpy as np

try:
    import h5py
    HAS_HDF5 = True
except ImportError:
    HAS_HDF5 = False

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
        if HAS_HDF5:
            file_filter = 'zip (*.zip *.);; hdf5 (*.h5 *.hdf5 *.)'
        else:
            file_filter = 'zip (*.zip *.)'

        filename = unicode(QtGui.QFileDialog.getSaveFileName(self, 'Save', '', filter =file_filter))
        extension = os.path.splitext(filename)[1]

        if (extension == '.h5' or extension == '.hdf5') and HAS_HDF5:
            self.dump_to_h5(filename)
        elif extension == '.zip':
            self.dump_to_zip(filename)
        else:
            raise TypeError('Unknown file extension')

    def dump_to_h5(self, filename):
        with h5py.File(filename, 'w') as f:
            self.save_metadata_as_h5(f)
            self.oscillo_widget.stats_widget.save_as_h5(f)
            self.oscillo_widget.math_widget.save_as_h5(f)
            self.oscillo_widget.select_channel_widget.save_as_h5(f)
            self.oscillo_widget.save_as_h5(f)
            self.oscillo_widget.monitor_widget.save_as_h5(f)
            self.oscillo_widget.laser_widget.save_as_h5(f)

    def dump_to_zip(self, filename):
        tmp_dir = os.path.join(os.path.dirname(filename), unicode(uuid.uuid4()))
        os.makedirs(tmp_dir)

        _dict = {} # Contains elements to be dumped in json
        _dict['metadata'] = self.metadata()

        self.oscillo_widget.stats_widget.save_as_zip(_dict, tmp_dir)
        self.oscillo_widget.math_widget.save_as_zip(_dict, tmp_dir)
        self.oscillo_widget.select_channel_widget.save_as_zip(_dict, tmp_dir)
        self.oscillo_widget.save_as_zip(_dict, tmp_dir)
        self.oscillo_widget.monitor_widget.save_as_zip(_dict, tmp_dir)
        self.oscillo_widget.laser_widget.save_as_zip(_dict, tmp_dir)

        with open(os.path.join(tmp_dir, 'data.json'), 'w') as f:
            json.dump(_dict, f)

        zipf = zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED)
        for root, dirs, files in os.walk(tmp_dir):
            for file in files:
                zipf.write(os.path.join(root, file), file)

        shutil.rmtree(tmp_dir)

    def save_metadata_as_h5(self, f):
        metadata_grp = f.create_group('h5_file_metadata')
        metadata_dset = f.create_dataset('h5_file_metadata/data', (0,), dtype='f')
        metadata = self.metadata()
        metadata_dset.attrs['Date'] = unicode(metadata['Date'])
        metadata_dset.attrs['Time'] = unicode(metadata['Time'])

    def metadata(self):
        # TODO save bitstream_id, server commit
        return {
          'Date': time.strftime("%d/%m/%Y"),
          'Time': time.strftime("%H:%M:%S")
        }