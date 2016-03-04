#!/usr/bin/env python
# -*- coding: utf-8 -*-

import initExample
import os
import time
import numpy as np
import matplotlib.pyplot as plt

from lase.core import KClient, ZynqSSH
from lase.drivers import Oscillo

# Load the oscillo instrument
host = os.getenv('HOST','192.168.1.100')
password = os.getenv('PASSWORD','changeme')
ssh = ZynqSSH(host, password)
ssh.install_instrument('oscillo')

# Connect to the instrument
client = KClient(host)
driver = Oscillo(client)

# Enable laser
driver.start_laser()

# Set laser current
current = 30  # mA
driver.set_laser_current(current)

# Modulation on DAC
amp_mod = 0.2
freq_mod = 1e6
driver.dac[1, :] = amp_mod*np.sin(2 * np.pi * freq_mod * driver.sampling.t)
driver.set_dac()

# Signal on ADC
driver.get_adc()
signal = driver.adc[0, :]

# Plot
plt.plot(driver.sampling.t, signal)
plt.show()

# Plot
psd_signal = np.abs(np.fft.fft(signal)) ** 2

plt.semilogy(1e-6 * np.fft.fftshift(driver.sampling.f_fft), np.fft.fftshift(psd_signal))
plt.xlabel('Frequency (MHz)')
plt.show()

# Disable laser
driver.stop_laser()
driver.close()
