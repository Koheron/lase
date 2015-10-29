# dac.py
# Client API for the DAC device
# (c) Koheron 2014-2015 

import numpy as np
from kclient import reference_dict

class Dac:
    """
    Dac control
    """
    def __init__(self, client, waveform_size):
        self.client = client

        # Dictionnary of references
        self.ref = reference_dict(self)

        # Operations to be executed at initialization
        self.open(waveform_size)
        self.waveform_size = waveform_size

    def open(self, waveform_size):
        self.client.send_command(self.ref['id'], self.ref['open'], waveform_size)

    def set_dac_constant(self, dac_1_float, dac_2_float):
        self.client.send_command(self.ref['id'], self.ref['set_dac_constant'], dac_1_float, dac_2_float)
        return self.client.recv_buffer(self.waveform_size, data_type = 'float32')
        
    def set_dac(self, data_1, data_2):
        data = np.concatenate((data_1, data_2))
        len_data = len(data)
        self.client.send_command(self.ref['id'], self.ref['set_dac'], len_data)
        self.client.send_handshaking(data, format_char='f')
        


