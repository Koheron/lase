# dac.py
# Client API for the DAC device
# (c) Koheron 2014-2015 

from device import Device, command
import numpy as np

class Dac(Device):
    def __init__(self, client, waveform_size):
        super(Dac, self).__init__(client)
        self.open(waveform_size)
        self.waveform_size = waveform_size

    @command
    def open(self, waveform_size):
        pass
   
    @command
    def set_dac_constant(self, dac_1_float, dac_2_float):
        pass
        
    def set_dac(self, data_1, data_2):
        @command
        def set_dac(self, len_data):
            pass
            
        data = np.concatenate((data_1, data_2))
        set_dac(self, len(data))
        self.client.send_handshaking(data, format_char='f')

