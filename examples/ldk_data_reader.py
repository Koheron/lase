import initExample

try:
    import h5py
    HAS_HDF5 = True
except ImportError:
    HAS_HDF5 = False

import uuid
import os
import json
import zipfile
import shutil
import numpy as np
import matplotlib.pyplot as plt

from tabulate import tabulate

class LDKdataReader:
    def __init__(self, filename):

        extension = os.path.splitext(filename)[1]

        if (extension == '.h5' or extension == '.hdf5') and HAS_HDF5:
            self.file_type = 'H5'
            self.file = h5py.File(h5_filename)
        elif extension == '.zip' and HAS_HDF5:
            self.file_type = 'ZIP'
            zipf = zipfile.ZipFile(filename, 'r', zipfile.ZIP_DEFLATED)
            tmp_dir = os.path.join(os.path.dirname(filename), unicode(uuid.uuid4()))
            os.makedirs(tmp_dir)
            zipf.extractall(tmp_dir)
            with open(os.path.join(tmp_dir, 'data.json')) as f:
                self.json = json.load(f)
            shutil.rmtree(tmp_dir)
        else:
            raise TypeError('Unknown file extension')

    def get_metadata(self):
        if self.file_type == 'H5':
            self.metadata = {
                'Date': self.file['h5_file_metadata/data'].attrs['Date'],
                'Time': self.file['h5_file_metadata/data'].attrs['Time']
            }
        elif self.file_type == 'ZIP':
            self.metadata = self.json['metadata']

    def get_stats(self):
        self.stats = {
          'average': self.file['stats/average'][()],
          'peak_peak': self.file['stats/peak_peak'][()],
          'rms': self.file['stats/amplitude_rms'][()]
        }

        return self.stats

    def get_math(self):
        self.math = {
          'AvgOnButton': {
            'StyleSheet': self.file['math/avg_on_button'].attrs['StyleSheet'],
            'Text': self.file['math/avg_on_button'].attrs['Text']
          },
          'AvgSpin': {
            'Minimum': self.file['math/avg_spin'].attrs['Minimum'],
            'Maximum': self.file['math/avg_spin'].attrs['Maximum'],
            'Value': self.file['math/avg_spin'].attrs['Value']
          },
          'Fourier': {
            'Status': self.file['math/fourier'].attrs['Status']
          }
        }

        return self.math

    def get_select_channel(self):
        self.select_channel = {
          'adc_checkbox': self.file['select_channel/adc_checkbox'][()],
          'dac_checkbox': self.file['select_channel/dac_checkbox'][()]
        }

        return self.select_channel

    def get_plot_data(self):
        self.data_x = self.file['plot/data_x'][()]
        self.data_y = self.file['plot/data_y'][()]

    def plot_data(self):
        self.get_plot_data()
        plt.plot(np.transpose(self.data_x), np.transpose(self.data_y))
        plt.show()

    def get_monitor(self):
        self.monitor = {
          'FrameRate': self.file['monitor/data'].attrs['FrameRate'],
          'LaserCurrent': self.file['monitor/data'].attrs['LaserCurrent'],
          'LaserPower': self.file['monitor/data'].attrs['LaserPower'],
        }

        return self.monitor

    def get_laser(self):
        self.laser = {
            'LaserCurrent': self.file['laser/data'].attrs['LaserCurrent'],
            'LaserON': self.file['laser/data'].attrs['LaserON']
        }

        return self.laser

    # -----------------------------------------------------------------------------------------------------------------
    #   Print
    # -----------------------------------------------------------------------------------------------------------------

    def print_metadata(self):
        self.get_metadata()

        print('\n--------------------------------------------------------------------------------')
        print('  Metadata')
        print('--------------------------------------------------------------------------------')
        print('Date       ' + self.metadata['Date'])
        print('Time       ' + self.metadata['Time'])

    def print_stats(self):
        self.get_stats()
        print('\n--------------------------------------------------------------------------------')
        print('  Stats')
        print('--------------------------------------------------------------------------------')
        print tabulate([['Average', self.stats['average'][0], self.stats['average'][1]],
                       ['Peak-peak', self.stats['peak_peak'][0], self.stats['peak_peak'][1]],
                       ['Average', self.stats['rms'][0], self.stats['rms'][1]]], 
                       headers=['', 'Chan 1', 'Chan 2'], tablefmt="plain")

    def print_math(self):
        self.get_math()

        print('\n--------------------------------------------------------------------------------')
        print('  Math')
        print('--------------------------------------------------------------------------------')
        print('avg_on_button')
        print('  StyleSheet   ' + self.math['AvgOnButton']['StyleSheet'])
        print('  Text         ' + self.math['AvgOnButton']['Text'])
        print('avg_spin')
        print('  Minimum      ' + unicode(self.math['AvgSpin']['Minimum']))
        print('  Maximum      ' + unicode(self.math['AvgSpin']['Maximum']))
        print('  Value        ' + unicode(self.math['AvgSpin']['Value']))
        print('fourier')
        print('  Status       ' + unicode(self.math['Fourier']['Status']))

    def print_select_channel(self):
        self.get_select_channel()

        print('\n--------------------------------------------------------------------------------')
        print('  Select channel')
        print('--------------------------------------------------------------------------------')
        print('ADC')
        print('  1            ' + unicode(self.select_channel['adc_checkbox'][0]))
        print('  2            ' + unicode(self.select_channel['adc_checkbox'][1]))
        print('DAC')
        print('  1            ' + unicode(self.select_channel['dac_checkbox'][0]))
        print('  2            ' + unicode(self.select_channel['dac_checkbox'][1]))

    def print_monitor(self):
        self.get_monitor()

        print('\n--------------------------------------------------------------------------------')
        print('  Monitor')
        print('--------------------------------------------------------------------------------')
        print('FrameRate      ' + unicode(self.monitor['FrameRate']))
        print('LaserCurrent   ' + unicode(self.monitor['LaserCurrent']))
        print('LaserPower     ' + unicode(self.monitor['LaserPower']))

    def print_laser(self):
        self.get_laser()

        print('\n--------------------------------------------------------------------------------')
        print('  Laser')
        print('--------------------------------------------------------------------------------')
        print('LaserCurrent   ' + unicode(self.laser['LaserCurrent']))
        print('LaserON        ' + unicode(self.laser['LaserON']))

    def print_all(self):
        self.print_metadata()
        # self.print_stats()
        # self.print_math()
        # self.print_select_channel()
        # self.print_monitor()
        # self.print_laser()
        print('\n')

    def __del__(self):
        if self.file_type == 'H5':
            self.file.close()

if __name__ == "__main__":
    # reader = LDKdataReader('../test.h5')
    # reader.print_all()
    # reader.plot_data()

    reader = LDKdataReader('../test.zip')
    reader.print_all()