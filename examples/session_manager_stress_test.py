#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This program opens repeatedly a client but do not all __del__.

A forgotten mutex in DeleteSession was inducing memory faults in the std::map sessions container.

Keep this program as a stress test for the session manager.
"""

import initExample
from lase.core import KClient

def session_manager_bug(host):
    client = KClient(host)
# To do things properly, we should call
#    client.__del__()
# but we don't do it to stress test the session manager.

for i in range(50):
    session_manager_bug('192.168.1.7')
