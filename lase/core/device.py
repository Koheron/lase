# @file device.py
#
# @brief Base class for devices
#
# @author Thomas Vanderbruggen <thomas@koheron.com>
# @date 28/10/2015
#
# (c) Koheron 2015

from kclient import KClient, reference_dict

# --------------------------------------------
# Decorators
# --------------------------------------------

def command(func):
    def decorator(self, *args):
        self.client.send_command(self.ref['id'], self.ref[func.__name__], *args)
        return func(self, *args)
    return decorator

# --------------------------------------------
# Base class
# --------------------------------------------

class Device(object):
    def __init__(self, client):
        self.client = client
        self.ref = reference_dict(self)
