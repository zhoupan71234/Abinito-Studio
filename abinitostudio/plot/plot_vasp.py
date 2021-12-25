# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 09:26:02 2021

@author: zhoup
"""

from abinitostudio.io.vasp_io import readCHGCAR
import numpy as np

def plot_CHGCAR(scene):
    contant, latt, chg = readCHGCAR('examples/CHGCAR')
        ############################################################
    # Draw the cell box
    ############################################################
    # Draw the unit cell:
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
        cell_box = scene.mlab.plot3d(Cxyz[0], Cxyz[1], Cxyz[2],
                                     tube_radius=cell_linewidth,
                                     color=cell_linecolor,
                                     name='CellBox'
                                     )
        cell_box.mlab_source.dataset.lines = np.array(conn)
    

    scene.mlab.clf()
    source = scene.mlab.pipeline.scalar_field(chg)
    
    min = chg.min()
    max = chg.max()
    vol = scene.mlab.pipeline.volume(source, vmin=min + 0.65 * (max - min),
                                   vmax=min + 0.9 * (max - min))

   # scene.mlab.view(132, 54, 45, [21, 20, 21.5])
    
    