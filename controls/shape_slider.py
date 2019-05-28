from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QWidget, QLabel, QSlider, QVBoxLayout, QHBoxLayout

import numpy as np

class ShapeSlider(QWidget):
    value_changed = QtCore.pyqtSignal(float)

    def __init__(self, idx, std_dev, std_offset = 2):
        super(ShapeSlider, self).__init__()
        self.idx = idx
        self.std_offset = std_offset

        self.slider = QSlider(QtCore.Qt.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setValue(50)

        self.value = 0
        self.value_label = QLabel("--")
        self.min_label = QLabel("--")
        self.max_label = QLabel("--")

        self.__set_range_by_std_dev(std_dev)
        
        self.slider.valueChanged[int].connect(self.__slider_value_changed)

        horiz_layout = QHBoxLayout()
        horiz_layout.addWidget(self.min_label)
        horiz_layout.addWidget(self.slider)
        horiz_layout.addWidget(self.max_label)
        horiz_layout.addWidget(self.value_label)

        self.setLayout(horiz_layout)

    def reset(self):
        self.slider.setValue(50)

    def setValue(self, value):
        self.slider.setValue(self.__float_to_slider(value))

    def __set_range_by_std_dev(self, std_dev):
        self.std_dev = std_dev

        min = -1.0 * std_dev * self.std_offset
        max = std_dev * self.std_offset

        min_rnd = np.around(min, decimals=2)
        max_rnd = np.around(max, decimals=2)

        self.min_label.setText(str(min_rnd))
        self.max_label.setText(str(max_rnd))
        self.__slider_value_changed(50)

    def __slider_value_changed(self, value):
        self.value = self.__slider_int_to_float(value)
        self.value_label.setText(str(np.around(self.value, decimals=2)))
        self.value_changed.emit(self.value)
        
    def __float_to_slider(self, float_val):
        total_range = self.std_dev * 2 * self.std_offset
        offset_val = float_val + (self.std_dev * self.std_offset)
        return (offset_val / total_range) * 100

    def __slider_int_to_float(self, slider_val):
        total_range = self.std_dev * 2 * self.std_offset
        float_percentage = (total_range / 100.0) * slider_val # slider ranges between [0, 100] so slider_val is just a percentage
        return (-1.0 * self.std_dev * self.std_offset) + float_percentage
