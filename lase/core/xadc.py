# xadc.py
# Client API for the XADC device
# (c) Koheron 2014-2015 

from device import Device, command

class Xadc(Device):
    def __init__(self, client):
        super(Xadc, self).__init__(client)
        self.open()

    @command
    def open(self, map_size = 16*4096):
        pass

    @command
    def set_channel(self, channel_0 = 1, channel_1 = 8):
        """ Select 2 channels among the four available channels (0, 1, 8 and 9)

        Args:
            channel_0: 0, 1, 8 or 9
            channel_1: 0, 1, 8 or 9
        """
        pass

    @command
    def enable_averaging(self):
        """ Enable averaging
        """
        pass

    @command
    def set_averaging(self, n_avg = 1):
        """ Set number of points averages

        Args:
            n_avg: Number of averages (1, 4, 64 or 256)
        """
        pass

    @command
    def read(self, channel):
        """ Read XADC value

        Args:
            channel: Channel to be read (1 or 8)
        """
        return self.client.recv_int(4)
