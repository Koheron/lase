
from pyqtgraph.Qt import QtGui, QtCore
from PyQt4.QtCore import SIGNAL 


class KoheronSlider(QtGui.QWidget):    
    def __init__(self, name ='Value : ', step = 0.01, max_slider = None, alpha=1):
        self.name = name
        super(KoheronSlider, self).__init__() 
        self.value = 0
        self.step = step
        self.flag = True
        self.alpha = alpha # Label value = alpha * spin value
        self.max_slider = max_slider
        self.layout = QtGui.QHBoxLayout() 
        self.label = QtGui.QLabel()
        self.label.setText(self.name)
        self.slider = QtGui.QSlider()
        self.slider.setMinimum(0)
        self.slider.setMaximum(self.max_slider/self.step)
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        
        self.spin = QtGui.QDoubleSpinBox()
        self.spin.setRange(0,self.max_slider)
        self.spin.setSingleStep(self.step)
        self.spin.setFixedSize(QtCore.QSize(59, 26))
        
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
            self.valueChanged()
        
    def spinChanged(self):
        self.flag = False
        self.value = self.spin.value()
        self.slider.setValue(int(self.value/self.step))
        self.valueChanged()
        self.flag = True
        
    def valueChanged(self):
        self.emit(SIGNAL("value(float)"), self.value)