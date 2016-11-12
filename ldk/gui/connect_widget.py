# -*- coding: utf-8 -*-

from pyqtgraph.Qt import QtGui, QtCore

import json
import os
import requests
from koheron import connect

class ConnectWidget(QtGui.QWidget):
    def __init__(self, parent, ip_path=None):
        super(ConnectWidget, self).__init__()

        self.parent = parent
        self.app_list = self.parent.app_list
        self.ip_path = ip_path
        self.is_connected = False

        # IP address
        self.create_ip_layout()

        # Connect button and connection information
        self.lay_connection = QtGui.QHBoxLayout()
        self.connect_button = QtGui.QPushButton()
        self.connect_button.setStyleSheet('QPushButton {color: green;}')
        self.connect_button.setText('Connect')
        self.connect_button.setFixedWidth(80)
        self.connection_info = QtGui.QLabel('')
        self.lay_connection.addWidget(self.connect_button)
        self.lay_connection.addWidget(self.connection_info)

        # Add layouts to main layout
        self.lay = QtGui.QVBoxLayout()
        self.lay.addLayout(self.lay_ip)
        self.lay.addLayout(self.lay_connection)
        self.setLayout(self.lay)

        self.retrieve_ip_address()

        for i, line in enumerate(self.lines):
            def make_callback(idx):
                return lambda : self.ip_changed(idx)
            line.textChanged.connect(make_callback(i))

        self.connect_button.clicked.connect(self.connect_onclick)

    def retrieve_ip_address(self):
        if not os.path.exists(self.ip_path):
            os.makedirs(self.ip_path)

        if os.path.exists(self.ip_path):
            try:
                fp = open(os.path.join(self.ip_path, 'ip_address' + '.json'))
                parameters = json.loads(fp.read())
                ip = parameters['ip_address']
            except:
                ip = '192.168.1.100'
            self.set_text_from_ip(ip)

        self.host = self.get_host_from_text()


    def create_ip_layout(self):
        self.lay_ip = QtGui.QHBoxLayout()

        self.lines = []
        for i in range(4):
            self.lines.append(QtGui.QLineEdit())
            self.lines[i].setFixedWidth(40)
            self.lines[i].setAlignment(QtCore.Qt.AlignCenter)

        self.points = []
        for i in range(3):
            self.points.append(QtGui.QLabel('.'))

        self.lay_ip.addWidget(QtGui.QLabel('IP address: '))
        for i in range(3):
            self.lay_ip.addWidget(self.lines[i])
            self.lay_ip.addWidget(self.points[i])
        self.lay_ip.addWidget(self.lines[3])

    def set_text_from_ip(self, ip):
        for i, num in enumerate(ip.split('.')):
            self.lines[i].setText(num)

    def get_host_from_text(self):
        return '.'.join(map(lambda x:str(x.text()), self.lines))

    def ip_changed(self, index):
        self.host = self.get_host_from_text()
        parameters = {}
        parameters['ip_address'] = self.host
        if not os.path.exists(self.ip_path):
            os.makedirs(self.ip_path)
        with open(os.path.join(self.ip_path, 'ip_address' + '.json'), 'w') as fp:
            json.dump(parameters, fp)
        if self.lines[index].cursorPosition() == 3 and index < 3:
            self.lines[index+1].setFocus()
            self.lines[index+1].selectAll()

    def load_instrument(self, instrument_name):
        self.client = load_instrument(self.host, instrument_name)

    def disconnect(self):
        self.is_connected = False
        self.connect_button.setStyleSheet('QPushButton {color: green;}')
        self.connect_button.setText('Connect')
        self.local_instruments = {}
        self.parent.instrument_list = [''] * len(self.app_list)
        self.parent.update_buttons()
        self.connection_info.setText('Disconnected')

    def connect(self):
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        self.connection_info.setText('Connecting to ' + self.host + ' ...')
        self.local_instruments = requests.get('http://{}/api/instruments/local'.format(self.host)).json()
        for i, app in enumerate(self.app_list):
            try:
               instrument = next(instr for instr in self.local_instruments if app in instr)
               self.parent.instrument_list[i] = instrument
            except StopIteration:
               self.parent.instrument_list[i] = ''

        # Load the first instrument available by default
        instrument_name = (next(instr for instr in self.parent.instrument_list if instr))
        self.client = connect(self.host, name=instrument_name)

        self.connection_info.setText('Connected to ' + self.host)
        self.is_connected = True
        self.connect_button.setStyleSheet('QPushButton {color: red;}')
        self.connect_button.setText('Disconnect')
        self.parent.update_buttons()
        QtGui.QApplication.restoreOverrideCursor()

    def connect_onclick(self):
        if self.is_connected:
            self.disconnect()
        else:
            self.connect()
