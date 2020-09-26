import os
#https://pyrender.readthedocs.io/en/latest/examples/offscreen.html
# fix for windows from https://github.com/mmatl/pyrender/issues/117
# edit C:\Users\bjb10042\.conda\envs\bjb_env\Lib\site-packages\pyrender
# os.environ['PYOPENGL_PLATFORM'] = 'osmesa'
import torch
from torchvision.utils import make_grid
import numpy as np
import pyrender
import trimesh

class Renderer:
    """
    Renderer used for visualizing the SMPL model
    Code adapted from https://github.com/vchoutas/smplify-x
    """
    def __init__(self, img_res=224):
        self.renderer = pyrender.OffscreenRenderer(viewport_width=img_res,
                                       viewport_height=img_res,
                                       point_size=1.0)
        self.focal_length = 5000
        self.camera_center = [img_res // 2, img_res // 2]

    def __call__(self, vertices, faces):
        material = pyrender.MetallicRoughnessMaterial(
            metallicFactor=0.2,
            alphaMode='OPAQUE',
            baseColorFactor=(0.8, 0.3, 0.3, 1.0))

        camera_translation = np.array([0.0, 0.0, 50.0])

        mesh = trimesh.Trimesh(vertices[0], faces[0], process=False)
        # rot = trimesh.transformations.rotation_matrix(
        #     np.radians(180), [1, 0, 0])
        # mesh.apply_transform(rot)
        mesh = pyrender.Mesh.from_trimesh(mesh, material=material)

        scene = pyrender.Scene(ambient_light=(0.5, 0.5, 0.5))
        scene.add(mesh, 'mesh')

        camera_pose = np.eye(4)
        camera_pose[:3, 3] = camera_translation
        camera = pyrender.IntrinsicsCamera(fx=self.focal_length, fy=self.focal_length,
                                           cx=self.camera_center[0], cy=self.camera_center[1])
        scene.add(camera, pose=camera_pose)


        light = pyrender.DirectionalLight(color=[1.0, 1.0, 1.0], intensity=1)
        light_pose = np.eye(4)

        light_pose[:3, 3] = np.array([0, -1, 1])
        scene.add(light, pose=light_pose)

        light_pose[:3, 3] = np.array([0, 1, 1])
        scene.add(light, pose=light_pose)

        light_pose[:3, 3] = np.array([1, 1, 2])
        scene.add(light, pose=light_pose)

        color, rend_depth = self.renderer.render(scene, flags=pyrender.RenderFlags.RGBA)
        color = color.astype(np.float32) / 255.0
        return torch.from_numpy(color).float().unsqueeze(0)