#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

class LaseModel(object):
    def __init__(self, sampling):
         
        self.sampling = sampling
        
        # Laser parameters
        self._laser_threshold = .005 # A
        self._laser_efficiency = 0.12 # W / A                
        self._modulation_resistance = 100 # Ohm
        self._wavelength = 1550e-9 # m
        self._linewidth = 4e6 # Hz
        
        # Amplitude Modulation Transfer Function
        self._amplitude_mtf = np.ones(self.sampling.n, dtype=np.dtype('complex64'))
        # Frequency Modulation Transfer Function
        self._frequency_mtf = np.ones(self.sampling.n, dtype=np.dtype('complex64'))  
        
        # Photodiodetection parameters
        self._photodiode_efficiency = 0.95 # A/W
        self._transimpedance_resistance = 1e4 # Ohm
        self._optical_attenuation = 0.01 # Attenuation between the laser and the photodiode
        
        # ADC parameters
        self._adc_conversion_factor = 8192 / 1 # 1/V
        self._adc_noise = 10 # Standard deviation of ADC noise
        
        # Mach-Zehnder interferometer parameters   
        self.zehnder = True
        self.tau = 5e-9 # s
        self.contrast = 0.7
        self.alpha = -1e14
        self.beta = 0
        
    def laser_current(self, laser_enable, constant_current, dac):
        laser_current = float(laser_enable) * (constant_current + 
            np.real(np.fft.ifft(np.fft.fft(dac) *
            (self._amplitude_mtf / np.max(np.abs(self._amplitude_mtf))))) /
            self._modulation_resistance)
        laser_current = np.maximum(np.zeros(len(laser_current)), laser_current - self._laser_threshold)        
        return laser_current

    def mach_zehnder_power(self, laser_frequency, laser_power):
        self.beta += 0.025
        phi = 2 * np.pi * np.cumsum(laser_frequency) * self.sampling.dt
        phi_tau = self.sampling.shift_subpix(phi, self.tau, correct_slope=True)
        output_power = laser_power * (1+ self.contrast*np.real(np.exp(1j*self.beta)*np.exp(1j*(phi - phi_tau)))) 
        return output_power        
        
    def laser_power(self, laser_current):
        laser_power = self._laser_efficiency * laser_current
        return laser_power
        
    def laser_frequency(self, laser_current):
        # TODO
        laser_frequency = self.alpha * (laser_current)**3       
        return laser_frequency

    def photodetection_voltage(self, optical_power):
        # Optical power in mW
        voltage = self._transimpedance_resistance * self._photodiode_efficiency * optical_power
        return voltage

    def adc_from_voltage(self, voltage, n_avg=1):
        tmp = self._adc_conversion_factor * voltage
        tmp += np.sqrt(1./n_avg) * self._adc_noise * np.random.randn(self.sampling.n)
        tmp = np.floor(tmp)
        tmp = np.where(tmp < +8191, tmp, +8191)
        tmp = np.where(tmp > -8192, tmp, -8192)
        return tmp
        
        
