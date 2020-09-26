# Data structures and functions for rendering
import torch
import torch.nn.functional as F
from scipy.io  import loadmat
import numpy as np

from pytorch3d.structures import Meshes
from pytorch3d.renderer import (
    OpenGLPerspectiveCameras, look_at_view_transform, look_at_rotation, 
    RasterizationSettings, MeshRenderer, MeshRasterizer, BlendParams,
    PointLights, SoftPhongShader, SoftSilhouetteShader
)
from pytorch3d.io import load_objs_as_meshes

class Renderer(torch.nn.Module):
    def __init__(self, image_size):
        super(Renderer, self).__init__()

        self.image_size = image_size
        self.dog_obj = load_objs_as_meshes(['data/dog_B/dog_B/dog_B_tpose.obj'])

        raster_settings = RasterizationSettings(
            image_size=self.image_size, 
            blur_radius=0.0, 
            faces_per_pixel=1, 
            bin_size=None
        )

        R, T = look_at_view_transform(2.7, 0, 0) 
        cameras = OpenGLPerspectiveCameras(device=R.device, R=R, T=T)
        lights = PointLights(device=R.device, location=[[0.0, 1.0, 0.0]])

        self.renderer = MeshRenderer(
            rasterizer=MeshRasterizer(
                cameras=cameras, 
                raster_settings=raster_settings
            ),
            shader=SoftPhongShader(
                device=R.device, 
                cameras=cameras,
                lights=lights
            )
        )

    def forward(self, vertices, faces):
        mesh = Meshes(verts=vertices, faces=faces, textures=self.dog_obj.textures)
        images = self.renderer(mesh)
        return images