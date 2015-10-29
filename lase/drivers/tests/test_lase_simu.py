# -*- coding: utf-8 -*-

from ..lase_simu import LaseSimu

class TestLaseSimu:
      
    def test_laser_enable(self):
        n = 8192
        lase_simu = LaseSimu(n)
        laser_current = 1000 * lase_simu.model._laser_threshold + 10
        lase_simu.set_laser_current(laser_current)
        lase_simu.update()
        assert lase_simu.get_laser_power() == 0
        lase_simu.start_laser()
        lase_simu.update()
        assert lase_simu.get_laser_power() > 0
        lase_simu.stop_laser()
        lase_simu.update()
        assert lase_simu.get_laser_power() == 0
