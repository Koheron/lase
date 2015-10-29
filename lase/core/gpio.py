# gpio.py
# Client API for the GPIO device
#
# (c) Koheron 2014-2015 

from kclient import reference_dict

class Gpio:
    """
    GPIO driver
    """
    def __init__(self, client, map_size = 16 * 4096):
        self.client = client

        # Dictionnary of references
        self.ref = reference_dict(self)
        self.open(map_size)
        return

    def open(self, map_size):
        self.client.send_command(self.ref['id'], self.ref['open'], map_size)

    def set_bit(self, index, channel = 1):
        """
        Args:
            index: Position of the bit to set
            channel: GPIO channel
        """
        self.client.send_command(self.ref['id'], self.ref['set_bit'], index, channel)

    def clear_bit(self, index, channel = 1):
        """
        Args:
            index: Position of the bit to erase
            channel: GPIO channel
        """
        self.client.send_command(self.ref['id'], self.ref['clear_bit'], index, channel)

    def toggle_bit(self, index, channel = 1):
        """
        Toggle a bit

        Args:
            index: Position of the bit to set
            channel: GPIO channel
        """
        self.client.send_command(self.ref['id'], self.ref['toggle_bit'], index, channel)

    def set_as_input(self, index, channel = 1):
        """
        Set a bit direction as input

        Args:
            index: Position of the bit to set
            channel: GPIO channel
        """
        self.client.send_command(self.ref['id'], self.ref['set_as_input'], index, channel)

    def set_as_output(self, index, channel = 1):
        """
        Set a bit direction as output

        Args:
            index: Position of the bit to set
            channel: GPIO channel
        """
        self.client.send_command(self.ref['id'], self.ref['set_as_output'], index, channel)

