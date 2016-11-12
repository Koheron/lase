#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import numpy as np

from .sampling import Sampling
from koheron import command

# Lorentzian fit
from scipy.optimize import leastsq
import matplotlib.pyplot as plt

def lorentzian(f, p):
    return p[0]/(1+f**2/p[1])

def residuals(p, y, f):
    return y - lorentzian(f, p)


class Spectrum(object):
    """ Driver for the spectrum bitstream """

    def __init__(self, client, verbose=False):
        self.client = client
        self.wfm_size = 4096
        self.max_current = 40  # mA
        self.sampling = Sampling(self.wfm_size, 125e6)

        self.fifo_start_acquisition(1000)

        self.avg_on = True

        self.spectrum = np.zeros(self.wfm_size, dtype=np.float32)
        self.demod = np.zeros((2, self.wfm_size))

        self.demod[0, :] = 0.49 * (1 - np.cos(2 * np.pi * np.arange(self.wfm_size) / self.wfm_size))
        self.demod[1, :] = 0

        self.noise_floor = np.zeros(self.wfm_size, dtype=np.float32)

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

        self.opened = True
        self.dac = np.zeros((2, self.sampling.n))

    def close(self):
        self.stop_laser()
        self.reset()


    def reset_laser(self):
        @command('Laser')
        def reset(self): pass

        reset(self)

    @command(classname='Laser')
    def start_laser(self): pass

    @command(classname='Laser')
    def stop_laser(self): pass

    @command(classname='Laser')
    def get_laser_current(self):
        return (0.0001/21.) * self.client.recv_uint32()

    @command(classname='Laser')
    def get_laser_power(self):
        return self.client.recv_uint32()

    @command(classname='Laser')
    def get_monitoring(self):
        return self.client.recv_tuple()

    @command(classname='Laser')
    def set_laser_current(self, current):
        """ current: The bias in mA """
        pass

    @command(classname='Common')
    def get_bitstream_id(self): pass

    @command(classname='Common')
    def set_led(self, value): pass

    @command(classname='Common')
    def init(self): pass

    def twoint14_to_uint32(self, data):
        data1 = np.mod(np.floor(8192 * data[0, :]) + 8192,16384) + 8192
        data2 = np.mod(np.floor(8192 * data[1, :]) + 8192,16384) + 8192
        return np.uint32(data1 + 65536 * data2)

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
        self.reset_laser()
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

    def calibrate(self):
        tmp = np.zeros(self.sampling.n, dtype=np.float32)
        for i in range(100):
            self.get_spectrum()
            tmp += self.spectrum
        self.noise_floor = tmp / 100
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
