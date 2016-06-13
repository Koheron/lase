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
        print tabulate([['Average', self.stats['average'][0], self.stats['average'][1]],
                       ['Peak-peak', self.stats['peak_peak'][0], self.stats['peak_peak'][1]],
                       ['Average', self.stats['rms'][0], self.stats['rms'][1]]], 
                       headers=['', 'Chan 1', 'Chan 2'])

    def __del__(self):
        self.file.close()

if __name__ == "__main__":
    reader = LDKdataReader('../test.h5')
    reader.print_stats()