#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import numpy as np
from lase_simu import LaseSimu


class OscilloSimu(LaseSimu):
    
    def __init__(self):
        n = 8192
        super(OscilloSimu, self).__init__(n)

        self.avg_on = False

        self.adc = np.zeros((2,self.sampling.n))
        self.spectrum = np.zeros((2,self.sampling.n/2))        
        self.avg_spectrum = np.zeros((2,self.sampling.n/2))
        self.ideal_amplitude_waveform = np.zeros(self.sampling.n)
        sigma_freq = 5e6 # Hz
        self.gaussian_filter = 1.0 * np.exp(-1.0*self.sampling.f_fft**2/(2*sigma_freq**2))

        self.amplitude_transfer_function = np.ones(self.sampling.n, dtype=np.dtype('complex128'))
        
        # Calibration
        self.adc_offset = np.zeros(2)
        self.optical_power = np.ones(2)
        self.power = np.ones(2)
        
        self.reset()
        
    def update(self):
        super(OscilloSimu, self).update()
            
    def reset(self):
        super(OscilloSimu, self).reset()
        self.avg_on = False
        self.set_averaging(self.avg_on)
        
    def set_averaging(self, avg_on):
        self.avg_on = avg_on    
        
    def get_adc(self):
        n_avg = 1
        if self.avg_on:
            n_avg = 100   
        self.update()
        self.adc[0,:] = self.model.adc_from_voltage(
            self.model.photodetection_voltage(
            self.model._optical_attenuation * self._live_laser_power),
            n_avg=n_avg)
        self.adc[1,:] = self.model.adc_from_voltage(
            self.model.photodetection_voltage(
            self.model._optical_attenuation * self._live_mach_zehnder_power),
            n_avg=n_avg)
        
        
        self.adc[0,:] -= self.adc_offset[0]
        self.adc[1,:] -= self.adc_offset[1]
        self.adc[0,:] *= self.optical_power[0] /self.power[0]
        self.adc[1,:] *= self.optical_power[1] /self.power[1]

    def get_amplitude_transfer_function(self, channel_dac = 0, channel_adc =0, \
                                        transfer_avg=100):
        n_freqs = self.sampling.n/2 +1
        self.amplitude_transfer_function *= 0
        for i in range(transfer_avg):
            self.amplitudes = np.ones(n_freqs)
            random_phases = 2 * np.pi * np.random.rand(n_freqs)
            white_noise = np.fft.irfft(self.amplitudes * \
                          np.exp(1j * random_phases))
            white_noise = np.fft.fft(white_noise)
            white_noise[0] = 0.01
            white_noise[self.sampling.n/2]=1    
            white_noise = np.real( np.fft.ifft(white_noise))
            white_noise /= 1.7 * np.max(np.abs(white_noise))
            self.dac[channel_dac,:] = white_noise
            self.set_dac()
            time.sleep(0.01)
            self.get_adc()
            self.amplitude_transfer_function += \
                np.fft.fft(self.adc[channel_adc,:])/np.fft.fft(white_noise)
        self.amplitude_transfer_function = self.amplitude_transfer_function/transfer_avg
        self.amplitude_transfer_function[0] = 1
        self.dac[channel_dac,:] = np.zeros(self.sampling.n)
        self.set_dac()

    def get_correction(self):
        tmp = np.fft.fft(self.amplitude_error)/self.amplitude_transfer_function
        tmp[0] = 0
        tmp = self.gaussian_filter * tmp
        return np.real(np.fft.ifft(tmp))

    def optimize_amplitude(self, alpha=1, channel=0):        
        self.amplitude_error = (self.adc[0,:] - np.mean(self.adc[0,:])) - self.ideal_amplitude_waveform
        self.dac[channel,:] -= alpha*self.get_correction()
        
    def get_spectrum(self):
        fft_adc = np.fft.fft(self.adc, axis=1)
        self.spectrum = fft_adc[:,0:self.sampling.n/2]
        
    def get_avg_spectrum(self, n_avg=1):
        self.avg_spectrum = np.zeros((2,self.sampling.n/2))        
        for i in range(n_avg):
            self.get_adc()
            fft_adc = np.abs(np.fft.fft(self.adc, axis=1))
            self.avg_spectrum += fft_adc[:,0:self.sampling.n/2]            
        self.avg_spectrum = self.avg_spectrum / n_avg
        
    def set_amplitude_transfer_function(self, amplitude_transfer_function):
        self.amplitude_transfer_function = amplitude_transfer_function
        self.model._amplitude_mtf = amplitude_transfer_function

