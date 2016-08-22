# -*- coding: utf-8 -*-

import os
import pytest
from koheron import KoheronClient
from ..utilities import install_instrument
from ..drivers import Oscillo

@pytest.mark.real
class TestConnection:
      
    def test(self):
        host = os.getenv('HOST','192.168.1.100')
        install_instrument(host, 'oscillo')
        client = KoheronClient(host)  
        assert client.is_connected
        driver = Oscillo(client)
        current = 30 #mA
        driver.set_laser_current(current)
        driver.start_laser()
        assert driver.get_laser_power() > 400
