import initExample

import h5py
import numpy as np

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
        print('\n=== Stats ===')
        print tabulate([['Average', self.stats['average'][0], self.stats['average'][1]],
                       ['Peak-peak', self.stats['peak_peak'][0], self.stats['peak_peak'][1]],
                       ['Average', self.stats['rms'][0], self.stats['rms'][1]]], 
                       headers=['', 'Chan 1', 'Chan 2'])

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

        print('\n=== Math widget ===')
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

        print('\n=== Select channel widget ===')
        print('ADC')
        print('  1            ' + unicode(self.select_channel['adc_checkbox'][0]))
        print('  2            ' + unicode(self.select_channel['adc_checkbox'][1]))
        print('DAC')
        print('  1            ' + unicode(self.select_channel['dac_checkbox'][0]))
        print('  2            ' + unicode(self.select_channel['dac_checkbox'][1]))


    def __del__(self):
        self.file.close()

if __name__ == "__main__":
    reader = LDKdataReader('../test.h5')
    reader.print_stats()
    reader.print_math()
    reader.print_select_channel()