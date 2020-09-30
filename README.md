# SMAL Viewer
PyQt5 app for viewing SMAL meshes

<img src="docs/smal_viewer.gif">

## Installation
1. Clone the repository and enter directory
   ```
   git clone https://github.com/benjiebob/SMALViewer
   cd SMALViewer
   ```

2. Clone the [SMALST](https://github.com/silviazuffi/smalst) project website in order to access the latest version of the SMAL deformable animal model. You should copy all of [these files](https://github.com/silviazuffi/smalst/tree/master/smpl_models) underneath a SMALViewer/data directory. 

   Windows tip: If you are a Windows user, you can use these files but you'll need to edit the line endings. Try the following Powershell commands, shown here on one example:
     ```
     $path="my_smpl_00781_4_all_template_w_tex_uv_001.pkl"
     (Get-Content $path -Raw).Replace("`r`n","`n") | Set-Content $path -Force
     ```

   For more information, check out the StackOverflow answer [here](https://stackoverflow.com/questions/19127741/replace-crlf-using-powershell)


3. Install dependencies, particularly [PyTorch](https://pytorch.org/), [PyQt5](https://pypi.org/project/PyQt5/), [Pyrender](https://github.com/mmatl/pyrender) and [nibabel](https://github.com/nipy/nibabel).

   Tips for debugging offscreen render: If you are a Linux user and have trouble with the Pyrender's OffscreenRenderer, I recommend following the steps to install OSMesa [here](https://pyrender.readthedocs.io/en/latest/examples/offscreen.html) including the need to add the following to the top of pyrenderer.py

   ```
   os.environ['PYOPENGL_PLATFORM'] = 'osmesa'.
   ```

   If you are a Windows user and you experience issues with OffscreenRenderer, you can fix by following the advice [here](https://github.com/mmatl/pyrender/issues/117). A quick fix is to edit the function "make_current" in pyrender/platforms/pyglet_platform.py, L53 (wherever it's installed for you) to:
  
     ```
     def make_uncurrent(self):
         try:
             import pyglet.gl.xlib
             pyglet.gl.xlib.glx.glXMakeContextCurrent(self._window.context.x_display, 0, 0, None)
         except:
             pass
     ```

4. Download [SMPL](https://smpl.is.tue.mpg.de/) and create a smpl_webuser directory underneath SMALViewer/smal_model

5. Test the python3 script
   ```
   python smal_viewer.py
   ```
## Differentiable Rendering

For many research applications, it is useful to be able to propagate gradients from 2D losses (e.g. silhouette/perceptual) back through the rendering process. For this, one should use a differentiable render such as [PyTorch3D](https://github.com/facebookresearch/pytorch3d) or [Neural Mesh Renderer](https://github.com/daniilidis-group/neural_renderer). Although not usful for this simple demo app, I have included a script p3d_renderer.py which shows how one can achieve differentiable rendering of the SMAL mesh with PyTorch3D. You can flip between the two rendering methods by selecting between the two imports at the top of pyqt_viewer.py:

```
from pyrenderer import Renderer
# from p3d_renderer import Renderer
```

   Please note that the speed of PyTorch3D compared to Pyrender is significantly slower so you'll probably experience some lag with this option.

   For completeness, I've also shown how to apply a texture map to the SMAL mesh with p3d_renderer (again useful for perceptual losses). To do this, you will need to download an example SMAL texture map. Do this by creating an account for the [SMALR page](http://smalr.is.tue.mpg.de/downloads), choose CVPR Downloads and download (for example) the Dog B zip file. Extract this underneath ./data.

## Acknowledgements
This work was completed in relation to the paper [Creatures Great and SMAL: Recovering the shape and motion of animals from video](https://arxiv.org/abs/1811.05804):
```
@inproceedings{biggs2018creatures,
  title={{C}reatures great and {SMAL}: {R}ecovering the shape and motion of animals from video},
  author={Biggs, Benjamin and Roddick, Thomas and Fitzgibbon, Andrew and Cipolla, Roberto},
  booktitle={ACCV},
  year={2018}
}
```

and more recently [Who Left the Dogs Out? 3D Animal Reconstruction with Expectation Maximization in the Loop](https://arxiv.org/abs/2007.11110):
```
@inproceedings{biggs2020wldo,
  title={{W}ho left the dogs out?: {3D} animal reconstruction with expectation maximization in the loop},
  author={Biggs, Benjamin and Boyne, Oliver and Charles, James and Fitzgibbon, Andrew and Cipolla, Roberto},
  booktitle={ECCV},
  year={2020}
}
```

Please also acknowledge the original authors of the SMAL animal model:
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
