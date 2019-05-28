# SMALViewer
PyQt5 app for viewing SMAL meshes

## Installation
1. Clone the repository with submodules and enter directory
   ```
   git clone --recurse-submodules https://github.com/benjiebob/SMALViewer
   cd CreaturesResult
    
2. Download texture map (from smal/dog_texture.pkl) and a version of SMAL 2017 converted to NumPy (smal_CVPR2017_np.pkl) from [my Google Drive](https://drive.google.com/open?id=1gPwA_tl1qrKiUkveE8PTsEOEMHtTw8br) and place under the smal folder

3. Visit the [SMAL](http://smal.is.tue.mpg.de/) website and download the smal_CVPR2017_data.pkl file. Be careful!

4. Install dependencies, particularly [PyTorch (with cuda support)](https://pytorch.org/), [PyQt5](https://pypi.org/project/PyQt5/) and [PyTorch Port of Neural Mesh Renderer](https://github.com/daniilidis-group/neural_renderer).

5. Test the python3 script
   ```
   python smal_viewer.py
   ```
