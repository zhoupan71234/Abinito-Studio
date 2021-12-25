# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 09:37:39 2020

@author: Administrator
"""

################################################################################
# the chemical symbol of elements in the periodic table, extracted from VESTA
# configuration file.
pt_atomic_name = [
    "H", "D", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na", "Mg", "Al",
    "Si", "P", "S", "Cl", "Ar", "K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co",
    "Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", "Kr", "Rb", "Sr", "Y", "Zr",
    "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb", "Te", "I",
    "Xe", "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy",
    "Ho", "Er", "Tm", "Yb", "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au",
    "Hg", "Tl", "Pb", "Bi", "Po", "At", "Rn", "Fr", "Ra", "Ac", "Th", "Pa", "U",
    "Np", "Pu", "Am", "XX"
]
# the atomic number of elements in the periodic table, extracted from VESTA
# configuration file.
pt_atomic_number = [
    1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
    20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37,
    38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55,
    56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73,
    74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91,
    92, 93, 94, 95, 96,
]
# the radius of elements in the periodic table, extracted from VESTA
# configuration file.
pt_atomic_radius = [
    0.46, 0.46, 1.22, 1.57, 1.12, 0.81, 0.77, 0.74, 0.74, 0.72, 1.60, 1.91, 1.60,
    1.43, 1.18, 1.10, 1.04, 0.99, 1.92, 2.35, 1.97, 1.64, 1.47, 1.35, 1.29, 1.37,
    1.26, 1.25, 1.25, 1.28, 1.37, 1.53, 1.22, 1.21, 1.04, 1.14, 1.98, 2.50, 2.15,
    1.82, 1.60, 1.47, 1.40, 1.35, 1.34, 1.34, 1.37, 1.44, 1.52, 1.67, 1.58, 1.41,
    1.37, 1.33, 2.18, 2.72, 2.24, 1.88, 1.82, 1.82, 1.82, 1.81, 1.81, 2.06, 1.79,
    1.77, 1.77, 1.76, 1.75, 1.00, 1.94, 1.72, 1.59, 1.47, 1.41, 1.37, 1.35, 1.36,
    1.39, 1.44, 1.55, 1.71, 1.75, 1.82, 1.77, 0.62, 0.80, 1.00, 2.35, 2.03, 1.80,
    1.63, 1.56, 1.56, 1.64, 1.73, 0.80
]
# the RGB-color for elements in the periodic table, extracted from VESTA
# configuration file.
pt_atomic_color = [
    (1.00000, 0.80000, 0.80000), (0.80000, 0.80000, 1.00000),
    (0.98907, 0.91312, 0.81091), (0.52731, 0.87953, 0.45670),
    (0.37147, 0.84590, 0.48292), (0.12490, 0.63612, 0.05948),
    (0.50430, 0.28659, 0.16236), (0.69139, 0.72934, 0.90280),
    (0.99997, 0.01328, 0.00000), (0.69139, 0.72934, 0.90280),
    (0.99954, 0.21788, 0.71035), (0.97955, 0.86618, 0.23787),
    (0.98773, 0.48452, 0.08470), (0.50718, 0.70056, 0.84062),
    (0.10596, 0.23226, 0.98096), (0.75557, 0.61256, 0.76425),
    (1.00000, 0.98071, 0.00000), (0.19583, 0.98828, 0.01167),
    (0.81349, 0.99731, 0.77075), (0.63255, 0.13281, 0.96858),
    (0.35642, 0.58863, 0.74498), (0.71209, 0.38930, 0.67279),
    (0.47237, 0.79393, 1.00000), (0.90000, 0.10000, 0.00000),
    (0.00000, 0.00000, 0.62000), (0.66148, 0.03412, 0.62036),
    (0.71051, 0.44662, 0.00136), (0.00000, 0.00000, 0.68666),
    (0.72032, 0.73631, 0.74339), (0.13390, 0.28022, 0.86606),
    (0.56123, 0.56445, 0.50799), (0.62292, 0.89293, 0.45486),
    (0.49557, 0.43499, 0.65193), (0.45814, 0.81694, 0.34249),
    (0.60420, 0.93874, 0.06122), (0.49645, 0.19333, 0.01076),
    (0.98102, 0.75805, 0.95413), (1.00000, 0.00000, 0.60000),
    (0.00000, 1.00000, 0.15259), (0.40259, 0.59739, 0.55813),
    (0.00000, 1.00000, 0.00000), (0.29992, 0.70007, 0.46459),
    (0.70584, 0.52602, 0.68925), (0.80574, 0.68699, 0.79478),
    (0.81184, 0.72113, 0.68089), (0.80748, 0.82205, 0.67068),
    (0.75978, 0.76818, 0.72454), (0.72032, 0.73631, 0.74339),
    (0.95145, 0.12102, 0.86354), (0.84378, 0.50401, 0.73483),
    (0.60764, 0.56052, 0.72926), (0.84627, 0.51498, 0.31315),
    (0.67958, 0.63586, 0.32038), (0.55914, 0.12200, 0.54453),
    (0.60662, 0.63218, 0.97305), (0.05872, 0.99922, 0.72578),
    (0.11835, 0.93959, 0.17565), (0.35340, 0.77057, 0.28737),
    (0.82055, 0.99071, 0.02374), (0.99130, 0.88559, 0.02315),
    (0.98701, 0.55560, 0.02744), (0.00000, 0.00000, 0.96000),
    (0.99042, 0.02403, 0.49195), (0.98367, 0.03078, 0.83615),
    (0.75325, 0.01445, 1.00000), (0.44315, 0.01663, 0.99782),
    (0.19390, 0.02374, 0.99071), (0.02837, 0.25876, 0.98608),
    (0.28688, 0.45071, 0.23043), (0.00000, 0.00000, 0.88000),
    (0.15323, 0.99165, 0.95836), (0.15097, 0.99391, 0.71032),
    (0.70704, 0.70552, 0.35090), (0.71952, 0.60694, 0.33841),
    (0.55616, 0.54257, 0.50178), (0.70294, 0.69401, 0.55789),
    (0.78703, 0.69512, 0.47379), (0.78975, 0.81033, 0.45049),
    (0.79997, 0.77511, 0.75068), (0.99628, 0.70149, 0.22106),
    (0.82940, 0.72125, 0.79823), (0.58798, 0.53854, 0.42649),
    (0.32386, 0.32592, 0.35729), (0.82428, 0.18732, 0.97211),
    (0.00000, 0.00000, 1.00000), (0.00000, 0.00000, 1.00000),
    (1.00000, 1.00000, 0.00000), (0.00000, 0.00000, 0.00000),
    (0.42959, 0.66659, 0.34786), (0.39344, 0.62101, 0.45034),
    (0.14893, 0.99596, 0.47106), (0.16101, 0.98387, 0.20855),
    (0.47774, 0.63362, 0.66714), (0.30000, 0.30000, 0.30000),
    (0.30000, 0.30000, 0.30000), (0.30000, 0.30000, 0.30000),
    (0.30000, 0.30000, 0.30000)
]
# The bond length extracted from VESTA configuration file.
pt_max_bond = {
    ("Ac", "O"): 2.73260, ("Ac", "F"): 2.58646, ("Ac", "Cl"): 3.08646, ("Ac", "Br"): 3.22726,
    ("Ag", "O"): 2.81139, ("Ag", "S"): 3.08839, ("Ag", "F"): 2.76939, ("Ag", "Cl"): 3.05939,
    ("Ag", "Br"): 2.37642, ("Ag", "I"): 2.53642, ("Ag", "Se"): 2.41642, ("Ag", "Te"): 2.66642,
    ("Ag", "N"): 2.00642, ("Ag", "P"): 2.37642, ("Ag", "As"): 2.45642, ("Ag", "H"): 1.65642,
    ("Al", "O"): 2.10740, ("Al", "S"): 2.66646, ("Al", "Se"): 2.72646, ("Al", "Te"): 2.93646,
    ("Al", "F"): 2.00146, ("Al", "Cl"): 2.48846, ("Al", "Br"): 2.65646, ("Al", "I"): 2.86646,
    ("Al", "N"): 2.24646, ("Al", "P"): 2.69646, ("Al", "As"): 2.75646, ("Al", "H"): 1.90646,
    ("Am", "O"): 2.71649, ("Am", "F"): 2.61945, ("Am", "Cl"): 3.08945, ("Am", "Br"): 3.22944,
    ("As", "S"): 2.84649, ("As", "Se"): 2.98649, ("As", "O"): 2.24546, ("As", "Te"): 3.10646,
    ("As", "F"): 2.15646, ("As", "Cl"): 2.61646, ("As", "Br"): 2.80646, ("As", "I"): 3.03646,
    ("As", "C"): 2.38646, ("Au", "Cl"): 2.88295, ("Au", "I"): 3.21295, ("Au", "O"): 2.34646,
    ("Au", "S"): 2.83260, ("Au", "F"): 2.34646, ("Au", "Br"): 2.77646, ("Au", "N"): 2.38260,
    ("Au", "Se"): 2.22998, ("Au", "Te"): 2.45998, ("Au", "P"): 2.18998, ("Au", "As"): 2.26998,
    ("Au", "H"): 1.41998, ("B", "O"): 1.82746, ("B", "S"): 2.27646, ("B", "Se"): 2.40646,
    ("B", "Te"): 2.65646, ("B", "F"): 1.76646, ("B", "Cl"): 2.19646, ("B", "Br"): 2.33646,
    ("B", "I"): 2.55646, ("B", "N"): 1.93846, ("B", "P"): 2.37646, ("B", "As"): 2.42646,
    ("B", "H"): 1.59646, ("B", "B"): 1.85846, ("Ba", "O"): 3.14795, ("Ba", "S"): 3.66195,
    ("Ba", "Se"): 3.74295, ("Ba", "Te"): 3.94295, ("Ba", "F"): 3.05095, ("Ba", "Cl"): 3.55295,
    ("Ba", "Br"): 3.74295, ("Ba", "I"): 3.99295, ("Ba", "N"): 3.33295, ("Ba", "P"): 3.48295,
    ("Ba", "As"): 3.69000, ("Ba", "H"): 3.08295, ("Be", "O"): 1.98749, ("Be", "S"): 2.43649,
    ("Be", "Se"): 2.57649, ("Be", "Te"): 2.81649, ("Be", "F"): 1.88749, ("Be", "Cl"): 2.36649,
    ("Be", "Br"): 2.50649, ("Be", "I"): 2.70649, ("Be", "N"): 2.10649, ("Be", "P"): 2.55649,
    ("Be", "As"): 2.60649, ("Be", "H"): 1.71649, ("Bi", "O"): 2.66080, ("Bi", "S"): 3.13291,
    ("Bi", "Se"): 3.24329, ("Bi", "F"): 2.55291, ("Bi", "Cl"): 3.04291, ("Bi", "Br"): 3.17993,
    ("Bi", "I"): 3.38291, ("Bi", "N"): 2.56329, ("Bi", "Te"): 3.02642, ("Bi", "P"): 2.78642,
    ("Bi", "As"): 2.87642, ("Bi", "H"): 2.12642, ("Br", "O"): 2.35646, ("Br", "F"): 2.20646,
    ("Br", "Cl"): 2.33296, ("C", "O"): 1.97249, ("C", "Cl"): 2.11002, ("C", "C"): 1.89002,
    ("C", "S"): 2.15002, ("C", "F"): 1.76002, ("C", "Br"): 2.26002, ("C", "N"): 1.79202,
    ("C", "Se"): 2.01998, ("C", "I"): 2.16998, ("C", "Te"): 2.25998, ("C", "P"): 1.93998,
    ("C", "H"): 1.20000, ("Ca", "O"): 2.83062, ("Ca", "S"): 3.31295, ("Ca", "Se"): 3.42295,
    ("Ca", "Te"): 3.62295, ("Ca", "F"): 2.70495, ("Ca", "Cl"): 3.23295, ("Ca", "Br"): 3.36995,
    ("Ca", "I"): 3.58295, ("Ca", "N"): 3.00295, ("Ca", "P"): 3.41295, ("Ca", "As"): 3.48295,
    ("Ca", "H"): 2.69295, ("Cd", "O"): 2.76695, ("Cd", "S"): 3.16695, ("Cd", "Se"): 3.26295,
    ("Cd", "Te"): 3.45295, ("Cd", "F"): 2.67395, ("Cd", "Cl"): 3.09295, ("Cd", "Br"): 3.21295,
    ("Cd", "I"): 3.46295, ("Cd", "N"): 2.82295, ("Cd", "P"): 3.20295, ("Cd", "As"): 3.29295,
    ("Cd", "H"): 2.52295, ("Ce", "O"): 2.86393, ("Ce", "S"): 3.36293, ("Ce", "F"): 2.75452,
    ("Ce", "Cl"): 3.25293, ("Ce", "Br"): 3.40452, ("Ce", "I"): 3.62452, ("Ce", "N"): 2.78549,
    ("Ce", "Se"): 3.04644, ("Ce", "Te"): 3.22644, ("Ce", "P"): 3.00644, ("Ce", "As"): 3.08644,
    ("Ce", "H"): 2.34644, ("Cl", "O"): 2.16646, ("Cl", "F"): 2.14646, ("Cl", "Cl"): 2.14296,
    ("Co", "H"): 1.92780, ("Co", "O"): 2.40493, ("Co", "S"): 2.65293, ("Co", "F"): 2.35293,
    ("Co", "Cl"): 2.74593, ("Co", "N"): 2.36293, ("Co", "C"): 2.19691, ("Co", "Br"): 2.33642,
    ("Co", "I"): 2.52878, ("Co", "Se"): 2.39642, ("Co", "Te"): 2.61642, ("Co", "P"): 2.36642,
    ("Co", "As"): 2.43642, ("Cr", "O"): 2.44293, ("Cr", "F"): 2.45293, ("Cr", "Cl"): 2.80293,
    ("Cr", "Br"): 2.97293, ("Cr", "I"): 3.19293, ("Cr", "N"): 2.51520, ("Cr", "S"): 2.72491,
    ("Cr", "Se"): 2.44642, ("Cr", "Te"): 2.67642, ("Cr", "P"): 2.42642, ("Cr", "As"): 2.49642,
    ("Cr", "H"): 1.67642, ("Cs", "O"): 3.53642, ("Cs", "S"): 4.24942, ("Cs", "Se"): 4.21655,
    ("Cs", "Te"): 4.46310, ("Cs", "F"): 3.49942, ("Cs", "Cl"): 3.91042, ("Cs", "Br"): 4.06942,
    ("Cs", "I"): 4.40942, ("Cs", "N"): 3.94942, ("Cs", "P"): 3.64194, ("Cs", "As"): 4.15942,
    ("Cs", "H"): 3.55942, ("Cu", "O"): 2.47295, ("Cu", "S"): 2.76095, ("Cu", "Se"): 2.76295,
    ("Cu", "F"): 2.46295, ("Cu", "Cl"): 2.75295, ("Cu", "Br"): 2.89295, ("Cu", "I"): 3.01795,
    ("Cu", "N"): 2.49295, ("Cu", "P"): 2.65649, ("Cu", "As"): 2.71895, ("Cu", "C"): 2.32649,
    ("Cu", "Te"): 2.87649, ("Cu", "H"): 1.81649, ("Dy", "O"): 2.65651, ("Dy", "F"): 2.52944,
    ("Dy", "Cl"): 3.01945, ("Dy", "Br"): 3.16945, ("Dy", "I"): 3.39945, ("Dy", "S"): 2.82300,
    ("Dy", "Se"): 2.81000, ("Dy", "Te"): 3.22000, ("Dy", "N"): 2.38000, ("Dy", "P"): 2.77000,
    ("Dy", "As"): 3.14000, ("Dy", "H"): 2.09000, ("Er", "O"): 2.63651, ("Er", "S"): 3.27651,
    ("Er", "Se"): 3.18649, ("Er", "F"): 2.51049, ("Er", "Cl"): 2.99944, ("Er", "Br"): 3.14945,
    ("Er", "I"): 3.38945, ("Er", "Te"): 3.22000, ("Er", "N"): 2.36000, ("Er", "P"): 2.75000,
    ("Er", "As"): 3.18000, ("Er", "H"): 2.06000, ("Eu", "O"): 2.94249, ("Eu", "S"): 3.37949,
    ("Eu", "F"): 2.83549, ("Eu", "Cl"): 3.32549, ("Eu", "Br"): 3.46549, ("Eu", "I"): 3.69549,
    ("Eu", "N"): 2.95549, ("Eu", "Se"): 2.89898, ("Eu", "Te"): 3.08898, ("Eu", "P"): 2.85898,
    ("Eu", "As"): 2.93898, ("Eu", "H"): 2.18898, ("Fe", "O"): 2.44693, ("Fe", "S"): 2.83793,
    ("Fe", "F"): 2.36293, ("Fe", "Cl"): 2.86293, ("Fe", "Br"): 2.89520, ("Fe", "I"): 3.15520,
    ("Fe", "N"): 2.48193, ("Fe", "C"): 2.25191, ("Fe", "Se"): 2.43642, ("Fe", "Te"): 2.68642,
    ("Fe", "P"): 2.42642, ("Fe", "As"): 2.50642, ("Fe", "H"): 1.68642, ("Ga", "Se"): 3.41295,
    ("Ga", "O"): 2.18646, ("Ga", "S"): 2.61946, ("Ga", "F"): 2.14646, ("Ga", "Cl"): 2.52646,
    ("Ga", "Br"): 2.64260, ("Ga", "I"): 2.91646, ("Ga", "Te"): 2.58998, ("Ga", "N"): 1.96000,
    ("Ga", "P"): 2.46998, ("Ga", "As"): 2.38998, ("Ga", "H"): 1.55998, ("Gd", "O"): 2.76651,
    ("Gd", "F"): 3.15651, ("Gd", "S"): 3.13649, ("Gd", "Cl"): 3.06349, ("Gd", "Br"): 3.19945,
    ("Gd", "I"): 3.41945, ("Gd", "Se"): 2.85000, ("Gd", "Te"): 3.24000, ("Gd", "N"): 2.42000,
    ("Gd", "P"): 2.81000, ("Gd", "As"): 3.18000, ("Gd", "H"): 2.13000, ("Ge", "O"): 2.09802,
    ("Ge", "S"): 2.56702, ("Ge", "Se"): 2.70002, ("Ge", "F"): 2.01002, ("Ge", "Cl"): 2.49002,
    ("Ge", "Br"): 2.34998, ("Ge", "I"): 2.54998, ("Ge", "Te"): 2.60998, ("Ge", "N"): 1.92998,
    ("Ge", "P"): 2.36998, ("Ge", "As"): 2.47998, ("Ge", "H"): 1.59998, ("Ge", "Ge"): 2.60000,
    ("O", "H"): 1.20000, ("H", "O"): 2.10000, ("H", "F"): 1.10000, ("H", "Cl"): 1.50000,
    ("H", "N"): 1.20000, ("O", "D"): 1.20000, ("D", "O"): 2.10000, ("D", "F"): 1.10000,
    ("D", "Cl"): 1.50000, ("D", "N"): 1.20000, ("Hf", "F"): 3.18291, ("Hf", "O"): 2.37946,
    ("Hf", "Cl"): 2.75646, ("Hf", "Br"): 2.62642, ("Hf", "S"): 2.64642, ("Hf", "Se"): 2.67642,
    ("Hf", "Te"): 2.87642, ("Hf", "I"): 2.83642, ("Hf", "N"): 2.24642, ("Hf", "P"): 2.63642,
    ("Hf", "As"): 2.71642, ("Hf", "H"): 1.93642, ("Hg", "O"): 2.86939, ("Hg", "F"): 2.88293,
    ("Hg", "Cl"): 3.24939, ("Hg", "S"): 3.42093, ("Hg", "Br"): 3.09293, ("Hg", "I"): 3.33293,
    ("Hg", "Se"): 2.82642, ("Hg", "Te"): 2.76642, ("Hg", "N"): 2.17642, ("Hg", "P"): 2.57642,
    ("Hg", "As"): 2.65642, ("Hg", "H"): 1.86642, ("Hg", "Hg"): 3.19520, ("Ho", "O"): 2.67047,
    ("Ho", "S"): 3.13547, ("Ho", "F"): 2.56159, ("Ho", "Cl"): 3.05159, ("Ho", "Br"): 3.20159,
    ("Ho", "I"): 3.44159, ("Ho", "Se"): 2.84898, ("Ho", "Te"): 3.03898, ("Ho", "N"): 2.41898,
    ("Ho", "P"): 2.79898, ("Ho", "As"): 2.87898, ("Ho", "H"): 2.11898, ("I", "I"): 2.40000,
    ("I", "F"): 3.18295, ("I", "Cl"): 3.33295, ("I", "O"): 2.47646, ("In", "Cl"): 3.52939,
    ("In", "O"): 2.46491, ("In", "S"): 2.93291, ("In", "F"): 2.35491, ("In", "Br"): 3.05329,
    ("In", "I"): 3.19291, ("In", "Co"): 3.13629, ("In", "Mn"): 3.14729, ("In", "Se"): 2.62642,
    ("In", "Te"): 2.84642, ("In", "N"): 2.18642, ("In", "P"): 2.68642, ("In", "As"): 2.66642,
    ("In", "H"): 1.87642, ("Ir", "O"): 2.27746, ("Ir", "F"): 2.15002, ("Ir", "Cl"): 2.56746,
    ("Ir", "S"): 2.42998, ("Ir", "Se"): 2.55998, ("Ir", "Te"): 2.75998, ("Ir", "Br"): 2.49998,
    ("Ir", "I"): 2.70998, ("Ir", "N"): 2.10998, ("Ir", "P"): 2.50998, ("Ir", "As"): 2.58998,
    ("Ir", "H"): 1.80998, ("K", "O"): 3.25142, ("K", "S"): 3.79285, ("K", "Se"): 4.00186,
    ("K", "Te"): 4.23284, ("K", "F"): 3.11142, ("K", "Cl"): 3.65976, ("K", "Br"): 3.85130,
    ("K", "I"): 4.11717, ("K", "N"): 3.41942, ("K", "P"): 3.44942, ("K", "As"): 3.94942,
    ("K", "H"): 3.21942, ("Kr", "F"): 2.67549, ("La", "O"): 2.90983, ("La", "S"): 3.35593,
    ("La", "Se"): 3.45293, ("La", "Te"): 3.65293, ("La", "F"): 2.79293, ("La", "Cl"): 3.33452,
    ("La", "Br"): 3.43293, ("La", "I"): 3.64293, ("La", "N"): 3.05293, ("La", "P"): 3.32293,
    ("La", "As"): 3.51293, ("La", "H"): 2.77293, ("Li", "O"): 2.60087, ("Li", "S"): 3.02481,
    ("Li", "Se"): 3.24330, ("Li", "Te"): 3.42496, ("Li", "F"): 2.34276, ("Li", "Cl"): 2.91814,
    ("Li", "Br"): 3.11654, ("Li", "I"): 3.37676, ("Li", "N"): 2.66213, ("Lu", "O"): 2.57749,
    ("Lu", "S"): 3.03649, ("Lu", "Se"): 3.16649, ("Lu", "Te"): 3.35649, ("Lu", "F"): 2.48249,
    ("Lu", "Cl"): 2.96944, ("Lu", "Br"): 3.11945, ("Lu", "I"): 3.36945, ("Lu", "N"): 2.71649,
    ("Lu", "P"): 3.11649, ("Lu", "As"): 3.19649, ("Lu", "H"): 2.42649, ("Mg", "O"): 2.41824,
    ("Mg", "S"): 2.89293, ("Mg", "Se"): 3.03293, ("Mg", "Te"): 3.24293, ("Mg", "F"): 2.29093,
    ("Mg", "Cl"): 2.79293, ("Mg", "Br"): 2.99293, ("Mg", "I"): 3.17293, ("Mg", "N"): 2.56293,
    ("Mg", "P"): 3.00293, ("Mg", "As"): 3.09293, ("Mg", "H"): 2.24293, ("Mn", "O"): 2.51652,
    ("Mn", "S"): 2.93293, ("Mn", "F"): 2.41093, ("Mn", "Cl"): 2.84593, ("Mn", "Br"): 3.05293,
    ("Mn", "I"): 3.23293, ("Mn", "N"): 2.56193, ("Mn", "Se"): 2.47642, ("Mn", "Te"): 2.70642,
    ("Mn", "P"): 2.39642, ("Mn", "As"): 2.51642, ("Mn", "H"): 1.70642, ("Mo", "S"): 2.80067,
    ("Mo", "Cl"): 2.80447, ("Mo", "O"): 2.34750, ("Mo", "F"): 2.29980, ("Mo", "Br"): 2.85350,
    ("Mo", "N"): 2.47350, ("Mo", "I"): 2.74701, ("Mo", "Se"): 2.59701, ("Mo", "Te"): 2.79701,
    ("Mo", "P"): 2.54701, ("Mo", "As"): 2.62701, ("Mo", "H"): 1.83701, ("N", "O"): 1.81746,
    ("N", "F"): 1.82646, ("N", "Cl"): 2.20646, ("N", "N"): 1.88260, ("Na", "O"): 2.95693,
    ("Na", "S"): 3.57685, ("Na", "Se"): 3.71593, ("Na", "Te"): 3.95459, ("Na", "F"): 2.80398,
    ("Na", "Cl"): 3.39412, ("Na", "Br"): 3.57715, ("Na", "I"): 3.88251, ("Na", "N"): 3.12942,
    ("Na", "P"): 3.47942, ("Na", "As"): 3.64942, ("Na", "H"): 2.79942, ("Nb", "O"): 2.45329,
    ("Nb", "F"): 2.35646, ("Nb", "Cl"): 2.76291, ("Nb", "Br"): 3.07646, ("Nb", "N"): 2.46046,
    ("Nb", "I"): 3.14390, ("Nb", "S"): 2.74000, ("Nb", "Se"): 2.66642, ("Nb", "Te"): 2.85642,
    ("Nb", "P"): 2.61642, ("Nb", "As"): 2.69642, ("Nb", "H"): 1.90642, ("Nd", "O"): 2.85870,
    ("Nd", "S"): 3.42712, ("Nd", "Se"): 3.42293, ("Nd", "Te"): 3.60293, ("Nd", "F"): 2.73452,
    ("Nd", "Cl"): 3.22493, ("Nd", "Br"): 3.37293, ("Nd", "I"): 3.59452, ("Nd", "N"): 3.01293,
    ("Ni", "O"): 2.28149, ("Ni", "S"): 2.58649, ("Ni", "F"): 2.20249, ("Ni", "Cl"): 2.62649,
    ("Ni", "Br"): 2.80649, ("Ni", "I"): 3.00649, ("Ni", "N"): 2.30649, ("Ni", "Se"): 2.18998,
    ("Ni", "Te"): 2.47998, ("Ni", "P"): 2.31998, ("Ni", "As"): 2.28998, ("Ni", "H"): 1.44998,
    ("Np", "F"): 2.59233, ("Np", "Cl"): 3.07233, ("Np", "S"): 3.20000, ("Np", "Br"): 3.21233,
    ("Np", "I"): 3.44233, ("Np", "O"): 2.63646, ("O", "O"): 1.70000, ("Os", "O"): 2.23000,
    ("Os", "S"): 2.56002, ("Os", "F"): 2.07746, ("Os", "Cl"): 2.54002, ("Os", "Br"): 2.72002,
    ("P", "O"): 2.08646, ("P", "S"): 2.57646, ("P", "Se"): 2.69646, ("P", "F"): 2.01002,
    ("P", "Cl"): 2.28746, ("P", "Br"): 2.44293, ("P", "N"): 1.97146, ("P", "I"): 2.44998,
    ("P", "P"): 2.48381, ("P", "As"): 2.29998, ("P", "H"): 1.45998, ("Pa", "O"): 2.63383,
    ("Pa", "F"): 2.54437, ("Pa", "Cl"): 3.01437, ("Pa", "Br"): 3.18437, ("Pb", "O"): 3.04096,
    ("Pb", "S"): 3.40395, ("Pb", "Se"): 3.55295, ("Pb", "F"): 2.92045, ("Pb", "Cl"): 3.39295,
    ("Pb", "Br"): 3.62451, ("Pb", "I"): 3.69562, ("Pb", "N"): 3.09670, ("Pb", "Te"): 3.14644,
    ("Pb", "P"): 2.94644, ("Pb", "As"): 3.02644, ("Pb", "H"): 2.27644, ("Pd", "O"): 2.39849,
    ("Pd", "S"): 2.69649, ("Pd", "F"): 2.34649, ("Pd", "Cl"): 2.65649, ("Pd", "Br"): 2.80649,
    ("Pd", "I"): 2.96649, ("Pd", "N"): 2.40451, ("Pd", "C"): 2.33649, ("Pd", "Se"): 2.26998,
    ("Pd", "Te"): 2.52998, ("Pd", "P"): 2.46998, ("Pd", "As"): 2.34998, ("Pd", "H"): 1.51998,
    ("Pm", "F"): 2.55233, ("Pm", "Cl"): 3.41233, ("Pm", "Br"): 3.18233, ("Po", "O"): 2.64646,
    ("Po", "F"): 2.83646, ("Pr", "O"): 2.74449, ("Pr", "S"): 3.20649, ("Pr", "Se"): 3.32649,
    ("Pr", "Te"): 3.50649, ("Pr", "F"): 2.62945, ("Pr", "Cl"): 3.12749, ("Pr", "Br"): 3.27649,
    ("Pr", "I"): 3.49649, ("Pr", "N"): 2.90649, ("Pr", "P"): 3.28649, ("Pr", "As"): 3.35649,
    ("Pr", "H"): 2.62649, ("Pt", "O"): 2.40649, ("Pt", "S"): 2.76649, ("Pt", "F"): 2.54002,
    ("Pt", "Cl"): 2.75646, ("Pt", "Br"): 2.94191, ("Pt", "C"): 2.36649, ("Pt", "N"): 2.41649,
    ("Pt", "I"): 2.41998, ("Pt", "Se"): 2.23998, ("Pt", "Te"): 2.49998, ("Pt", "P"): 2.23998,
    ("Pt", "As"): 2.30998, ("Pt", "H"): 1.44998, ("Pu", "O"): 2.68329, ("Pu", "F"): 2.58233,
    ("Pu", "Cl"): 3.05233, ("Pu", "S"): 3.30000, ("Pu", "Br"): 3.19233, ("Pu", "I"): 3.43233,
    ("Rb", "O"): 3.43945, ("Rb", "S"): 3.97645, ("Rb", "Se"): 4.13773, ("Rb", "Te"): 4.28802,
    ("Rb", "F"): 3.37645, ("Rb", "Cl"): 3.86664, ("Rb", "Br"): 4.05498, ("Rb", "I"): 4.33462,
    ("Rb", "N"): 3.79645, ("Rb", "P"): 3.50645, ("Rb", "As"): 4.04645, ("Rb", "H"): 3.43645,
    ("Re", "Cl"): 3.44712, ("Re", "O"): 2.34260, ("Re", "F"): 2.16002, ("Re", "Br"): 2.70002,
    ("Re", "I"): 2.65998, ("Re", "S"): 2.61998, ("Re", "Se"): 2.54998, ("Re", "Te"): 2.74998,
    ("Re", "N"): 2.10998, ("Re", "P"): 2.50998, ("Re", "As"): 2.61998, ("Re", "H"): 1.79998,
    ("Rh", "O"): 2.24946, ("Rh", "F"): 2.16646, ("Rh", "Cl"): 2.62646, ("Rh", "Br"): 2.71260,
    ("Rh", "N"): 2.26260, ("Rh", "I"): 2.52998, ("Rh", "S"): 2.19998, ("Rh", "Se"): 2.37998,
    ("Rh", "Te"): 2.59998, ("Rh", "P"): 2.43998, ("Rh", "As"): 2.41998, ("Rh", "H"): 1.59998,
    ("Ru", "Se"): 2.69451, ("Ru", "F"): 2.57646, ("Ru", "O"): 2.22646, ("Ru", "S"): 2.64260,
    ("Ru", "Cl"): 2.70646, ("Ru", "N"): 2.26260, ("Ru", "Br"): 2.30998, ("Ru", "I"): 2.52998,
    ("Ru", "Te"): 2.58998, ("Ru", "P"): 2.33998, ("Ru", "As"): 2.40998, ("Ru", "H"): 1.65998,
    ("S", "O"): 1.80000, ("S", "S"): 2.20000, ("S", "N"): 2.28849, ("S", "F"): 1.95002,
    ("S", "Cl"): 2.37002, ("S", "Br"): 2.21998, ("S", "I"): 2.40998, ("S", "H"): 1.42998,
    ("Sb", "O"): 2.45237, ("Sb", "S"): 3.05000, ("Sb", "Se"): 3.05646, ("Sb", "F"): 2.35646,
    ("Sb", "Cl"): 2.80646, ("Sb", "Br"): 2.96646, ("Sb", "I"): 3.21646, ("Sb", "N"): 2.56446,
    ("Sb", "Te"): 2.82998, ("Sb", "P"): 2.56998, ("Sb", "As"): 2.64998, ("Sb", "H"): 2.81998,
    ("Sc", "O"): 2.42029, ("Sc", "S"): 2.88391, ("Sc", "Se"): 3.00291, ("Sc", "Te"): 3.20291,
    ("Sc", "F"): 2.32291, ("Sc", "Cl"): 2.92291, ("Sc", "Br"): 2.94291, ("Sc", "I"): 3.15291,
    ("Sc", "N"): 2.54291, ("Sc", "P"): 2.96291, ("Sc", "As"): 3.04291, ("Sc", "H"): 2.24291,
    ("Se", "S"): 2.81649, ("Se", "Se"): 2.93649, ("Se", "O"): 2.16102, ("Se", "F"): 2.08002,
    ("Se", "Cl"): 2.57002, ("Se", "Br"): 2.78002, ("Se", "N"): 2.10000, ("Se", "I"): 2.58998,
    ("Se", "H"): 1.58998, ("Si", "O"): 1.99002, ("Si", "S"): 2.47602, ("Si", "Se"): 2.61002,
    ("Si", "Te"): 2.84002, ("Si", "F"): 1.93002, ("Si", "Cl"): 2.38002, ("Si", "Br"): 2.55002,
    ("Si", "I"): 2.76002, ("Si", "C"): 2.23302, ("Si", "N"): 2.12002, ("Si", "P"): 2.58002,
    ("Si", "As"): 2.66002, ("Si", "H"): 1.82002, ("Si", "Si"): 2.60000, ("Sm", "O"): 2.88251,
    ("Sm", "N"): 3.02351, ("Sm", "S"): 3.15649, ("Sm", "Se"): 3.27649, ("Sm", "Te"): 3.46649,
    ("Sm", "F"): 2.60649, ("Sm", "Cl"): 3.08749, ("Sm", "Br"): 3.26649, ("Sm", "I"): 3.44649,
    ("Sm", "P"): 3.23649, ("Sm", "As"): 3.30649, ("Sm", "H"): 2.56649, ("Sn", "O"): 2.82146,
    ("Sn", "S"): 3.15293, ("Sn", "F"): 2.63793, ("Sn", "Cl"): 3.13111, ("Sn", "Br"): 3.21520,
    ("Sn", "I"): 3.52293, ("Sn", "N"): 2.71520, ("Sn", "Se"): 2.96646, ("Sn", "Te"): 2.91642,
    ("Sn", "P"): 2.60642, ("Sn", "As"): 2.77642, ("Sn", "H"): 2.00642, ("Sr", "O"): 2.98095,
    ("Sr", "S"): 3.51295, ("Sr", "Se"): 3.58295, ("Sr", "Te"): 3.73295, ("Sr", "F"): 2.88195,
    ("Sr", "Cl"): 3.37295, ("Sr", "Br"): 3.54295, ("Sr", "I"): 3.74295, ("Sr", "N"): 3.09295,
    ("Sr", "P"): 3.43295, ("Sr", "As"): 3.62295, ("Sr", "H"): 2.87295, ("Ta", "O"): 2.74646,
    ("Ta", "S"): 2.84390, ("Ta", "F"): 2.25390, ("Ta", "Cl"): 2.67390, ("Ta", "Br"): 2.60642,
    ("Ta", "I"): 2.81642, ("Ta", "Se"): 2.66642, ("Ta", "Te"): 2.85642, ("Ta", "N"): 2.16642,
    ("Ta", "P"): 2.62642, ("Ta", "As"): 2.70642, ("Ta", "H"): 1.91642, ("Tb", "O"): 2.65549,
    ("Tb", "S"): 3.11649, ("Tb", "Se"): 3.23649, ("Tb", "Te"): 3.42649, ("Tb", "F"): 2.54249,
    ("Tb", "Cl"): 3.04349, ("Tb", "Br"): 3.18649, ("Tb", "I"): 3.40945, ("Tb", "N"): 2.80649,
    ("Tb", "P"): 3.19649, ("Tb", "As"): 3.26649, ("Tb", "H"): 2.51649, ("Tc", "O"): 2.22446,
    ("Tc", "F"): 2.24219, ("Tc", "Cl"): 2.56002, ("Te", "O"): 2.33340, ("Te", "S"): 2.79002,
    ("Te", "F"): 2.22002, ("Te", "Cl"): 2.73906, ("Te", "Br"): 2.90002, ("Te", "I"): 3.13702,
    ("Te", "Se"): 2.57998, ("Te", "Te"): 2.80998, ("Te", "N"): 2.16998, ("Te", "P"): 2.56998,
    ("Te", "H"): 1.87998, ("Th", "O"): 2.77349, ("Th", "S"): 3.24649, ("Th", "Se"): 3.36649,
    ("Th", "Te"): 3.54649, ("Th", "F"): 2.68945, ("Th", "Cl"): 3.15945, ("Th", "Br"): 3.31945,
    ("Th", "I"): 3.56649, ("Th", "N"): 2.94649, ("Th", "P"): 3.33649, ("Th", "As"): 3.40649,
    ("Th", "H"): 2.67649, ("Ti", "F"): 2.86293, ("Ti", "Cl"): 3.02293, ("Ti", "Br"): 3.20293,
    ("Ti", "O"): 2.35391, ("Ti", "S"): 2.74646, ("Ti", "I"): 3.08291, ("Ti", "Se"): 2.53642,
    ("Ti", "Te"): 2.95642, ("Ti", "N"): 2.08642, ("Ti", "P"): 2.51642, ("Ti", "As"): 2.87642,
    ("Ti", "H"): 1.76642, ("Tl", "O"): 3.36945, ("Tl", "S"): 3.66442, ("Tl", "F"): 3.26942,
    ("Tl", "Cl"): 3.72942, ("Tl", "Br"): 3.80942, ("Tl", "I"): 3.94142, ("Tl", "Se"): 3.00644,
    ("Tl", "Te"): 3.23644, ("Tl", "N"): 2.59644, ("Tl", "P"): 3.01644, ("Tl", "As"): 3.09644,
    ("Tl", "H"): 2.35644, ("Tm", "O"): 2.60649, ("Tm", "S"): 3.05649, ("Tm", "Se"): 3.18649,
    ("Tm", "Te"): 3.37649, ("Tm", "F"): 2.51649, ("Tm", "Cl"): 2.98944, ("Tm", "Br"): 3.13945,
    ("Tm", "I"): 3.37945, ("Tm", "N"): 2.74649, ("Tm", "P"): 3.13649, ("Tm", "As"): 3.22649,
    ("Tm", "H"): 2.45649, ("U", "O"): 2.94295, ("U", "S"): 3.25293, ("U", "F"): 2.80293,
    ("U", "Cl"): 3.24452, ("U", "Br"): 3.39452, ("U", "I"): 3.62452, ("U", "N"): 2.78649,
    ("U", "Se"): 3.00644, ("U", "Te"): 3.16644, ("U", "P"): 2.94644, ("U", "As"): 3.02644,
    ("U", "H"): 2.27644, ("V", "O"): 2.84939, ("V", "Cl"): 3.15293, ("V", "S"): 2.82293,
    ("V", "F"): 2.87293, ("V", "Br"): 2.87329, ("V", "N"): 2.38329, ("V", "I"): 2.66642,
    ("V", "Se"): 2.48642, ("V", "Te"): 2.72642, ("V", "P"): 2.46642, ("V", "As"): 2.54642,
    ("V", "H"): 1.73642, ("W", "O"): 2.20102, ("W", "F"): 2.03000, ("W", "Cl"): 2.47000,
    ("W", "Br"): 2.49998, ("W", "I"): 2.70998, ("W", "S"): 2.43998, ("W", "Se"): 2.55998,
    ("W", "Te"): 2.75998, ("W", "N"): 2.10998, ("W", "P"): 2.50998, ("W", "As"): 2.58998,
    ("W", "H"): 1.80998, ("Xe", "O"): 2.63451, ("Xe", "F"): 2.62649, ("Y", "O"): 2.62549,
    ("Y", "S"): 3.08649, ("Y", "Se"): 3.21649, ("Y", "Te"): 3.40649, ("Y", "F"): 2.51049,
    ("Y", "Cl"): 3.00649, ("Y", "Br"): 3.15649, ("Y", "I"): 3.37649, ("Y", "N"): 2.77649,
    ("Y", "P"): 3.17649, ("Y", "As"): 3.24649, ("Y", "H"): 2.46649, ("Yb", "O"): 2.74551,
    ("Yb", "N"): 2.84851, ("Yb", "S"): 3.03649, ("Yb", "Se"): 3.16649, ("Yb", "Te"): 3.36649,
    ("Yb", "F"): 2.50649, ("Yb", "Cl"): 2.98249, ("Yb", "Br"): 3.12945, ("Yb", "I"): 3.37945,
    ("Yb", "P"): 3.13649, ("Yb", "As"): 3.19649, ("Yb", "H"): 2.42649, ("Zn", "O"): 2.41693,
    ("Zn", "S"): 2.80293, ("Zn", "Se"): 2.93293, ("Zn", "Te"): 3.16293, ("Zn", "F"): 2.38293,
    ("Zn", "Cl"): 2.72293, ("Zn", "Br"): 2.86293, ("Zn", "I"): 3.07293, ("Zn", "N"): 2.43293,
    ("Zn", "P"): 2.86293, ("Zn", "As"): 2.95293, ("Zn", "H"): 2.13293, ("Zr", "O"): 3.09651,
    ("Zr", "F"): 2.99651, ("Zr", "Cl"): 3.33651, ("Zr", "S"): 2.91004, ("Zr", "Se"): 3.03004,
    ("Zr", "Te"): 3.17004, ("Zr", "Br"): 2.98004, ("Zr", "I"): 3.19004, ("Zr", "N"): 2.65004,
    ("Zr", "P"): 3.02004, ("Zr", "As"): 3.07004, ("Zr", "H"): 2.29004
}

import numpy as np
from ase.io import read
from pymatgen import Structure
import pandas as pd
from abinitostudio.ui.UI_vasp_supercell import Ui_Form_UI_supercell
from PyQt5.QtWidgets import QDialog, QMessageBox


# Supercell Dialog
class Supercell_Dialog(QDialog, Ui_Form_UI_supercell):
    def __init__(self):
        super(Supercell_Dialog, self).__init__()
        self.setupUi(self)

    def warning_4(self):
        dlgTitle = "Warning"
        strInfo = "A structure is not opened！"
        QMessageBox.warning(self, dlgTitle, strInfo)
        print("A structure is not opened！")


class structure_plot():
    def __init__(self, scene):
        self.showcell = True
        self.supercell = (1, 1, 1)
        self.cell_linewidth = 0.02
        self.cell_linecolor = (1, 1, 1)

        self.atom_oper = None
        self.shift_size = None
        self.scene = scene

    def build_supercell(self):
        dialog_supercell = Supercell_Dialog()
        dialog_supercell.setModal(True)

        def get_supercell_parameter():
            value_a = dialog_supercell.spinBox.value()
            value_b = dialog_supercell.spinBox_2.value()
            value_c = dialog_supercell.spinBox_3.value()
            self.supercell = (int(value_a), int(value_b), int(value_c))

        dialog_supercell.show()
        dialog_supercell.pushButton.clicked.connect(get_supercell_parameter)
        dialog_supercell.exec_()
        try:
            self.get_info_poscar()
            self.plot_str()
        except:
            dialog_supercell.warning_4()

    def warning_4(self):
        dlgTitle = "Warning"
        strInfo = "A structure is not opened！"
        QMessageBox.warning(self, dlgTitle, strInfo)
        print("A structure is not opened！")

    def adjust_cell(self, showcell, supercell, cell_linewidth, cell_linecolor):
        self.showcell = showcell
        self.supercell = supercell
        self.cell_linewidth = cell_linewidth
        self.cell_linecolor = cell_linecolor

    def read_poscar(self, filename):
        # print(self.supercell)
        # read the POSCAR
        self.poscar_tmp = read(filename, format='vasp')
        # print(self.poscar_tmp.positions)
        # print(self.poscar_tmp)
        # store the cell in case we need to make a supercell
        self.ucell = self.poscar_tmp.cell.copy()

    def get_info_poscar(self):
        # making supercells
        repeat = self.supercell
        self.poscar = self.poscar_tmp * repeat
        self.nions = self.poscar.get_global_number_of_atoms()
        self.atom_chem_symb = np.array(self.poscar.get_chemical_symbols())
        self.uniq_atom_chem_symb = list(set(self.atom_chem_symb))
        self.ntype = len(self.uniq_atom_chem_symb)
        atom_index = np.arange(self.nions, dtype=int)
        # index of atoms for each type of elements
        self.atom_type_integerID = dict([
            (self.uniq_atom_chem_symb[itype], atom_index[self.atom_chem_symb == self.uniq_atom_chem_symb[itype]])
            for itype in range(self.ntype)
        ])
        # number of atoms for each type of elements
        self.atom_type_num = [len(self.atom_type_integerID[k]) for k in self.uniq_atom_chem_symb]

    def get_periodic_positions(self, pos):
        eps = 10e-6
        ndim = 3
        npos = np.shape(pos)[0]
        add_atom = 0
        del_all = []
        for i in range(npos):
            ntot = 0;
            pos_flag = []
            for j in range(ndim):
                if abs(pos[i][j]) < eps:
                    ntot = ntot + 1
                    pos_flag.append(j)
                elif abs(pos[i][j] - 1.0) < eps:
                    ntot = ntot + 1
                    pos_flag.append(j)
            if ntot == 1:
                del_all.append(i)
                pos_new = pos[i]
                pos_new[pos_flag[0]] = 0.0;
                pos = np.append(pos, [pos_new], axis=0)
                pos_new[pos_flag[0]] = 1.0;
                pos = np.append(pos, [pos_new], axis=0)
                add_atom = add_atom + 1
            elif ntot == 2:
                del_all.append(i)
                pos_new = pos[i]
                pos_new[pos_flag[0]] = 0.0;
                pos_new[pos_flag[1]] = 0.0;
                pos = np.append(pos, [pos_new], axis=0)
                pos_new[pos_flag[0]] = 0.0;
                pos_new[pos_flag[1]] = 1.0;
                pos = np.append(pos, [pos_new], axis=0)
                pos_new[pos_flag[0]] = 1.0;
                pos_new[pos_flag[1]] = 0.0;
                pos = np.append(pos, [pos_new], axis=0)
                pos_new[pos_flag[0]] = 1.0;
                pos_new[pos_flag[1]] = 1.0;
                pos = np.append(pos, [pos_new], axis=0)
                add_atom = add_atom + 3
            elif ntot == 3:
                del_all.append(i)
                pos_new = pos[i]
                pos_new[0] = 0.0;
                pos_new[1] = 0.0;
                pos_new[2] = 0.0;
                pos = np.append(pos, [pos_new], axis=0)
                pos_new[0] = 1.0;
                pos_new[1] = 0.0;
                pos_new[2] = 0.0;
                pos = np.append(pos, [pos_new], axis=0)
                pos_new[0] = 0.0;
                pos_new[1] = 1.0;
                pos_new[2] = 0.0;
                pos = np.append(pos, [pos_new], axis=0)
                pos_new[0] = 0.0;
                pos_new[1] = 0.0;
                pos_new[2] = 1.0;
                pos = np.append(pos, [pos_new], axis=0)
                pos_new[0] = 1.0;
                pos_new[1] = 1.0;
                pos_new[2] = 0.0;
                pos = np.append(pos, [pos_new], axis=0)
                pos_new[0] = 0.0;
                pos_new[1] = 1.0;
                pos_new[2] = 1.0;
                pos = np.append(pos, [pos_new], axis=0)
                pos_new[0] = 1.0;
                pos_new[1] = 0.0;
                pos_new[2] = 1.0;
                pos = np.append(pos, [pos_new], axis=0)
                pos_new[0] = 1.0;
                pos_new[1] = 1.0;
                pos_new[2] = 1.0;
                pos = np.append(pos, [pos_new], axis=0)
                add_atom = add_atom + 7

        return np.delete(pos, del_all, axis=0), add_atom

    def get_periodic_position_single(self, pos):
        eps = 10e-6
        ndim = 3
        add_atom = 0
        ntot = 0;
        pos_flag = []
        all_pos = pos
        for j in range(ndim):
            if abs(pos[j]) < eps:
                ntot = ntot + 1
                pos_flag.append(j)
            elif abs(pos[j] - 1.0) < eps:
                ntot = ntot + 1
                pos_flag.append(j)
        if ntot == 1:
            all_pos = [[] for i in range(2)]
            pos_new = pos
            pos_new[pos_flag[0]] = 0.0
            all_pos[0].extend(pos_new)
            pos_new[pos_flag[0]] = 1.0
            all_pos[1].extend(pos_new)
            # print(pos_new)
            add_atom = add_atom + 1
        elif ntot == 2:
            all_pos = [[] for i in range(4)]
            pos_new = pos
            pos_new[pos_flag[0]] = 0.0;
            pos_new[pos_flag[1]] = 0.0;
            all_pos[0].extend(pos_new)
            pos_new[pos_flag[0]] = 0.0;
            pos_new[pos_flag[1]] = 1.0;
            all_pos[1].extend(pos_new)
            pos_new[pos_flag[0]] = 1.0;
            pos_new[pos_flag[1]] = 0.0;
            all_pos[2].extend(pos_new)
            pos_new[pos_flag[0]] = 1.0;
            pos_new[pos_flag[1]] = 1.0;
            all_pos[3].extend(pos_new)
            add_atom = add_atom + 3
        elif ntot == 3:
            all_pos = [[] for i in range(8)]
            pos_new = pos
            pos_new[0] = 0.0;
            pos_new[1] = 0.0;
            pos_new[2] = 0.0;
            all_pos[0].extend(pos_new)
            pos_new[0] = 1.0;
            pos_new[1] = 0.0;
            pos_new[2] = 0.0;
            all_pos[1].extend(pos_new)
            pos_new[0] = 0.0;
            pos_new[1] = 1.0;
            pos_new[2] = 0.0;
            all_pos[2].extend(pos_new)
            pos_new[0] = 0.0;
            pos_new[1] = 0.0;
            pos_new[2] = 1.0;
            all_pos[3].extend(pos_new)
            pos_new[0] = 1.0;
            pos_new[1] = 1.0;
            pos_new[2] = 0.0;
            all_pos[4].extend(pos_new)
            pos_new[0] = 0.0;
            pos_new[1] = 1.0;
            pos_new[2] = 1.0;
            all_pos[5].extend(pos_new)
            pos_new[0] = 1.0;
            pos_new[1] = 0.0;
            pos_new[2] = 1.0;
            all_pos[6].extend(pos_new)
            pos_new[0] = 1.0;
            pos_new[1] = 1.0;
            pos_new[2] = 1.0;
            all_pos[7].extend(pos_new)
            add_atom = add_atom + 7

        return np.array(all_pos), add_atom

    def plot_str(self):
        self.all_spheres = []
        self.all_pos_num = []
        self.all_pos = []
        self.all_plot_pos = []
        self.all_color = []
        self.scene.mlab.clf()
        self.figure = self.scene.mlab.gcf()
        self.figure.scene.disable_render = True

        ############################################################
        # Draw the cell box
        ############################################################
        # Draw the unit cell:
        if self.showcell:
            Nx, Ny, Nz = self.supercell
            fx = range(Nx + 1)
            fy = range(Ny + 1)
            fz = range(Nz + 1)
            Dxyz = np.array(np.meshgrid(fx, fy, fz, indexing='ij'))
            Cxyz = np.array(np.tensordot(self.ucell, Dxyz, axes=(0, 0)))
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
            cell_box = self.scene.mlab.plot3d(Cxyz[0], Cxyz[1], Cxyz[2],
                                              tube_radius=self.cell_linewidth,
                                              color=self.cell_linecolor,
                                              name='CellBox'
                                              )
            cell_box.mlab_source.dataset.lines = np.array(conn)

        for itype in range(self.ntype):
            # element name for this type
            typeName = self.uniq_atom_chem_symb[itype]
            # index for this type
            typeID = self.atom_type_integerID[typeName]
            # number of atoms for this type
            typeNo = self.atom_type_num[itype]

            # the coordinates for this type
            typePos_tmp = self.poscar.positions[typeID]

            scaled_pos = self.poscar.cell.scaled_positions(typePos_tmp)

            #            scaled_typePos, add_atoms = self.get_periodic_positions(scaled_pos)
            #            typePos = self.poscar.cell.cartesian_positions(scaled_typePos)
            #            typeNo = typeNo + add_atoms
            # the atom color for this type
            typeClr = pt_atomic_color[pt_atomic_name.index(typeName)]
            # the atom radius for this type
            typeRad = pt_atomic_radius[pt_atomic_name.index(typeName)]

            for i in range(typeNo):
                pos_tmp1, add_atom = self.get_periodic_position_single(scaled_pos[i])

                if add_atom == 0:
                    pos_tmp = self.poscar.cell.cartesian_positions([pos_tmp1])
                    # for each euqivalent atom
                    sphere_tmp = self.scene.mlab.points3d(pos_tmp[0][0], pos_tmp[0][1], pos_tmp[0][2],
                                                          np.ones(add_atom + 1) * typeRad,
                                                          color=typeClr, resolution=60,
                                                          scale_factor=1.0,
                                                          name="AtomSphere_{}".format(typeName))
                    self.all_plot_pos.append(np.array([pos_tmp]))
                else:
                    pos_tmp = self.poscar.cell.cartesian_positions(pos_tmp1)
                    # for each euqivalent atom
                    sphere_tmp = self.scene.mlab.points3d(pos_tmp[:, 0], pos_tmp[:, 1], pos_tmp[:, 2],
                                                          np.ones(add_atom + 1) * typeRad,
                                                          color=typeClr, resolution=60,
                                                          scale_factor=1.0,
                                                          name="AtomSphere_{}".format(typeName))
                    self.all_plot_pos.append(pos_tmp)
                self.all_spheres.append(sphere_tmp)
                self.all_pos_num.append(add_atom + 1)
                self.all_color.append(sphere_tmp.actor.property.color)
                self.all_pos.append(typePos_tmp[i])

        ############################################################
        # plot the bonds
        ############################################################
        # first, find out the possible conbinations 
        type_of_bonds = []
        bond_max_of_each_type = []

        for ii in range(self.ntype):
            for jj in range(ii + 1):
                A = self.uniq_atom_chem_symb[ii]
                B = self.uniq_atom_chem_symb[jj]

                # check if A and B can form a bond
                if (A, B) in pt_max_bond:
                    AB = (A, B)
                elif (B, A) in pt_max_bond:
                    AB = (B, A)
                else:
                    AB = None

                if AB is not None:
                    type_of_bonds.append((A, B))
                    bond_max_of_each_type.append(pt_max_bond[AB])

        ############################################################
        # second, connect each possible bond
        ############################################################

        # Again, iterate over the bonds is a lot slower than iterate over the types of
        # bonds.
        n_type_bonds = len(type_of_bonds)
        for itype in range(n_type_bonds):
            A, B = type_of_bonds[itype]
            L = bond_max_of_each_type[itype]

            A_ID = self.uniq_atom_chem_symb.index(A)
            B_ID = self.uniq_atom_chem_symb.index(B)

            A_atom_IDs = self.atom_type_integerID[A]
            B_atom_IDs = self.atom_type_integerID[B]

            # find out all the possible bonds: A-B
            ijs = []
            if A == B:
                A_atom_Num = self.atom_type_num[A_ID]
                for ii in range(A_atom_Num):
                    for jj in range(ii):
                        if self.poscar.get_distance(A_atom_IDs[ii], B_atom_IDs[jj]) < L:
                            ijs.append((A_atom_IDs[ii], B_atom_IDs[jj]))
            else:
                for ii in A_atom_IDs:
                    for jj in B_atom_IDs:
                        if self.poscar.get_distance(ii, jj) < L:
                            ijs.append((ii, jj))
            ijs = np.array(ijs, dtype=int)

            if ijs.size > 0:
                A_color = pt_atomic_color[pt_atomic_name.index(A)]
                B_color = pt_atomic_color[pt_atomic_name.index(B)]

                p_A = self.poscar.positions[ijs[:, 0]]
                p_B = self.poscar.positions[ijs[:, 1]]
                # The coordinate of the middle point in the bond A-B
                p_M = (p_A + p_B) / 2.
                p_T = np.zeros((ijs.shape[0] * 2, 3))
                p_T[1::2, :] = p_M
                # only connect the bonds
                bond_connectivity = np.vstack(
                    [range(0, 2 * ijs.shape[0], 2),
                     range(1, 2 * ijs.shape[0], 2)]
                ).T

                # plot the first half of the bond: A-M
                p_T[0::2, :] = p_A
                bond_A = self.scene.mlab.plot3d(p_T[:, 0], p_T[:, 1], p_T[:, 2],
                                                tube_radius=0.1, color=A_color,
                                                name="Bonds_{}-{}".format(A, B))
                bond_A.mlab_source.dataset.lines = bond_connectivity
                # plot the second half of the bond: M-B
                p_T[0::2, :] = p_B
                bond_B = self.scene.mlab.plot3d(p_T[:, 0], p_T[:, 1], p_T[:, 2],
                                                tube_radius=0.1, color=B_color,
                                                name="Bonds_{}-{}".format(A, B))
                bond_B.mlab_source.dataset.lines = bond_connectivity

        self.figure.scene.disable_render = False
        self.all_pos = pd.DataFrame(self.all_pos, columns=['x', 'y', 'z'])

    def animate_atoms(self):
        @mlab.animate(delay=100)
        def updateAnimation():
            t = 0.0
            while True:
                self.all_spheres[0].mlab_source.set(x=np.cos(t), y=np.sin(t), z=0)
                t += 0.1
                yield

        updateAnimation()

    def recover_colors(self):
        for i in range(len(self.all_pos)):
            self.all_spheres[i].actor.property.color = self.all_color[i]

    def picker_atoms(self):

        g1 = self.all_spheres[0].glyph.glyph_source.glyph_source.output.points.to_array()

        def picker_callback(picker):
            self.recover_colors()
            for i in range(len(self.all_pos)):
                if picker.actor in self.all_spheres[i].actor.actors:
                    self.atom_oper = i
                    point_id = int(picker.point_id / g1.shape[0])  # int向下取整        
                    if point_id != -1:  # 如果没有小球被选取，则point_id = -1
                        self.all_spheres[i].actor.property.color = (1, 0, 0)

                        self.shift_atom_x()

        #                # get coordinates of mouse click position
        #                cen = picker.pick_position
        #                # compute Euclidean distance btween mouse position and all nodes
        #                dist = np.linalg.norm(self.all_pos-cen, axis=1)
        #                print(cen)
        #                # get closest node
        #                ni = np.argmin(dist)
        #                # hide/show node and text
        #                n = self.all_spheres[ni]
        #                n.actor.property.color = (1,0,0)

        #
        # add picker callback
        picker = self.figure.on_mouse_pick(picker_callback)
        picker.tolerance = 0.01

    def shift_atom_x(self):
        if self.atom_oper is not None:
            cam = self.figure.scene.camera
            print(cam.position)
            # vector to offset the camera loc and focal point
            v = np.zeros(3)

            # view plane vetor points behind viewing direction, so we invert it
            yhat = -1. * np.array(cam.view_plane_normal)
            zhat = cam.view_up
            xhat = np.cross(yhat, zhat)
            right = 5

            v += right * zhat

            newx = self.all_plot_pos[self.atom_oper].T[0] + np.array([v[0]] * self.all_pos_num[self.atom_oper])
            newy = self.all_plot_pos[self.atom_oper].T[1] + np.array([v[1]] * self.all_pos_num[self.atom_oper])
            newz = self.all_plot_pos[self.atom_oper].T[2] + np.array([v[2]] * self.all_pos_num[self.atom_oper])

            print(newx, newy, newz)

            #            self.all_spheres[self.atom_oper].mlab_source.set(x = 0,y = 0, z = 0)
            self.all_spheres[self.atom_oper].mlab_source.set(x=newx, y=newy, z=newz)
        else:
            print('Without atom is choosen!!')

    def shift_atom_y(self):
        if self.atom_oper is not None:
            cam = self.figure.scene.camera
            # vector to offset the camera loc and focal point
            v = np.zeros(3)

            # view plane vetor points behind viewing direction, so we invert it
            yhat = -1. * np.array(cam.view_plane_normal)
            zhat = cam.view_up
            xhat = np.cross(yhat, zhat)
            right = 0.5

            v += right * zhat
            self.all_spheres[i].mlab_source.set(x=self.all_pos[i][0] + v[0],
                                                y=self.all_pos[i][1] + v[1], z=self.all_pos[i][2] + v[2])
        else:
            print('Without atom is choosen!!')