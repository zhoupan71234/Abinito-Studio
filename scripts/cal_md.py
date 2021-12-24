#!/usr/bin/env python

'''
@author Pan Zhou 
email: zhoupan71234@xtu.edu.cn
'''
import re
import os
import sys
import numpy as np


def produce_potcar(pseudo_dir, listpseudo, xc):
    psopt = ''
    for ips in range(len(listpseudo)):
        if xc == 1:
            psopt = psopt + pseudo_dir + 'pbe/' + listpseudo[ips] + '/POTCAR '
        else:
            psopt = psopt + pseudo_dir + 'lda/' + listpseudo[ips] + '/POTCAR '
    os.system('cat ' + psopt + ' >>./POTCAR')

# default values
relax = 0; 
# pbe or lda
pbe = 1
# directory
cal_dir = 'calculation'

for arg in sys.argv[1:]:
    k=arg.split("=")[0]
    v="=".join(arg.split("=")[1:])
    if   k=="relax"  : relax = int(v)
    elif k=="temp"  : temp = v
    elif k=="pbe"  : pbe = int(v)
    elif k=="npr"  : npr = int(v) 
    elif k=="vasp"  : vasp = v
    elif k=="psdir"  : psdir = v
    elif k=="listps"  : listps = v.split()
    elif k=="cal_dir"  : cal_dir = v
    
    # phonon calculation
    elif k=="phonon"  : phonon = int(v)
    elif k=='dim' : dim = v
    elif k=='kpath_phonon' : kpath_phonon = v
    
    # wannier90
    elif k=='wan' : scf = 1; wan = int(v)
    elif k=='wan_type' : wan_type = v


if not 'npr' in locals().keys():
    print('please set the number of process:')
    sys.exit()

if not 'vasp' in locals().keys():
    print('please set the order of vasp:')
    sys.exit()
    
if not 'psdir' in locals().keys():
    print('please set the directory of the pseudopotential:')
    sys.exit()
    
if not 'listps' in locals().keys():
    print('please set the elements of the pseudopotential:')
    sys.exit()


tmpdir = os.getcwd()
n = 0
pathnew = cal_dir
if not os.path.exists(pathnew):
    os.system('mkdir ' + pathnew)
#path_exist = os.path.exists('path.txt')
#if not path_exist:
#    while True:
#        if os.path.exists(pathnew):
#            n = n + 1
#            pathnew = cal_dir + str(n)
#        else:
#            os.system('mkdir ' + pathnew)
#            pfile = open('path.txt','w')
#            pfile.write(pathnew)
#            pfile.close()
#            break
#else:
#    rfile = open('path.txt','r')
#    name_tmp = rfile.readline()
#    rfile.close()
#    pathnew = name_tmp
        
os.system('mv INCAR* KPOINTS* POSCAR* ' + pathnew )
os.chdir('./'+ pathnew)

ispos = os.path.isfile('POTCAR')
if ispos is True:
    os.system('rm POTCAR')
produce_potcar(psdir, listps, pbe)

# relax the structure
if relax == 1:
    if not os.path.exists('relax'):
        os.system('mkdir relax')
        os.system('cp POSCAR POTCAR ./relax')
        os.chdir('./relax')
        os.system('cp ../INCAR_relax ./INCAR')
        os.system('cp ../KPOINTS_relax ./KPOINTS')
        os.system('mpirun -np ' + str(npr) + ' ' + vasp + ' ' + '>./log ')
        os.chdir('../')
    
# and energy band calculation
mdpath = 'md' + temp
if not os.path.exists(mdpath):
    os.system('mkdir ' + mdpath)
    if relax == 1:
        os.system('cp POTCAR ./' + mdpath)
        os.system('cp ./relax/CONTCAR ' + './'  + mdpath + '/POSCAR')
    else:
        os.system('cp POSCAR POTCAR ./' + mdpath)
    os.chdir('./'  + mdpath)
    os.system('cp ../INCAR_md' + temp + ' ./INCAR')
    os.system('cp ../KPOINTS_md' + temp +' ./KPOINTS')
    os.system('mpirun -np ' + str(npr) + ' ' + vasp + ' ' + '>./log ')
    os.chdir('../')
    cfile = open('calculation.dat','w')
    cfile.write('md'+ temp + '_finished!')
    cfile.close()

        

        

                

    
