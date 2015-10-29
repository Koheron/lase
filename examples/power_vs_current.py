#!/usr/bin/env python
# -*- coding: utf-8 -*-

import initExample

from lase.core import KClient
from lase.drivers import Oscillo

import matplotlib.pyplot as plt
import time

# Connect to Lase
host = '192.168.1.12'
client = KClient(host)
driver = Oscillo(client)

# Enable laser
driver.start_laser()

laser_current = [0,5,10,15,20,25,30,35,40] #mA
laser_power = []

for current in laser_current:
    driver.set_laser_current(current)
    time.sleep(0.1)
    laser_power.append(driver.get_laser_power())


plt.plot(laser_current, laser_power)
plt.xlabel('Laser current (mA)')
plt.ylabel('Laser power (u.a.)')
plt.show()

driver.stop_laser()
driver.close()
