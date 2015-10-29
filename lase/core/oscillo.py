# oscillo.py
# Client API for the OSCILLO device
# (c) Koheron 2014-2015 

from kclient import reference_dict

class Oscillo:
    """
    ADC control
    """
    def __init__(self, client, waveform_size):
        self.client = client

        # Dictionnary of references
        self.ref = reference_dict(self)

        _const_ip_addr = int('0x43C00000',0)
        _adc_1_addr = int('0x40000000',0)
        _adc_2_addr = int('0x42000000',0)
        self.open(_const_ip_addr, _adc_1_addr, _adc_2_addr, waveform_size)
        
        self.waveform_size = waveform_size
        return

    def open(self, _const_ip_addr, _adc_1_addr, _adc_2_addr, waveform_size):
        self.client.send_command(self.ref['id'], self.ref['open'], _const_ip_addr, _adc_1_addr, _adc_2_addr, waveform_size)

    def read_data(self, channel):
        """
        Read the acquired data
        Args:
            channel: Channel to be read (0 or 1)
        """
        self.client.send_command(self.ref['id'], self.ref['read_data'], self.channel)
        return self.client.recv_buffer(self.waveform_size, data_type = 'float32')

        
    def read_all_channels(self):
        """
        Read all the acquired channels
        """
        self.client.send_command(self.ref['id'], self.ref['read_all_channels'])
        return self.client.recv_buffer(2*self.waveform_size, data_type = 'float32')

    def read_all(self):
        return self.read_all_channels()
        
    def set_averaging(self, avg_status):
        """
        Enable/disable averaging

        Args:
            avg_status: Status ON or OFF
        """
        if avg_status:
            status = 1;
        else:
            status = 0;            
        self.client.send_command(self.ref['id'], self.ref['set_averaging'], status)

    def get_num_average(self):
        """
        Number of averages
        """
        self.client.send_command(self.ref['id'], self.ref['get_num_averages'])
        return self.client.recv_int(4)



