from pyqtgraph.Qt import QtGui, QtCore

class SaveWidget(QtGui.QWidget):
    def __init__(self):
        super(SaveWidget, self).__init__()
        self.layout = QtGui.QVBoxLayout()

        # Save 
        self.save_button = QtGui.QPushButton()
        self.save_button.setStyleSheet('QPushButton {color: green;}')
        self.save_button.setText('Save')
        self.save_button.setCheckable(True)
        self.layout.addWidget(self.save_button)
        self.save_button.clicked.connect(self.save_data)

    def save_data(self):
        filename = QtGui.QFileDialog.getSaveFileName(self, 'Dialog Title')

        if filename:
            print filename
