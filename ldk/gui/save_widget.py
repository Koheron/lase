from pyqtgraph.Qt import QtGui, QtCore

import h5py

class SaveWidget(QtGui.QWidget):
    def __init__(self, stats_widget, math_widget, select_channel_widget):
        super(SaveWidget, self).__init__()
        self.layout = QtGui.QVBoxLayout()
        self.stats_widget = stats_widget
        self.math_widget = math_widget
        self.select_channel_widget = select_channel_widget

        self.n_channels = self.stats_widget.n_channels

        self.save_button = QtGui.QPushButton()
        self.save_button.setStyleSheet('QPushButton {color: green;}')
        self.save_button.setText('Save')
        self.layout.addWidget(self.save_button)
        self.save_button.clicked.connect(self.save_data)

    def save_data(self):
        filename = QtGui.QFileDialog.getSaveFileName(self, 'Dialog Title')

        if filename:
            with h5py.File(unicode(filename), 'w') as f:
                self._save_stats(f)
                self._save_math(f)
                self._save_select_channel(f)

    def _save_stats(self, f):
        stats_grp = f.create_group('stats')
        average_dset = f.create_dataset('stats/average', (self.n_channels,), dtype='f')
        average_dset[...] = self.stats_widget.average

        peak_peak_dset = f.create_dataset('stats/peak_peak', (self.n_channels,), dtype='f')
        peak_peak_dset[...] = self.stats_widget.amplitude

        amplitude_rms_dset = f.create_dataset('stats/amplitude_rms', (self.n_channels,), dtype='f')
        amplitude_rms_dset[...] = self.stats_widget.amplitude_rms

    def _save_math(self, f):
        math_grp = f.create_group('math')
        avg_on_button_dset = f.create_dataset('math/avg_on_button', (0,), dtype='f')
        avg_on_button_dset.attrs['StyleSheet'] = unicode(self.math_widget.avg_on_button.styleSheet())
        avg_on_button_dset.attrs['Text'] = unicode(self.math_widget.avg_on_button.text())

        avg_spin_dset = f.create_dataset('math/avg_spin', (0,), dtype='f')
        avg_spin_dset.attrs['Minimum'] = self.math_widget.avg_spin.minimum()
        avg_spin_dset.attrs['Maximum'] = self.math_widget.avg_spin.maximum()
        avg_spin_dset.attrs['Value'] = self.math_widget.avg_spin.value() # Always at 1 ??!!
        
        fourier_dset = f.create_dataset('math/fourier', (0,), dtype='f')
        fourier_dset.attrs['Status'] = self.math_widget.fourier

    def _save_select_channel(self, f):
        select_channel_grp = f.create_group('select_channel')
        adc_checkbox_dset = f.create_dataset('select_channel/adc_checkbox', (self.n_channels,), dtype=bool)
        dac_checkbox_dset = f.create_dataset('select_channel/dac_checkbox', (self.n_channels,), dtype=bool)

        for i in range(self.n_channels):
            adc_checkbox_dset[i] = self.select_channel_widget.adc_checkbox[i].isChecked()
            dac_checkbox_dset[i] = self.select_channel_widget.dac_checkbox[i].isChecked()
