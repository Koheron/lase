#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import time
from koheron_tcp_client import KClient

def install_instrument(host, instrument_name, always_restart=False):
    if not always_restart:
        # Don't restart the instrument if already launched
        current_instrument = requests.get('http://{}/api/instruments/current'.format(host)).json()
        if current_instrument['name'] == instrument_name:
            return

    instruments = requests.get('http://{}/api/instruments/local'.format(host)).json()
    if instruments:
        for name, shas in instruments.items():
            if name == instrument_name and len(shas) > 0:
                r = requests.get('http://{}/api/instruments/run/{}/{}'.format(host, name, shas[0]))
                if int(r.text.split('status:')[1].strip()) < 0:
                    raise RuntimeError("Instrument " + instrument_name + " launch failed.")
                return
    raise ValueError("Instrument " + instrument_name + " not found")

def load_instrument(host, instrument='oscillo'):
    install_instrument(host, instrument)
    client = KClient(host)
    return client
