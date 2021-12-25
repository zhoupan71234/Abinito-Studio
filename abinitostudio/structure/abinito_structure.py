# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 10:33:32 2021

@author: Administrator
"""

from pymatgen.core import Lattice, Structure
import numpy as np

class abinito_structrue():
    def __init__(self):  
        self.lattice = None
        self.species = None
        self.coords = None
        self.spacegroup = None
        self.use_spg = False


        
    def build_structure(self,
                        lattice,
                        species,
                        coords):
        if self.use_spg:
            self.structure = Structure.from_spacegroup(self.spacegroup, lattice, species, coords)
        else:
            self.structure = Structure(lattice, species, coords)
    def build_structure_from_file(self, filename):
        self.structure = Structure.from_file(filename)

        
    
    def set_spacegroup(self, spacegroup):
        self.spacegroup = spacegroup
        self.use_spg = True
        
            
    def lattice_from_parameters(self,
        a: float,
        b: float,
        c: float,
        alpha: float,
        beta: float,
        gamma: float
    ):
        lattice = Lattice.from_parameters(a=a, b=b, c=c, alpha=alpha, beta=beta, gamma=gamma)
        return lattice