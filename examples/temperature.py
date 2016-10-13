#!/usr/bin/env python
# -*- coding: utf-8 -*-

import initExample
import os
import time
import numpy as np
import matplotlib.pyplot as plt
import csv
import time
from scipy import signal

from koheron import connect
from ldk.drivers import Oscillo

host = os.getenv('HOST','192.168.1.100')
client = connect(host, name='oscillo')
driver = Oscillo(client)

current = 30 #mA

freq = 1
mod_amp = 0.2
# Modulate with a triangle waveform of period 8192 x 8 ns
driver.dac[1,:] = mod_amp * signal.sawtooth(2 * np.pi * freq / driver.n * np.arange(driver.n), width=0.5)
driver.set_dac()

driver.start_laser()
driver.set_averaging(True)
driver.set_laser_current(current)
time.sleep(0.1)

plt.ylim([-2*np.pi, 2*np.pi])
plt.ion()
plt.show()

phase_previous_pos = 0
phase_previous_neg = 0

temperature = 20 # degrees Celsius
data = np.zeros((1000,2)) + temperature
# Hanning FFT Window
window = 0.5 * (1-np.cos(2 * np.pi * np.arange(4095) / 4095))

with open('temperature.csv','w') as f:
	for i in range(50000000):
		driver.get_adc()
		
		# Separate positive and negative slopes in the triangle waveform
		adc_pos = driver.adc[0,0:4095]
		adc_neg = driver.adc[0,4096:8191]

		fft_pos = np.fft.fft(adc_pos * window)
		fft_neg = np.fft.fft(adc_neg * window)

		phase_adc_pos = np.angle(fft_pos)
		phase_adc_neg = np.angle(fft_neg)
		
		# The phase of the frequency modulation 
		phase_pos = phase_adc_pos[6]
		phase_neg = phase_adc_pos[6]
		
		plt.clf()

		diff_pos = -(phase_pos - phase_previous_neg + np.pi)%(2*np.pi)-np.pi
		diff_neg = +(phase_neg - phase_previous_neg + np.pi)%(2*np.pi)-np.pi
	  
		diff = diff_pos + diff_neg/2

		data = np.roll(data, -1, axis=0)
		temperature = temperature + 0.015 * diff / (2*np.pi)
		data[-1] = temperature
		string = str(time.time())+','+str(temperature)+'\n'
		f.write(string)
		print(string)
		phase_previous_pos = phase_pos
		phase_previous_neg = phase_neg

f.close()

driver.stop_laser()
driver.close()
plt.show()
