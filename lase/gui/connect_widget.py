# -*- coding: utf-8 -*-

from pyqtgraph.Qt import QtGui, QtCore
import json, os
from lase.core import ZynqSSH, KClient

class ConnectWidget(QtGui.QWidget):
    def __init__(self, parent, ip_path=None):
        super(ConnectWidget, self).__init__()
        
        self.parent = parent
        self.ip_path = ip_path
        self.host = ''
        self.password = 'changeme'
        
        self.is_connected = False
        
        self.lay = QtGui.QVBoxLayout()
        
        self.lay_ip = QtGui.QHBoxLayout()
        self.lay_password = QtGui.QHBoxLayout()
        self.lay_connection = QtGui.QHBoxLayout()
        
        self.line = []        
        for i in range(4):
            self.line.append(QtGui.QLineEdit()) 
            self.line[i].setFixedWidth(40)
            self.line[i].setAlignment(QtCore.Qt.AlignCenter)
        
        self.point = []
        for i in range(3):
            self.point.append(QtGui.QLabel('.'))
            
        self.lay_ip.addWidget(QtGui.QLabel('IP address: '))    
        for i in range(3):
            self.lay_ip.addWidget(self.line[i])
            self.lay_ip.addWidget(self.point[i])
        self.lay_ip.addWidget(self.line[3])
        
        self.lay_password.addWidget(QtGui.QLabel('Password:')) 
        self.password_widget = QtGui.QLineEdit()
        self.password_widget.setEchoMode(QtGui.QLineEdit.Password)
        self.lay_password.addWidget(self.password_widget)

        self.connect_button = QtGui.QPushButton()
        self.connect_button.setStyleSheet('QPushButton {color: green;}')
        self.connect_button.setText('Connect')
        self.connect_button.setFixedWidth(80)
        
        self.lay_connection.addWidget(self.connect_button)
        
        self.lay.addLayout(self.lay_ip)
        self.lay.addLayout(self.lay_password)
        
        
        self.connection_info = QtGui.QLabel('')
        self.lay_connection.addWidget(self.connection_info)
        
        self.lay.addLayout(self.lay_connection)
        
        
        self.setLayout(self.lay)
        
        if not os.path.exists(self.ip_path):
            os.makedirs(self.ip_path)
            
        if os.path.exists(self.ip_path):
            try:
                with open(os.path.join(self.ip_path, 'ip_address' + '.json')) as fp:
                    json_data = fp.read()
                    parameters = json.loads(json_data)
                    IP = parameters['TCP_IP']
            except:
                IP = ['192','168','1','1']
            for i in range(4):
                self.line[i].setText(str(IP[i]))
                
        for i in range(3):
            self.host += self.line[i].text() + '.'
            
        self.host += self.line[3].text() 
        self.host = str(self.host)
        
        self.line[0].textChanged.connect(lambda: self.ip_changed(0))
        self.line[1].textChanged.connect(lambda: self.ip_changed(1))
        self.line[2].textChanged.connect(lambda: self.ip_changed(2))
        self.line[3].textChanged.connect(lambda: self.ip_changed(3))
        
        self.connect_button.clicked.connect(self.connect)
            
    def ip_changed(self, index):
        self.host = ''
        IP = []
        for i in range(3):
            self.host += self.line[i].text() + '.'
        self.host += self.line[3].text() 
        self.host = str(self.host)
        for i in range(4):
            IP.append(str(self.line[i].text())) 
        parameters = {}
        parameters['TCP_IP'] = IP
        if not os.path.exists(self.ip_path):
            os.makedirs(self.ip_path)
            
        with open(os.path.join(self.ip_path, 'ip_address' + '.json'), 'w') as fp:
            json.dump(parameters, fp)
        if self.line[index].cursorPosition() == 3 and index < 3 :
            self.line[index+1].setFocus()
            self.line[index+1].selectAll()
            
    def connect(self):
        if not self.is_connected:
            self.client = KClient(self.host)
            self.connection_info.setText('Connecting to '+self.host+' ...')
            if self.client.is_connected:
                self.connection_info.setText('Connected to '+self.host)
                self.is_connected = True
                self.connect_button.setStyleSheet('QPushButton {color: red;}')
                self.connect_button.setText('Disconnect')
                self.parent.connected()
                self.password = str(self.password_widget.text())
                self.ssh = ZynqSSH(self.host, self.password)

            else:
                self.connection_info.setText('Failed to connect to '+self.host)
                
        else:
            if hasattr(self,'client'):
                self.client.__del__()
            self.connection_info.setText('Disconnected')    
            self.parent.disconnected()
            self.connect_button.setStyleSheet('QPushButton {color: green;}')
            self.connect_button.setText('Connect')
            self.is_connected = False
        
            
