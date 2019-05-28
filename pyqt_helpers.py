from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QImage
import vtk
from vtk.util.numpy_support import numpy_to_vtk, numpy_to_vtkIdTypeArray, vtk_to_numpy
import numpy as np

# def toQImage(self, im, copy=False):
#         if im is None:
#             return QImage()

#         if im.dtype == np.uint8:
#             if len(im.shape) == 2:
#                 qim = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_Indexed8)
#                 qim.setColorTable(gray_color_table)
#                 return qim.copy() if copy else qim

#             elif len(im.shape) == 3:
#                 if im.shape[2] == 3:
                    
#                 elif im.shape[2] == 4:
#                     qim = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_ARGB32)
#                     return qim.copy() if copy else qim

def image_to_pixmap(img, img_size):
    im = np.require(img * 255.0, dtype='uint8')
    qim = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_RGB888).copy()
    pixmap = QPixmap(qim)
    return pixmap.scaled(img_size, img_size, QtCore.Qt.KeepAspectRatio)


def createPolyData(verts, tris):
    """Create and return a vtkPolyData.
    
    verts is a (N, 3) numpy array of float vertices

    tris is a (N, 1) numpy array of int64 representing the triangles
    (cells) we create from the verts above.  The array contains 
    groups of 4 integers of the form: 3 A B C
    Where 3 is the number of points in the cell and A B C are indexes
    into the verts array.
    """
    
    triangles = np.concatenate([np.ones_like(tris)[:, [0]] * 3, tris], axis = 1).reshape(-1).astype(np.int64)
    poly = vtk.vtkPolyData()
    
    points = vtk.vtkPoints()
    points.SetData(numpy_to_vtk(verts))        
    poly.SetPoints(points)
    
    cells = vtk.vtkCellArray()
    cells.SetCells(tris.shape[0], numpy_to_vtkIdTypeArray(triangles))        
    poly.SetPolys(cells)
    
    return poly

def vtkPolyData_to_numpy(polyData):
    points = vtk_to_numpy(polyData.GetPoints().GetData())
    trilist = vtk_to_numpy(polyData.GetPolys().GetData())
    return points, trilist.reshape([-1, 4])[:, 1:]

def vtkMatrix_to_numpy(matrix):
    """
    Copies the elements of a vtkMatrix4x4 into a numpy array.
    
    :@type matrix: vtk.vtkMatrix4x4
    :@param matrix: The matrix to be copied into an array.
    :@rtype: numpy.ndarray
    """
    m = np.ones((4,4))
    for i in range(4):
        for j in range(4):
            m[i,j] = matrix.GetElement(i,j)
    return m