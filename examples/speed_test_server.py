#!/usr/bin/env python
# -*- coding: utf-8 -*-

import initExample
from lase.core import KClient
from lase.drivers import Oscillo

import numpy as np
import matplotlib.pyplot as plt
import time

def read(host, n_pts=1000, decim_factor = 1):
    data = np.zeros(2*8192/decim_factor)
    client = KClient(host)
    driver = Oscillo(client)
    time_total = np.zeros((n_pts,9))    
    for j in range(9):
        t0 = time.time()
        t_prev = t0
        print j
        for i in range(n_pts):
            if j==0:
                data = driver.read_zeros()
            elif j==1:
                data = driver.read_rambuf()
            elif j==2:
                data = driver.read_rambuf_memcpy()
            elif j==3:
                data = driver.read_rambuf_mycopy()
            elif j==4:
                data = driver.read_all_channels()
            elif j==5:
                data = driver.read_raw_all()
            elif j==6:
                data = driver.read_mmapbuf_nocopy()
            elif j==7:
                data = driver.read_all_channels_decim(decim_factor)
            elif j==8:
                data = driver.read_rambuf_mmap_memcpy()

            print i
            t = time.time()
            time_total[i,j] = t - t_prev
            t_prev = t
    driver.close()
    client.__del__()
    print np.mean(time_total[256:768])
    return time_total

host = '192.168.1.2'

legends = ('read_zeros',
           'read_rambuf',
           'read_rambuf_memcpy',
           'read_rambuf_mycopy',
           'read_all_channels',
           'read_raw_all',
           'read_mmapbuf_nocopy',
           'read_all_channels_decim',
           'read_rambuf_mmap_memcpy')

lineObjects = plt.plot(read(host,n_pts=1000,decim_factor = 1))
plt.legend(iter(lineObjects), legends)

plt.show()


#sizes = 1024 * np.arange(8+1)
#a = np.zeros((len(sizes),2))

#for i, size in enumerate(sizes):
#    a[i,:] = speed_test(host, size=size)
#    print size, a[i,:]

#plt.plot(sizes, a[:,0])
#plt.plot(sizes, a[:,1])

def speed_test(host, n_pts=1, size=8192):
    time_total = np.zeros(n_pts)
    time_server = np.zeros(n_pts)
    client = KClient(host)
    driver = Oscillo(client)
    t0 = time.time()
    t_prev = t0    

    for i in range(n_pts):
        for j in range(1):
            time_server[i] = driver.speed_test(1,1000,size=size)
        t = time.time()
        time_total[i] = t - t_prev
        t_prev = t

    driver.close()
    client.__del__()
    return [1e-3 *np.median(time_server), np.median(time_total)*1e6]
