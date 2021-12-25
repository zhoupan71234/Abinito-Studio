# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 11:07:44 2021

@author: zhoup
"""
from mayavi import mlab


def plot_magnetic_field(u, v, w):
    # scene.mlab.quiver3d(u, v, w)
    # scene.mlab.outline()
    src = mlab.pipeline.vector_field(u, v, w)
    mlab.pipeline.vectors(src, mask_points=20, scale_factor=3.)
    
#    scene.mlab.pipeline.vector_cut_plane(src, mask_points=2, scale_factor=3)
    
import numpy as np
x, y, z = np.mgrid[0:1:20j, 0:1:20j, 0:1:20j]

u =    np.sin(np.pi*x) * np.cos(np.pi*z)
v = -2*np.sin(np.pi*y) * np.cos(2*np.pi*z)
w = np.cos(np.pi*x)*np.sin(np.pi*z) + np.cos(np.pi*y)*np.sin(2*np.pi*z)

plot_magnetic_field(u, v, w)