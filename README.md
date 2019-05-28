# SMAL Viewer
PyQt5 app for viewing SMAL meshes

<img src="docs/smal_viewer.gif" width="50%" height="50%">

## Installation
1. Clone the repository with submodules and enter directory
   ```
   git clone --recurse-submodules https://github.com/benjiebob/SMALViewer
   cd SMALViewer
    
2. Download texture map (from smal/dog_texture.pkl) and a version of SMAL 2017 converted to NumPy (smal_CVPR2017_np.pkl) from [my Google Drive](https://drive.google.com/open?id=1gPwA_tl1qrKiUkveE8PTsEOEMHtTw8br) and place under the smal folder

3. Visit the [SMAL](http://smal.is.tue.mpg.de/) website and download the smal_CVPR2017_data.pkl file. Be careful to obtain the correct data file or you'll find the toy reconstructions look strange!

4. Install dependencies, particularly [PyTorch (with cuda support)](https://pytorch.org/), [PyQt5](https://pypi.org/project/PyQt5/), [PyTorch Port of Neural Mesh Renderer](https://github.com/daniilidis-group/neural_renderer) and [nibabel](https://github.com/nipy/nibabel).

5. Test the python3 script
   ```
   python smal_viewer.py
   ```

## Acknoledgements
This work was completed in relation to the following paper:
```
@inproceedings{biggs2018creatures,
  title={{C}reatures great and {SMAL}: {R}ecovering the shape and motion of animals from video},
  author={Biggs, Benjamin and Roddick, Thomas and Fitzgibbon, Andrew and Cipolla, Roberto},
  booktitle={ACCV},
  year={2018}
}
```
   
However, please do acknowledge the original authors of the SMAL animal model:
```
@inproceedings{Zuffi:CVPR:2017,
  title = {{3D} Menagerie: Modeling the {3D} Shape and Pose of Animals},
  author = {Zuffi, Silvia and Kanazawa, Angjoo and Jacobs, David and Black, Michael J.},
  booktitle = {IEEE Conf. on Computer Vision and Pattern Recognition (CVPR)},
  month = jul,
  year = {2017},
  month_numeric = {7}
}
```
