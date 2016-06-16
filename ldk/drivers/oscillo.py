#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import math
import numpy as np

from .base import Base
from koheron_tcp_client import command, write_buffer

class Oscillo(Base):
    """ Driver for the oscillo bitstream
    """

    def __init__(self, client, verbose=False):
        self.wfm_size = 8192
        super(Oscillo, self).__init__(self.wfm_size, client)

        if self.open_oscillo() < 0:
            print('Cannot open device OSCILLO')
    
        self.avg_on = False

        self.adc = np.zeros((2, self.wfm_size))
        self.spectrum = np.zeros((2, self.wfm_size / 2))
        self.avg_spectrum = np.zeros((2, self.wfm_size / 2))
        self.set_n_avg_min(0)
        self.reset()

    def open_oscillo(self):
        @command('OSCILLO')
        def open(self):
            return self.client.recv_int32()
        return open(self)

    @command('OSCILLO')
    def open(self):
        return self.client.recv_int32()

    @command('OSCILLO','I')
    def set_n_avg_min(self, n_avg_min): pass

    @command('OSCILLO','I')
    def set_period(self, period): pass

    @command('OSCILLO')
    def reset_acquisition(self): pass

    @write_buffer('OSCILLO')
    def set_dac_buffer(self, data): pass

    def reset_dac(self):
        @command('OSCILLO')
        def reset(self): pass
        reset(self)

    def set_dac(self, warning=False, reset=False):
        if warning:
            if np.max(np.abs(self.dac)) >= 1:
                print('WARNING : dac out of bounds')
        self.set_dac_buffer(self.twoint14_to_uint32(self.dac))

        if reset:
            self.reset_acquisition()

    def reset(self):
        super(Oscillo, self).reset()
        self.reset_dac()
        self.avg_on = False
        self.set_averaging(self.avg_on)

    @command('OSCILLO', '?')
    def set_averaging(self, avg_status):
        pass

    @command('OSCILLO')
    def get_num_average(self):
        n_avg = self.client.recv_uint32()
        return n_avg

    @command('OSCILLO')
    def read_all_channels(self):
        return self.client.recv_buffer(2 * self.wfm_size, data_type='float32')

    def get_adc(self):
        data = self.read_all_channels()
        self.adc = np.reshape(data, (2, self.wfm_size))

    def get_spectrum(self):
        fft_adc = np.fft.fft(self.adc, axis=1)
        self.spectrum = fft_adc[:, 0:self.wfm_size / 2]

    def get_avg_spectrum(self, n_avg=1):
        self.avg_spectrum = np.zeros((2, self.wfm_size / 2))
        for i in range(n_avg):
            self.get_adc()
            fft_adc = np.abs(np.fft.fft(self.adc, axis=1))
            self.avg_spectrum += fft_adc[:, 0:self.wfm_size / 2]
        self.avg_spectrum /= n_avg
