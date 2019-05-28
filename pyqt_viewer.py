# Imports
import numpy as np
import torch

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow, QWidget, QFrame, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QScrollArea, QGridLayout, QCheckBox
from PyQt5.QtGui import QImage

from pyqt_helpers import image_to_pixmap, createPolyData, image_to_pixmap

from controls.shape_slider import ShapeSlider
from controls.pose_slider import PoseSlider
from controls.trans_slider import TransSlider

import matplotlib.pyplot as plt
from operator import itemgetter
from functools import partial

import os
import collections

import scipy.misc
import datetime

from smal.smal3d_renderer import SMAL3DRenderer
import pickle as pkl

NUM_POSE_PARAMS = 32
NUM_SHAPE_PARAMS = 41
DISPLAY_SIZE = 512
SMAL_DATA_PATH = 'smal/smal_CVPR2017_data.pkl'

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.smal_params = {
            'betas' : torch.zeros(1, NUM_SHAPE_PARAMS).cuda(),
            'joint_rotations' : torch.zeros(1, NUM_POSE_PARAMS, 3).cuda(),
            'global_rotation' :  torch.zeros(1, 1, 3).cuda(),
            'trans' : torch.zeros(1, 1, 3).cuda(),
        }

        self.model_renderer = SMAL3DRenderer(DISPLAY_SIZE)
        self.faces_np = self.model_renderer.smal_model.faces.cpu().numpy()

        with open(SMAL_DATA_PATH, 'rb') as f:
            u = pkl._Unpickler(f)
            u.encoding = 'latin1'
            smal_data = u.load()

        self.toy_betas = smal_data['toys_betas']
        self.setup_ui()

    def get_layout_region(self, control_set):
        layout_region = QVBoxLayout()

        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollAreaWidgetContents = QWidget(scrollArea)
        scrollArea.setWidget(scrollAreaWidgetContents)
        scrollArea.setMinimumWidth(750)

        grid_layout = QGridLayout()

        for idx, (label, com_slider) in enumerate(control_set):
            grid_layout.addWidget(label, idx, 0)
            grid_layout.addWidget(com_slider, idx, 1)
        
        scrollAreaWidgetContents.setLayout(grid_layout)

        layout_region.addWidget(scrollArea)
        return layout_region

    def setup_ui(self):
        self.shape_controls = []
        self.pose_controls = []
        self.update_poly = True
        self.toy_pbs = []

        def ctrl_layout_add_separator():
            line = QFrame()
            line.setFrameShape(QFrame.HLine)
            line.setFrameShadow(QFrame.Sunken)
            ctrl_layout.addWidget(line)

        # SHAPE REGION
        std_devs = np.std(self.toy_betas, axis=1)
        for idx, toy_std in enumerate(std_devs):
            label = QLabel("S{0}".format(idx))
            sliders = ShapeSlider(idx, toy_std)
            sliders.value_changed.connect(self.update_model)
            self.shape_controls.append((label, sliders))
            self.toy_pbs.append(QPushButton("T{0}".format(idx)))

        reset_shape_pb = QPushButton('Reset Shape')
        reset_shape_pb.clicked.connect(self.reset_shape)

        self.toy_frame = QFrame()
        self.toy_layout = QGridLayout()
        for idx, pb in enumerate(self.toy_pbs):
            row = idx // 5
            col = idx - row * 5
            pb.clicked.connect(partial(self.make_toy_shape, idx))
            self.toy_layout.addWidget(pb, row, col)

        self.toy_frame.setLayout(self.toy_layout)
        self.toy_frame.setHidden(True)

        show_toys_cb = QCheckBox('Show Toys', self)
        show_toys_cb.stateChanged.connect(partial(self.toggle_control, self.toy_frame))
        
        shape_layout = self.get_layout_region(self.shape_controls)
        shape_layout.addWidget(reset_shape_pb)
        shape_layout.addWidget(show_toys_cb)

        ctrl_layout = QVBoxLayout()
        ctrl_layout.addLayout(shape_layout)
        ctrl_layout.addWidget(self.toy_frame)
        ctrl_layout_add_separator()

        # POSE REGION
        model_joints = NUM_POSE_PARAMS
        for idx in range(model_joints):
            if idx == 0:
                label = QLabel("Root Pose (P{0})".format(idx))
                slider = PoseSlider(idx, 2 * np.pi, vert_stack = True)
            else:
                label = QLabel("P{0}".format(idx))
                slider = PoseSlider(idx, np.pi)

            slider.value_changed.connect(self.update_model)
            self.pose_controls.append((label, slider))

        reset_pose_pb = QPushButton('Reset Pose')
        reset_pose_pb.clicked.connect(self.reset_pose)

        root_pose_dict = collections.OrderedDict()
        root_pose_dict[ "Face Left" ] = np.array([0, 0, np.pi])
        root_pose_dict[ "Diag Left" ] = np.array([0, 0, 3 * np.pi / 2])
        root_pose_dict[ "Head On" ] = np.array([0, 0, np.pi / 2])
        root_pose_dict[ "Diag Right" ] = np.array([0, 0, np.pi / 4])
        root_pose_dict[ "Face Right" ] = np.array([0, 0, 0])
        root_pose_dict[ "Straight Up" ] = np.array([np.pi / 2, 0, np.pi / 2])
        root_pose_dict[ "Straight Down" ] = np.array([-np.pi / 2, 0, np.pi / 2])

        root_pose_layout = QGridLayout()
        idx = 0
        for key, value in root_pose_dict.items():
            head_on_pb = QPushButton(key)
            head_on_pb.clicked.connect(partial(self.set_known_pose, value))
            root_pose_layout.addWidget(head_on_pb, 0, idx)
            idx = idx + 1
   
        pose_layout = QGridLayout()
        root_label, root_pose_sliders = self.pose_controls[0]

        pose_layout.addWidget(root_label, 0, 0)
        pose_layout.addWidget(root_pose_sliders, 1, 0)
        pose_layout.addLayout(self.get_layout_region(self.pose_controls[1:]), 2, 0)
        pose_layout.addWidget(reset_pose_pb)

        ctrl_layout.addLayout(pose_layout)
        ctrl_layout.addLayout(root_pose_layout)
        ctrl_layout_add_separator()

        # TRANSLATION REGION
        trans_label = QLabel("Root Translation".format(idx))
        self.trans_sliders = TransSlider(idx, -5.0, 5.0, np.array([0.0, 0.0, 0.0]), vert_stack = True)
        self.trans_sliders.value_changed.connect(self.update_model)

        reset_trans_pb = QPushButton('Reset Translation')
        reset_trans_pb.clicked.connect(self.reset_trans)
          
        # Add the translation slider
        trans_layout = QGridLayout()
        trans_layout.addWidget(trans_label, 0, 0)
        trans_layout.addWidget(self.trans_sliders, 1, 0)
        trans_layout.addWidget(reset_trans_pb, 2, 0)

        self.trans_frame = QFrame()
        self.trans_frame.setLayout(trans_layout)
        self.trans_frame.setHidden(True)

        show_trans_cb = QCheckBox('Show Translation Parameters', self)
        show_trans_cb.stateChanged.connect(partial(self.toggle_control, self.trans_frame))

        ctrl_layout.addWidget(show_trans_cb)
        ctrl_layout.addWidget(self.trans_frame)
        ctrl_layout_add_separator()

        # ACTION BUTTONS
        reset_pb = QPushButton('&Reset')
        reset_pb.clicked.connect(self.reset_model)

        export_image_pb = QPushButton('&Export Image')
        export_image_pb.clicked.connect(self.export_image)

        misc_pbs_layout = QGridLayout() 
        misc_pbs_layout.addWidget(reset_pb, 0, 0)
        misc_pbs_layout.addWidget(export_image_pb, 0, 1)
        ctrl_layout.addLayout(misc_pbs_layout)
        ctrl_layout_add_separator()

        view_layout = QVBoxLayout()
        self.render_img_label = QLabel()
        view_layout.addWidget(self.render_img_label)

        main_layout = QHBoxLayout()
        main_layout.addLayout(ctrl_layout)
        main_layout.addLayout(view_layout, stretch=1)

        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        
        # WINDOW
        self.window_title_stem = 'SMAL Model Viewer'
        self.setWindowTitle(self.window_title_stem)
        
        self.statusBar().showMessage('Ready...')
        self.update_render()
        
        self.showMaximized()

    def update_model(self, value):
        sender = self.sender()

        if type(sender) is ShapeSlider:
            self.smal_params['betas'][0, sender.idx] = value
        elif type(sender) is PoseSlider:
            if sender.idx == 0:
                self.smal_params['global_rotation'][0, sender.idx] = torch.FloatTensor(value).cuda()
            else:
                self.smal_params['joint_rotations'][0, sender.idx - 1] = torch.FloatTensor(value).cuda()
        elif type(sender) is TransSlider:
            self.smal_params['trans'][0] = torch.FloatTensor(value).cuda()

        if self.update_poly:
            self.update_render()

    def update_render(self):
        with torch.no_grad():
            rendered_images, rendered_silhouettes, rendered_joints, verts, joints_3d = self.model_renderer(self.smal_params)
        
        image_np = rendered_images[0].permute(1, 2, 0).cpu().numpy()
        verts_np = verts[0].cpu().numpy()
        
        poly_data = createPolyData(verts_np, self.faces_np)
        self.render_img_label.setPixmap(image_to_pixmap(image_np, DISPLAY_SIZE))
        self.render_img_label.update()

    def reset_shape(self):
        # Reset sliders to zero
        self.update_poly = False
        for label, com_slider in self.shape_controls:
            com_slider.reset()
        self.update_poly = True
        self.update_render()

    def reset_pose(self):
        self.update_poly = False
        for label, com_slider in self.pose_controls:
            com_slider.reset()
        self.update_poly = True
        self.update_render()

    def make_toy_shape(self, toy_id):
        self.update_poly = False
        toy_betas = self.toy_betas[toy_id]
        for idx, val in enumerate(toy_betas):
            label, shape_slider = self.shape_controls[idx]
            shape_slider.setValue(val)

        self.update_poly = True
        self.statusBar().showMessage(str(toy_betas))
        self.smal_params['betas'][0] = torch.from_numpy(toy_betas).cuda()
        self.update_render()

    def toggle_control(self, layout):
        sender = self.sender()
        layout.setHidden(not sender.isChecked())
            
    def set_known_pose(self, pose):
        label, root_pose_slider = self.pose_controls[0]
        root_pose_slider.setValue(pose)
        root_pose_slider.force_emit()

    def reset_trans(self):
        self.trans_sliders.reset()

    def reset_model(self):
        self.reset_shape()
        self.reset_pose()
        self.reset_trans()

    def export_image(self):
        pretty_image = self.generate_renderer(silhouette = False)
        sil_image = self.generate_renderer(silhouette = True)

        pretty_small = scipy.misc.imresize(pretty_image, [256, 256])
        sil_small = scipy.misc.imresize(sil_image, [256, 256], 'nearest')

        time_str = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        scipy.misc.imsave(os.path.join("output", "pretty_{0}.png".format(time_str)), pretty_small)
        scipy.misc.imsave(os.path.join("output", "sil_{0}.png".format(time_str)), sil_small)
        
        plt.figure()
        plt.subplot(121)
        plt.imshow(pretty_image)
        plt.subplot(122)
        plt.imshow(sil_image)
        plt.show()


