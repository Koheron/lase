
from pyqtgraph.Qt import QtGui, QtCore
#from PyQt4.QtCore import SIGNAL


class SliderWidget(QtGui.QWidget):

    valueChanged = QtCore.pyqtSignal([float])

    def __init__(self, name ='Value : ', step = 0.01, min_slider = 0, max_slider = None, layout=True):
        self.name = name
        super(SliderWidget, self).__init__()
        self.value = 0
        self.step = step
        self.flag = True
        self.min_slider = min_slider
        self.max_slider = max_slider

        self.label = QtGui.QLabel()
        self.label.setText(self.name)
        self.slider = QtGui.QSlider()
        self.slider.setMinimum(self.min_slider/self.step)
        self.slider.setMaximum(self.max_slider/self.step)
        self.slider.setOrientation(QtCore.Qt.Horizontal)

        if int(step) == step:
            self.spin = QtGui.QSpinBox()
        else:
            self.spin = QtGui.QDoubleSpinBox()

        self.spin.setRange(self.min_slider,self.max_slider)
        self.spin.setSingleStep(self.step)
        self.spin.setFixedSize(QtCore.QSize(59, 26))

        if layout:
            self.layout = QtGui.QHBoxLayout()
            self.layout.addWidget(self.label)
            self.layout.addWidget(self.spin)
            self.layout.addWidget(self.slider)
            self.setLayout(self.layout)

        self.slider.valueChanged.connect(self.sliderChanged)
        self.spin.valueChanged.connect(self.spinChanged)



    def sliderChanged(self):
        if self.flag == True:
            self.value = self.slider.value()*self.step
            self.spin.setValue(self.value)
            self.valueChanged.emit()

    def spinChanged(self):
        self.flag = False
        self.value = self.spin.value()
        self.slider.setValue(int(self.value/self.step))
        self.valueChanged.emit()
        self.flag = True
