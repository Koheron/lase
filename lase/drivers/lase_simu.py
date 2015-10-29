#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from ..models import LaseModel
from ..signal import Sampling

class LaseSimu(object):
    """
    This class is used as a base class for `OscilloSimu` and `SpectrumSimu`
    
    args:
        n (int): number of points in the waveform (ex: n = 8192)
        
    """
    
    def __init__(self, n):
        
         
        self.max_current = 50 # mA
        
        self.sampling = Sampling(n, 125e6)
        
        self.opened = True
 
        self.dac = np.zeros((2,self.sampling.n)) # V
        
        self._laser_current = 0
        self._laser_enable = False
        self._laser_power = 0
        
        # Lase model
        self.model = LaseModel(self.sampling)
        
        self._live_laser_current = np.zeros(self.sampling.n) # A
        self._live_laser_power = np.zeros(self.sampling.n) # W
        self._live_laser_frequency = np.zeros(self.sampling.n) # Hz
        
    def update(self):
        self.get_live_current()
        self.get_live_laser_power()
        self.get_live_laser_frequency()
        self.get_live_mach_zehnder_power()
        self._laser_power = np.mean(self._live_laser_power)
        
    def close(self):
        self.opened = False
        
    def reset(self):       
        self.stop_laser()
        self.set_laser_current(0)
        
    def stop_laser(self):
        self._laser_enable = False
        
    def get_laser_current(self):
        return self._laser_current
        
    def get_laser_power(self):
        return self._laser_power
    
    def start_laser(self):
        self._laser_enable = True
        
    def set_laser_current(self, current):
        # Current in mA
        self._laser_current = current / 1000
             
    def set_dac(self, warning=False):
        pass
        
    def get_bitstream_id(self):
        return 42        
    
    def set_led(self, ip):
        print 'LED set to ', ip
        
    def get_live_current(self):
            self._live_laser_current = self.model.laser_current( \
                self._laser_enable, \
                self._laser_current, \
            self.dac[1,:])
            
    def get_live_laser_frequency(self):
        self._live_laser_frequency = self.model.laser_frequency(self._live_laser_current)
            
    def get_live_laser_power(self):
        self._live_laser_power = self.model.laser_power(self._live_laser_current)
    
    def get_live_mach_zehnder_power(self):
        self._live_mach_zehnder_power = self.model.mach_zehnder_power(self._live_laser_frequency, self._live_laser_power)