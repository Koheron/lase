# -*- coding: utf-8 -*-

import os
from lase.core import KClient
from lase.core import ZynqSSH
from lase.drivers import Oscillo

class TestConnection:
      
    def test(self):
        current_path = os.getcwd()
        bitstreams_path = os.path.join(current_path,'bitstreams')
        host = os.getenv('HOST','192.168.1.100')
        client = KClient(host)        
        assert client.is_connected
        ssh = ZynqSSH(host, 'koheron')
        ssh.load_pl(os.path.join(bitstreams_path, 'oscillo.bit'))
        driver = Oscillo(client, current_mode='pwm')
        current = 30 #mA
        driver.set_laser_current(current)
        driver.start_laser()
        assert driver.get_laser_power() > 400
