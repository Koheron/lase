import initExample

import h5py
import numpy as np
import matplotlib.pyplot as plt

from tabulate import tabulate

class LDKdataReader:
    def __init__(self, h5_filename):
        self.file = h5py.File(h5_filename)

    def get_stats(self):
        self.stats = {
          'average': self.file['stats/average'][()],
          'peak_peak': self.file['stats/peak_peak'][()],
          'rms': self.file['stats/amplitude_rms'][()]
        }

        return self.stats

    def print_stats(self):
        self.get_stats()
        print('\n--------------------------------------------------------------------------------')
        print('  Stats')
        print('--------------------------------------------------------------------------------')
        print tabulate([['Average', self.stats['average'][0], self.stats['average'][1]],
                       ['Peak-peak', self.stats['peak_peak'][0], self.stats['peak_peak'][1]],
                       ['Average', self.stats['rms'][0], self.stats['rms'][1]]], 
                       headers=['', 'Chan 1', 'Chan 2'], tablefmt="plain")

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

    def get_select_channel(self):
        self.select_channel = {
          'adc_checkbox': self.file['select_channel/adc_checkbox'][()],
          'dac_checkbox': self.file['select_channel/dac_checkbox'][()]
        }

        return self.select_channel

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

    def print_monitor(self):
        self.get_monitor()

        print('\n--------------------------------------------------------------------------------')
        print('  Monitor')
        print('--------------------------------------------------------------------------------')
        print('FrameRate      ' + unicode(self.monitor['FrameRate']))
        print('LaserCurrent   ' + unicode(self.monitor['LaserCurrent']))
        print('LaserPower     ' + unicode(self.monitor['LaserPower']))

    def get_laser(self):
        self.laser = {
            'LaserCurrent': self.file['laser/data'].attrs['LaserCurrent'],
            'LaserON': self.file['laser/data'].attrs['LaserON']
        }

        return self.laser

    def print_laser(self):
        self.get_laser()

        print('\n--------------------------------------------------------------------------------')
        print('  Laser')
        print('--------------------------------------------------------------------------------')
        print('LaserCurrent   ' + unicode(self.laser['LaserCurrent']))
        print('LaserON        ' + unicode(self.laser['LaserON']))

    def print_all(self):
        self.print_stats()
        self.print_math()
        self.print_select_channel()
        self.print_monitor()
        self.print_laser()
        print('\n')

    def __del__(self):
        self.file.close()

if __name__ == "__main__":
    reader = LDKdataReader('../test.h5')
    reader.print_all()
    reader.plot_data()