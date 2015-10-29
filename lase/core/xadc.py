# xadc.py
# Client API for the XADC device
# (c) Koheron 2014-2015 

from kclient import reference_dict

class Xadc:
    """
    XADC driver
    """
    def __init__(self, client, map_size = 16*4096):
        self.client = client

        # Dictionnary of references
        self.ref = reference_dict(self)

        self.open(map_size)
        return

    def open(self, map_size):
        self.client.send_command(self.ref['id'], self.ref['open'], map_size)

    def set_channel(self, channel_0 = 1, channel_1 = 8):
        """
        Select 2 channels among the four available channels (0, 1, 8 and 9)

        Args:
            channel_0: (0, 1, 8 or 9)
            channel_1: (0, 1, 8 or 9)
        """
        self.client.send_command(self.ref['id'], self.ref['set_channel'], channel_0, channel_1)

    def enable_averaging(self):
        """
        Enable averaging
        """
        self.client.send_command(self.ref['id'], self.ref['enable_averaging'])

    def set_averaging(self, n_avg = 1):
        """
        Set number of points averages

        Args:
            n_avg: Number of averages (1, 4, 64 or 256)
        """
        self.client.send_command(self.ref['id'], self.ref['set_averaging'], n_avg)

    def read(self, channel):
        """
        Read XADC value

        Args:
            channel: Channel to be read (1 or 8)
        """
        self.client.send_command(self.ref['id'], self.ref['read'], channel)
        return self.client.recv_int(4)



