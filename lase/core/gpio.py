# gpio.py
# GPIO interface
# (c) Koheron 2015 

from device import Device, command

class Gpio(Device):
    def __init__(self, client):
        super(Gpio, self).__init__(client)
        self.open()
        
    @command
    def open(self, map_size = 16 * 4096):
        pass

    @command
    def set_bit(self, index, channel = 1):
        """
        Args:
            index: Position of the bit to set
            channel: GPIO channel
        """
        pass

    @command
    def clear_bit(self, index, channel = 1):
        """
        Args:
            index: Position of the bit to clear
            channel: GPIO channel
        """
        pass

    @command
    def toggle_bit(self, index, channel = 1):
        """
        Args:
            index: Position of the bit to toggle
            channel: GPIO channel
        """
        pass

    @command
    def set_as_input(self, index, channel = 1):
        """ Set a bit direction as input

        Args:
            index: Position of the bit to set
            channel: GPIO channel
        """
        pass

    @command
    def set_as_output(self, index, channel = 1):
        """ Set a bit direction as output

        Args:
            index: Position of the bit to set
            channel: GPIO channel
        """
        pass


