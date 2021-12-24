# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 09:45:43 2021

@author: zhoup
"""
import sys
import numpy as np
sys.path.append('../')
from mayavi import mlab

from abinitostudio.io.vasp_io import readCHGCAR

mlab.figure(1, bgcolor=(1, 1, 1), size=(350, 350))
mlab.clf()

# # The position of the atoms
# atoms_x = np.array([2.9, 2.9, 3.8]) * 40 / 5.5
# atoms_y = np.array([3.0, 3.0, 3.0]) * 40 / 5.5
# atoms_z = np.array([3.8, 2.9, 2.7]) * 40 / 5.5

# O = mlab.points3d(atoms_x[1:-1], atoms_y[1:-1], atoms_z[1:-1],
#                   scale_factor=3,
#                   resolution=20,
#                   color=(1, 0, 0),
#                   scale_mode='none')

# H1 = mlab.points3d(atoms_x[:1], atoms_y[:1], atoms_z[:1],
#                    scale_factor=2,
#                    resolution=20,
#                    color=(1, 1, 1),
#                    scale_mode='none')

# H2 = mlab.points3d(atoms_x[-1:], atoms_y[-1:], atoms_z[-1:],
#                    scale_factor=2,
#                    resolution=20,
#                    color=(1, 1, 1),
#                    scale_mode='none')

# # The bounds between the atoms, we use the scalar information to give
# # color
# mlab.plot3d(atoms_x, atoms_y, atoms_z, [1, 2, 1],
#             tube_radius=0.4, colormap='Reds')

contant, ucell, data = readCHGCAR('../examples/CHGCAR')
print(np.shape(data))
print(ucell)
plot_way = 'cut'
#sys.exit()
    ############################################################
    # Draw the cell box
    ############################################################
# Draw the unit cell:
repeat = (1,1,1)
showcell = True
singleCell = True
cell_linewidth = 0.02
cell_linecolor = (0, 0, 0)
if showcell:
    if singleCell:
        Nx, Ny, Nz = (1, 1, 1)
    else:
        Nx, Ny, Nz = repeat
    fx = range(Nx + 1)
    fy = range(Ny + 1)
    fz = range(Nz + 1)
    Dxyz = np.array(np.meshgrid(fx, fy, fz, indexing='ij'))
    Cxyz = np.array(np.tensordot(ucell, Dxyz, axes=(0, 0)))
    Dxyz = Dxyz.reshape((3, -1))
    Cxyz = Cxyz.reshape((3, -1))

    conn = []
    cpts = Dxyz.shape[1]
    for ii in range(cpts):
        for jj in range(ii):
            L = Dxyz[:, ii] - Dxyz[:, jj]
            # only connect the nearest cell boundary point
            if list(L).count(0) == 2:
                conn.append((ii, jj))
    cell_box = mlab.plot3d(Cxyz[0], Cxyz[1], Cxyz[2],
                                 tube_radius=cell_linewidth,
                                 color=cell_linecolor,
                                 name='CellBox'
                                 )
    cell_box.mlab_source.dataset.lines = np.array(conn)
x,y,z=np.mgrid[0:3.4:48j,0:3.4:48j,0:22:300j]
if plot_way == 'contour':
    mlab.contour3d(x,y,z,data,contours=3, transparent=True)

if plot_way == 'vol':
    source = mlab.pipeline.scalar_field(x,y,z,data)
    vol = mlab.pipeline.volume(source)
    print(source)
    min = data.min()
    max = data.max()
if plot_way == 'cut':
    src = mlab.pipeline.scalar_field(x,y,z,data)
    mlab.pipeline.iso_surface(src, contours=[data.min()+0.1*data.ptp(), ], opacity=0.1)
    mlab.pipeline.iso_surface(src, contours=[data.max()-0.1*data.ptp(), ],)
    mlab.pipeline.image_plane_widget(src,
                            plane_orientation='z_axes',
                            slice_index=150,
                        )
print(mlab.view())


#mlab.view(132, 54, 45, [21, 20, 21.5])

mlab.show()
sys.exit()