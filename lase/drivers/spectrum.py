#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import numpy as np
from lase import Lase


class Spectrum(Lase):
    """
    @brief Driver for the spectrum bitstream
    """
    
    def __init__(self, client, map_size = 4096, verbose = False, current_mode = 'pwm'): 
        n = 4096
        super(Spectrum, self).__init__(n, client, map_size = 4096, current_mode = 'pwm')   
                
        # addresses
        _spectrum_addr = int('0x40000000',0)
        _demod_addr = int('0x42000000',0)
        # \end
        
        # offsets
        self._subtract_mean_re_off = 16
        self._subtract_mean_im_off = 20      
        self._scale_sch_off = 24  

        # Add memory maps
        self._spectrum = self.dvm.add_memory_map(_spectrum_addr, self.sampling.n/1024*map_size)
        self._demod = self.dvm.add_memory_map(_demod_addr, self.sampling.n/1024*map_size)

        self.spectrum = np.zeros(self.sampling.n, dtype=np.float32)
        self.demod = np.zeros((2,self.sampling.n))
        
        #demod = np.exp(2*np.pi*1j*self.fs/8*self.t)       
        self.demod[0,:] = 0.49 * (1-np.cos(2*np.pi*np.arange(self.sampling.n)/self.sampling.n))   #0.5*np.real(demod) 
        self.demod[1,:] = 0#0.5*np.imag(demod)
        
        self.set_offset(0)

        self.set_demod()
        self.dvm.write(self._const_ip,self._scale_sch_off, 0)
        
        self.reset()
    
    def set_scale_sch(self, scale_sch):
        self.dvm.write(self._const_ip,self._scale_sch_off, scale_sch)           
           
    def set_offset(self, offset):
        self.dvm.write(self._const_ip,self._subtract_mean_re_off, offset)
        self.dvm.write(self._const_ip,self._subtract_mean_im_off, offset)    

    def set_demod(self, warning=False):
        if warning:
            if np.max(np.abs(self.demod)) >= 1:
                print 'WARNING : dac out of bounds'                
        demod_data_1 = np.mod(np.floor(8192*self.demod[0,:]) + 8192,16384)+8192
        demod_data_2 = np.mod(np.floor(8192*self.demod[1,:]) + 8192,16384)+8192
        self.dvm.write_buffer(self._demod, 0, demod_data_1 + 65536 * demod_data_2)
        
    def get_spectrum(self):
        self.dvm.write(self._const_ip,self._trig_acq_off,1) 
        time.sleep(0.001)
        self.spectrum = self.dvm.read_buffer(self._spectrum, 0, self.sampling.n, data_type='float32')
        n_avg = self.dvm.read(self._const_ip,self._n_avg_off)
        self.spectrum = self.spectrum / np.float(n_avg)
        self.dvm.write(self._const_ip,self._trig_acq_off,0)
        
