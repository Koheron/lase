from pyqtgraph.Qt import QtGui, QtCore

import h5py

class SaveWidget(QtGui.QWidget):
    def __init__(self, stats_widget):
        super(SaveWidget, self).__init__()
        self.layout = QtGui.QVBoxLayout()
        self.stats_widget = stats_widget

        # Save 
        self.save_button = QtGui.QPushButton()
        self.save_button.setStyleSheet('QPushButton {color: green;}')
        self.save_button.setText('Save')
        self.save_button.setCheckable(True)
        self.layout.addWidget(self.save_button)
        self.save_button.clicked.connect(self.save_data)

    def save_data(self):
        filename = QtGui.QFileDialog.getSaveFileName(self, 'Dialog Title')

        if filename:
            with h5py.File(unicode(filename), 'w') as f:
                self._save_stats(f)

    def _save_stats(self, f):
        stats_grp = f.create_group('stats')
        average_dset = f.create_dataset('stats/average', (self.stats_widget.n_channels,), dtype='f')
        average_dset[...] = self.stats_widget.average

        peak_peak_dset = f.create_dataset('stats/peak_peak', (self.stats_widget.n_channels,), dtype='f')
        peak_peak_dset[...] = self.stats_widget.amplitude

        amplitude_rms_dset = f.create_dataset('stats/amplitude_rms', (self.stats_widget.n_channels,), dtype='f')
        amplitude_rms_dset[...] = self.stats_widget.amplitude_rms