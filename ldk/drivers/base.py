#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import math

from ..signal import Sampling
from koheron import command

class Base(object):
    """ This class is used as a base class for `Oscillo` and `Spectrum`

    args:
        wfm_size: number of points in the waveform.
        client : instance of KoheronClient class, used to connect to the board.
    """

    def __init__(self, wfm_size, client):
        self.client = client
        self.n = wfm_size
        self.max_current = 40  # mA
        self.sampling = Sampling(wfm_size, 125e6)

        self.opened = True
        self.dac = np.zeros((2, self.sampling.n))

    def update(self):
        pass  # Used in BaseSimu

    def close(self):
        self.stop_laser()
        self.reset()

    def reset(self):
        self.reset_laser()

    def reset_laser(self):
        @command('Laser')
        def reset(self): pass
        reset(self)

    @command(classname='Laser')
    def start_laser(self): pass

    @command(classname='Laser')
    def stop_laser(self): pass

    @property
    @command(classname='Laser', funcname='get_laser_current')
    def laser_current(self):
        self.__laser_current = (0.0001/21.) * self.client.recv_uint32()
        return self.__laser_current

    @property
    @command(classname='Laser', funcname='get_laser_power')
    def laser_power(self):
        self.__laser_power = self.client.recv_uint32()
        return self.__laser_power

    @command(classname='Laser')
    def get_monitoring(self):
        return self.client.recv_tuple()

    @laser_current.setter
    @command(classname='Laser', funcname='set_laser_current')
    def laser_current(self, current):
        """ current: The bias in mA """
        pass

    @command(classname='Common')
    def init(self): pass

    def twoint14_to_uint32(self, data):
        data1 = np.mod(np.floor(8192 * data[0, :]) + 8192,16384) + 8192
        data2 = np.mod(np.floor(8192 * data[1, :]) + 8192,16384) + 8192
        return data1 + 65536 * data2