#!/usr/bin/env python
# -*- coding: utf-8 -*-

import initExample
import os
import time
import numpy as np
import matplotlib
matplotlib.use('GTKAgg')
from matplotlib import pyplot as plt

from koheron import connect
from ldk.drivers import Spectrum

# Load the spectrum instrument
host = os.getenv('HOST','192.168.1.100')
client = connect(host, name='spectrum')
driver = Spectrum(client)

# Enable laser
driver.start_laser()

# Set laser current
current = 30  # mA
driver.set_laser_current(current)

# Plot parameters
fig = plt.figure()
ax = fig.add_subplot(111)
x = 1e-6 * np.fft.fftshift(driver.sampling.f_fft)
y = 10*np.log10(np.fft.fftshift(driver.spectrum))
li, = ax.plot(x, y)
fig.canvas.draw()
ax.set_xlim((x[0],x[-1]))
ax.set_ylim((100,250))
ax.set_xlabel('Frequency (MHz)')
ax.set_ylabel('Power spectral density (dB)')

while True:
    try:
        driver.get_spectrum()
        li.set_ydata(10*np.log10(np.fft.fftshift(driver.spectrum)))
        fig.canvas.draw()
        plt.pause(0.001)
    except KeyboardInterrupt:
        # Save last spectrum in a csv file
        np.savetxt("psd.csv", driver.spectrum, delimiter=",")
        driver.stop_laser()
        driver.close()
        break
