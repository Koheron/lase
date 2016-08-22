#!/usr/bin/env python
# -*- coding: utf-8 -*-

import initExample
import os
import time
import numpy as np
import matplotlib.pyplot as plt

from koheron import load_instrument
from ldk.drivers import Oscillo

host = os.getenv('HOST','192.168.1.100')
cmd = os.getenv('CMD','get_adc')

def speed_test(host, n_pts=100):
    time_array = np.zeros(n_pts)
    client = load_instrument(host, instrument='oscillo')
    driver = Oscillo(client)
    driver.set_averaging(False)

    t0 = time.time()
    t_prev = t0

    for i in range(n_pts):
        if cmd == 'get_adc':
        	driver.get_adc()
        	time.sleep(0.00001) # used to fix garbage collection pb
        elif cmd == 'get_num_average':
            driver.get_num_average(0)
        t = time.time()
        time_array[i] = t - t_prev
        print host, i, time_array[i]
        t_prev = t
    
    print '{} us'.format(1E6 * np.median(time_array))
    assert(np.median(time_array) < 0.0025)
    return time_array

plt.plot(1E6 * speed_test(host))
plt.xlabel('Trial #')
plt.ylabel('Time (us)')
plt.show()
