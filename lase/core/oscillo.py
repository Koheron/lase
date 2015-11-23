# oscillo.py
# Client API for the OSCILLO device
# (c) Koheron 2014-2015 

from device import command

class Oscillo(object):
    def __init__(self, client, waveform_size):
        self.client = client
        self.ref = reference_dict(self)
        
        config_addr = int('0x60000000',0)
        adc_1_addr  = int('0x42000000',0)
        adc_2_addr  = int('0x44000000',0)
        self.open(const_ip_addr, adc_1_addr, adc_2_addr, waveform_size)
        
        self.waveform_size = waveform_size

    @command
    def open(self, _const_ip_addr, _adc_1_addr, _adc_2_addr, waveform_size):
        pass

    @command
    def read_data(self, channel):
        """ Read the acquired data of a given channel
        
        Args:
            channel: Channel to be read (0 or 1)
        """
        return self.client.recv_buffer(self.waveform_size, data_type = 'float32')

    @command
    def read_all_channels(self):
        """ Read all the acquired channels
        """
        return self.client.recv_buffer(2*self.waveform_size, data_type = 'float32')

    def read_all(self):
        return self.read_all_channels()
        
    def set_averaging(self, avg_status):
        """ Enable/disable averaging
        
        Args:
            avg_status: Status ON or OFF
        """
        if avg_status:
            status = 1;
        else:
            status = 0;   
            
        @command
        def set_averaging(self, status):  
            pass
            
        set_averaging(self, status)

    @command
    def get_num_average(self):
        """ Number of averages
        """
        return self.client.recv_int(4)



