import argparse
import pickle as pkl
from PyQt5.QtWidgets import QApplication

import os
import pyqt_viewer
import numpy as np

def main():
    qapp = QApplication([])
    main_window = pyqt_viewer.MainWindow()

    main_window.setWindowTitle("SMAL Model Viewer")
    main_window.show()
    qapp.exec_()

if __name__ == '__main__':
    main()
