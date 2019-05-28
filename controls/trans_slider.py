from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QWidget, QLabel, QSlider, QVBoxLayout, QHBoxLayout

import numpy as np
from nibabel import eulerangles

class TransSlider(QWidget):
    value_changed = QtCore.pyqtSignal(np.ndarray)

    def __init__(self, idx, min_trans, max_trans, initial_trans, vert_stack = False, label_to_side = True):
        super(TransSlider, self).__init__()
        self.idx = idx
        self.default = initial_trans

        self.max_trans = max_trans
        self.min_trans = min_trans
        self.value_label = QLabel()

        self.x_slider = QSlider(QtCore.Qt.Horizontal)
        self.y_slider = QSlider(QtCore.Qt.Horizontal)
        self.z_slider = QSlider(QtCore.Qt.Horizontal)
        self.sliders = [self.x_slider, self.y_slider, self.z_slider]
            
        vert_layout = QVBoxLayout()
        horiz_layout = QHBoxLayout()
        for slider in self.sliders:
            slider.setRange(0, 100)
            slider.setValue(50)
            slider.valueChanged[int].connect(self.__slider_value_changed)
            min_label = QLabel(str(np.around(self.min_trans, decimals=2)))
            max_label = QLabel(str(np.around(self.max_trans, decimals=2)))

            horiz_layout.addWidget(min_label)
            horiz_layout.addWidget(slider)
            horiz_layout.addWidget(max_label)
            
            if vert_stack:
                if label_to_side:
                    horiz_layout.addWidget(self.value_label)
                vert_layout.addLayout(horiz_layout)
                horiz_layout = QHBoxLayout()

        if not label_to_side:
            horiz_layout.addWidget(self.value_label)
            vert_layout.addLayout(horiz_layout)

        if vert_stack:
            self.setLayout(vert_layout)         
        else:
            horiz_layout.addWidget(self.value_label)
            self.setLayout(horiz_layout)    

        self.setValue(initial_trans)

    def reset(self):
        self.setValue(self.default)
        
    def setValue(self, value):
        self.value = value
        self.value_label.setText(self.np_to_label_text(self.value))
        
        self.x_slider.setValue(self.__np_to_slider_int(value[0]))
        self.y_slider.setValue(self.__np_to_slider_int(value[1]))
        self.z_slider.setValue(self.__np_to_slider_int(value[2]))
        
    def np_to_label_text(self, np_array):
        return str(np.around(np_array, decimals = 2))
    
    def __slider_value_changed(self, value):
        x_value = self.__slider_int_to_np(self.x_slider.value())
        y_value = self.__slider_int_to_np(self.y_slider.value())
        z_value = self.__slider_int_to_np(self.z_slider.value())

        self.value = np.array([x_value, y_value, z_value])

        self.value_label.setText(self.np_to_label_text(self.value))
        self.value_changed.emit(self.value)

    def __np_to_slider_int(self, rotation):
        total_range = self.max_trans - self.min_trans
        offset = rotation - self.min_trans
        return (offset / total_range) * 100.0

    def __slider_int_to_np(self, slider_val):
        total_range = self.max_trans - self.min_trans
        float_percentage = (total_range / 100.0) * slider_val # slider ranges between [0, 100] so slider_val is just a percentage
        return self.min_trans + float_percentage
