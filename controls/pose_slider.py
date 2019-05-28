from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QWidget, QLabel, QSlider, QVBoxLayout, QHBoxLayout

import numpy as np
from nibabel import eulerangles

class PoseSlider(QWidget):
    value_changed = QtCore.pyqtSignal(np.ndarray)

    def __init__(self, idx, angle_range, vert_stack = False, label_to_side = True):
        super(PoseSlider, self).__init__()
        self.idx = idx

        self.max_angle = 0.5 * angle_range
        self.min_angle = -0.5 * angle_range

        self.value = np.array([0.0, 0.0, 0.0])
        self.axis_value = self.eul_to_axis(self.value)
        self.eul_value_label = QLabel(self.np_rots_to_label_text(self.value))
        self.axis_value_label = QLabel(self.np_rots_to_label_text(self.axis_value))

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
            min_label = QLabel(str(np.around(self.min_angle, decimals=2)))
            max_label = QLabel(str(np.around(self.max_angle, decimals=2)))

            horiz_layout.addWidget(min_label)
            horiz_layout.addWidget(slider)
            horiz_layout.addWidget(max_label)
            if vert_stack:
                if label_to_side:
                    horiz_layout.addWidget(self.eul_value_label)
                    horiz_layout.addWidget(self.axis_value_label)
                vert_layout.addLayout(horiz_layout)
                horiz_layout = QHBoxLayout()

        if not label_to_side:
            horiz_layout.addWidget(self.eul_value_label)
            horiz_layout.addWidget(self.axis_value_label)
            vert_layout.addLayout(horiz_layout)

        if vert_stack:
            self.setLayout(vert_layout)         
        else:
            horiz_layout.addWidget(self.eul_value_label)
            horiz_layout.addWidget(self.axis_value_label)
            self.setLayout(horiz_layout)  

    def reset(self):
        self.value = np.array([0.0, 0.0, 0.0])
        self.axis_value = self.eul_to_axis(self.value)
        self.eul_value_label.setText(self.np_rots_to_label_text(self.value))
        self.axis_value_label.setText(self.np_rots_to_label_text(self.axis_value))
        self.x_slider.setValue(50)
        self.y_slider.setValue(50)
        self.z_slider.setValue(50)

    def setValue(self, value):
        self.value = value
        self.axis_value = self.eul_to_axis(self.value)
        self.eul_value_label.setText(self.np_rots_to_label_text(self.value))
        self.axis_value_label.setText(self.np_rots_to_label_text(self.axis_value))

        self.x_slider.setValue(self.__rot_to_slider_int(value[0]))
        self.y_slider.setValue(self.__rot_to_slider_int(value[1]))
        self.z_slider.setValue(self.__rot_to_slider_int(value[2]))
        
    def np_rots_to_label_text(self, np_array):
        return str(np.around(np_array, decimals = 2))
    
    def __slider_value_changed(self, value):
        x_value = self.__slider_int_to_float(self.x_slider.value())
        y_value = self.__slider_int_to_float(self.y_slider.value())
        z_value = self.__slider_int_to_float(self.z_slider.value())

        self.value = np.array([x_value, y_value, z_value])
        self.axis_value = self.eul_to_axis(self.value)

        self.eul_value_label.setText(self.np_rots_to_label_text(self.value))
        self.axis_value_label.setText(self.np_rots_to_label_text(self.axis_value))
        self.value_changed.emit(self.axis_value)

    def force_emit(self):
        axis_value = self.eul_to_axis(self.value)
        self.value_changed.emit(self.axis_value)

    def eul_to_axis(self, euler_value):
        theta, vector = eulerangles.euler2angle_axis(euler_value[2], euler_value[1], euler_value[0])
        return vector * theta

    def __rot_to_slider_int(self, rotation):
        total_range = self.max_angle - self.min_angle
        offset = rotation - self.min_angle
        return (offset / total_range) * 100.0

    def __slider_int_to_float(self, slider_val):
        total_range = self.max_angle - self.min_angle
        float_percentage = (total_range / 100.0) * slider_val # slider ranges between [0, 100] so slider_val is just a percentage
        return self.min_angle + float_percentage
