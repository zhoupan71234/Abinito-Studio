# -*- coding: utf-8 -*-
"""
Created on Mon Aug  9 16:51:34 2021

@author: Administrator
"""

from structure import *
import numpy as np

def prn_obj(obj):
    print ('\n'.join(['%s:%s' % item for item in obj.__dict__.items()]))

struc = structure_plot()
struc.adjust_cell(True, (1, 1, 1), 0.02, (1, 1, 1))
struc.read_poscar('POSCAR')
#print(struc.poscar.get_scaled_positions(wrap=True))

struc.plot_str()
struc.picker_atoms()
#struc.animate_atoms()


