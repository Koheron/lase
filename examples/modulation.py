#!/usr/bin/env python
# -*- coding: utf-8 -*-

import initExample

from lase.core import KClient

# Driver to use 
from lase.drivers import Oscillo

# Modules to import
import numpy as np
import matplotlib.pyplot as plt
import time


# Connect to Lase
host = '192.168.1.4' # Lase IP address 
client = KClient(host)
driver = Oscillo(client) # Replace with appropriate driver

# Enable laser
driver.start_laser()

# Set laser current
current = 15 #mA
driver.set_laser_current(current)

# Modulation on DAC
amp_mod = 0.2
freq_mod = 1e6
driver.dac[1,:] = amp_mod*np.sin(2*np.pi*freq_mod*driver.sampling.t)
driver.set_dac()

# Signal on ADC
driver.get_adc()
signal = driver.adc[0,:]

# Plot 
plt.plot(driver.sampling.t, signal)
plt.show()

# Plot 
psd_signal = np.abs(np.fft.fft(signal))**2

plt.semilogy(1e-6 * np.fft.fftshift(driver.sampling.f_fft), np.fft.fftshift(psd_signal))
plt.xlabel('Frequency (MHz)')
plt.show()

# Disable laser
driver.stop_laser()
driver.close()
