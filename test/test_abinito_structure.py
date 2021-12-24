# -*- coding: utf-8 -*-
"""
Created on Sun Aug 22 21:22:33 2021

@author: Administrator
"""
import sys
import numpy as np
sys.path.append('../')

from abinitostudio.structure.abinito_structure import abinito_structrue

struc = abinito_structrue()
struc.set_spacegroup(230)
struc.build_structure(np.array([[1,0,0],[0,1,0],[0,0,1]]),
                          ['C','C'], 
                          np.array([[0,0,0],[0.5,0.5,0.0]])
                          )
print(struc.structure._lattice)
