#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import numpy as np

from .base import Base
from koheron import command

# Lorentzian fit
from scipy.optimize import leastsq
import matplotlib.pyplot as plt

def lorentzian(f, p):
    return p[0]/(1+f**2/p[1])

def residuals(p, y, f):
    return y - lorentzian(f, p)


class Spectrum(Base):
    """ Driver for the spectrum bitstream """

    def __init__(self, client, verbose=False):
        self.wfm_size = 4096
        super(Spectrum, self).__init__(self.wfm_size, client)
        
        self.fifo_start_acquisition(1000)

        self.avg_on = True

        self.spectrum = np.zeros(self.wfm_size, dtype=np.float32)
        self.demod = np.zeros((2, self.wfm_size))

        self.demod[0, :] = 0.49 * (1 - np.cos(2 * np.pi * np.arange(self.wfm_size) / self.wfm_size))
        self.demod[1, :] = 0

        self.noise_floor = np.zeros(self.wfm_size)

        # self.set_offset(0, 0)
 
        self.set_address_range(0, 0)

        self.set_demod()
        self.set_scale_sch(0)
        self.set_n_avg_min(0)

        self.reset()

        # Laser linewidth estimation
        self.fit_linewidth = False
        self.fit = np.zeros((2,100))
        self.i = 0

    @command()
    def set_n_avg_min(self, n_avg_min): 
        """ Set the minimum of averages that will be computed on the FPGA
        The effective number of averages is >= n_avg_min.
        """
        pass

    @command(funcname='reset')
    def reset_dac(self):
        pass

    def set_dac(self, channels=[0,1]):
        @command(classname='Spectrum')
        def set_dac_buffer(self, channel, data):
            pass
        for channel in channels:
            data = np.uint32(np.mod(np.floor(8192 * self.dac[channel,:]) + 8192, 16384) + 8192)
            set_dac_buffer(self, channel, data[::2] + data[1::2] * 65536)

    def reset(self):
        super(Spectrum, self).reset()
        self.reset_dac()
        self.avg_on = True
        self.set_averaging(self.avg_on)

    @command()
    def set_scale_sch(self, scale_sch):
        pass

    @command()
    def set_offset(self, offset_real, offset_imag):
        pass

    @command()
    def set_demod_buffer(self, data):
        pass

    @command()
    def set_noise_floor_buffer(self, data):
        pass

    def set_demod(self, warning=False):
        if warning:
            if np.max(np.abs(self.demod)) >= 1:
                print('WARNING : demod out of bounds')
        self.set_demod_buffer(self.twoint14_to_uint32(self.demod))

    def calibrate(self, noise_floor):
        self.noise_floor = noise_floor
        self.set_noise_floor_buffer(self.noise_floor)

    @command()
    def get_spectrum(self):
        self.spectrum = self.client.recv_array(self.wfm_size, dtype='float32')

        if self.fit_linewidth:
            idx = np.arange(1000,4000)
            f = self.sampling.f_fft[idx]
            y = self.spectrum[idx]
            params_init = [2e17, 3e6**2]
            best_params = leastsq(residuals, params_init, args=(y,f), full_output=1)
            self.fit[:, self.i % 100] = best_params[0]
            self.i += 1
            print("Linewidth = {0:2f} kHz".format(1e-3 * np.sqrt(np.mean(self.fit[1,:]))))

            if self.cnt == 50:
                spectrum_fit = lorentzian(self.sampling.f_fft, best_params[0])
                freq = 1e-6 * np.fft.fftshift(self.sampling.f_fft)
                psd = np.fft.fftshift(self.spectrum)
                psd_fit = np.fft.fftshift(spectrum_fit)
                plt.semilogy(freq, psd, freq, psd_fit)
                plt.show()

    @command()
    def get_num_average(self):
        return self.client.recv_uint32()

    @command()
    def get_peak_address(self):
        return self.client.recv_uint32()

    @command()
    def get_peak_maximum(self):
        return self.client.recv_int(4, fmt='f')

    @command()
    def set_address_range(self, address_low, address_high):
        pass

    @command()
    def set_averaging(self, avg_status): pass

    # === Peak data stream

    def get_peak_values(self):
        @command(classname='Spectrum')
        def store_peak_fifo_data(self):
            return self.client.recv_uint32()

        self.peak_stream_length = store_peak_fifo_data(self)

        @command(classname='Spectrum')
        def get_peak_fifo_data(self):
            return self.client.recv_vector(dtype='uint32')

        return get_peak_fifo_data(self)

    @command()
    def get_peak_fifo_length(self):
        return self.client.recv_uint32()

    @command()
    def fifo_start_acquisition(self, acq_period): pass

    @command()
    def fifo_stop_acquisition(self): pass
