# xadc.py
# Client API for the XADC device
# (c) Koheron 2014-2015 

class Xadc():
    """
    @brief XADC driver
    http://www.xilinx.com/support/documentation/ip_documentation/xadc_wiz/v3_0/pg091-xadc-wiz.pdf
    http://www.xilinx.com/support/documentation/user_guides/ug480_7Series_XADC.pdf
    """
    def __init__(self, dvm, addr = int('0x43C00000',0), map_size = 16 * 4096):
        self.dvm = dvm
        self.dev_num = self.dvm.add_memory_map(addr, map_size)
        self.channel_0 = 1
        self.channel_1 = 8
    
    def set_channel(self, channel_0 = 1, channel_1 = 8):
        self.channel_0 = channel_0
        self.channel_1 = channel_1
        val = (1 << self.channel_0) + (1 << self.channel_1)
        self.dvm.write(self.dev_num, int('0x324',0), val)
        # Average enable
        self.dvm.write(self.dev_num, int('0x32C',0), val)
        
    def set_averaging(self, n_avg = 1):
        reg = int('0b0000000000000000',0)
        if n_avg == 4:
            reg = int('0b0001000000000000',0)
        elif n_avg == 64:
            reg = int('0b0010000000000000',0)
        elif n_avg == 256:
            reg = int('0b0011000000000000',0)
        self.dvm.write(self.dev_num, int('0x300',0), reg)
    
    def read(self, channel):
        offset = int('0x240',0) + 4*channel
        value = self.dvm.read(self.dev_num, offset)
        return value
