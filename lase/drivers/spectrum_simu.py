#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from lase_simu import LaseSimu


class SpectrumSimu(LaseSimu):
    
    def __init__(self): 
        n = 4096
        super(SpectrumSimu, self).__init__(n)
                
        self.spectrum = np.zeros(self.sampling.n, dtype=np.float32)
        self.demod = np.zeros((2,self.sampling.n))
        
        #demod = np.exp(2*np.pi*1j*self.fs/8*self.t)       
        self.demod[0,:] = 0.49 * (1-np.cos(2*np.pi*np.arange(self.sampling.n)/self.sampling.n))           #0.5*np.real(demod) 
        self.demod[1,:] = 0#0.5*np.imag(demod)
        
        self.reset()
    
    def get_spectrum(self):
        pass
        
