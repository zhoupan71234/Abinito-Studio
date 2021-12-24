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
relax = 0; scf = 0; band = 0; scf_noncol = 0; bandsoc = 0; dos = 0
phonon = 0; wan = 0; 
# pbe or lda
pbe = 1
# directory
cal_dir = 'calculation'

for arg in sys.argv[1:]:
    k=arg.split("=")[0]
    v="=".join(arg.split("=")[1:])
    if   k=="relax"  : relax = int(v)
    elif k=="scf"  : scf = int(v)
    elif k=="band"  : scf = 1; band = int(v)
    elif k=="soc"  : scfsoc = int(v)
    elif k=="bandsoc"  : scfsoc = 1; bandsoc = int(v)
    elif k=="pbe"  : pbe = int(v)
    elif k=="npr"  : npr = int(v) 
    elif k=="vasp"  : vasp = v
    elif k=="vaspsoc"  : vaspsoc = v
    elif k=="psdir"  : psdir = v
    elif k=="listps"  : listps = v.split()
    elif k=="cal_dir"  : cal_dir = v
    elif k=="dos"  : scf = 1; dos = int(v)
    
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
        
os.system('mv INCAR* KPOINTS* POSCAR* wannier90.* ' + pathnew )
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
if scf == 1:
    if not os.path.exists('scf'):
        os.system('mkdir scf')
        if relax == 1:
            os.system('cp POTCAR ./scf')
            os.system('cp ./relax/CONTCAR ./scf/POSCAR')
        else:
            os.system('cp POSCAR POTCAR ./scf')
        os.chdir('./scf')
        os.system('cp ../INCAR_scf ./INCAR')
        os.system('cp ../KPOINTS_scf ./KPOINTS')
        os.system('mpirun -np ' + str(npr) + ' ' + vasp + ' ' + '>./log ')
        os.chdir('../')
        cfile = open('calculation.dat','w')
        cfile.write('scf_finished!')
        cfile.close()
    if band == 1:
        if not os.path.exists('band'):
            os.system('mkdir band')
            os.system('cp scf/POSCAR scf/POTCAR scf/CHGCAR ./band')
            os.chdir('./band')
            os.system('cp ../INCAR_band ./INCAR')
            os.system('cp ../KPOINTS_band ./KPOINTS')
            os.system('mpirun -np ' + str(npr) + ' ' + vasp + ' ' + '>./log ')
            os.chdir('../')
            cfile = open('calculation.dat','w')
            cfile.write('band_finished!')
            cfile.close()

if scf == 1:
    if not os.path.exists('scf'):
        os.system('mkdir scf')
        if relax == 1:
            os.system('cp POTCAR ./scf')
            os.system('cp ./relax/CONTCAR ./scf/POSCAR')
        else:
            os.system('cp POSCAR POTCAR ./scf')
        os.chdir('./scf')
        os.system('cp ../INCAR_scf ./INCAR')
        os.system('cp ../KPOINTS_scf ./KPOINTS')
        os.system('mpirun -np ' + str(npr) + ' ' + vasp + ' ' + '>./log ')
        os.chdir('../')
    if dos == 1:
        if not os.path.exists('dos'):
            os.system('mkdir dos')
            os.system('cp scf/POSCAR scf/POTCAR scf/CHGCAR ./dos')
            os.chdir('./dos')
            os.system('cp ../INCAR_dos ./INCAR')
            os.system('cp ../KPOINTS_dos ./KPOINTS')
            os.system('mpirun -np ' + str(npr) + ' ' + vasp + ' ' + '>./log ')
            os.chdir('../')   
            cfile = open('calculation.dat','w')
            cfile.write('dos_finished!')
            cfile.close()
        

        
# noncollinear calculation        
if scf_noncol == 1:
    if not os.path.exists('scfsoc'):
        os.system('mkdir scfsoc')
        if relax == 1:
            os.system('cp POTCAR ./scfsoc')
            os.system('cp ./relax/CONTCAR ./scfsoc/POSCAR')
        else:
            os.system('cp POSCAR POTCAR ./scfsoc')
        os.chdir('./scfsoc')
        os.system('cp ../INCAR_scf ./INCAR')
        os.system('cp ../KPOINTS_scf ./KPOINTS')
        os.system('mpirun -np ' + str(npr) + ' ' + vaspsoc + ' ' + '>./log ')
        os.chdir('../')
        if bandsoc == 1:
            if not os.path.exists('bandsoc'):
                os.system('mkdir bandsoc')
                os.system('cp scfsoc/POSCAR scfsoc/POTCAR scfsoc/CHGCAR ./bandsoc')
                os.chdir('./bandsoc')
                os.system('cp ../INCAR_band ./INCAR')
                os.system('cp ../KPOINTS_band ./KPOINTS')
                os.system('mpirun -np ' + str(npr) + ' ' + vaspsoc + ' ' + '>./log ')
                os.chdir('../')
                
if phonon == 1: 
    if not os.path.exists('phonon'):
    # decide whether the phononpy order is or not exist
    
        os.system('mkdir phonon')
        if relax == 1:
            os.system('cp POTCAR ./phonon')
            os.system('cp ./relax/CONTCAR ./phonon/POSCAR')
        else:
            os.system('cp POTCAR ./phonon')
        os.chdir('./phonon')
        os.system('mkdir relax')
        os.system('cp ../INCAR_phonon_relax ./relax/INCAR')
        os.system('cp ../KPOINTS_phonon_relax ./relax/KPOINTS')
        os.system('cp ../POSCAR ../POTCAR ./relax')
        os.chdir('./relax')
        os.system('mpirun -np ' + str(npr) + ' ' + vasp + ' ' + '>./log ')
        
        os.system('cp CONTCAR ../POSCAR-unitcell')
        os.chdir('../')
        
        os.system('phonopy -d --dim='+ "\'" + dim +"\'"+ ' -c POSCAR-unitcell')
        os.system('cp SPOSCAR POSCAR')
        os.system('cp ../INCAR_phonon ./INCAR')
        os.system('cp ../KPOINTS_phonon ./KPOINTS')
        os.system('mpirun -np ' + str(npr) + ' ' + vasp + ' ' + '>./log ')
    
        os.system('phonopy --fc vasprun.xml')
        pband = []
        sys_name = 'system'
        pband.append('ATOM_NAME = ' + sys_name)
        pband.append('DIM = ' + dim)
        pband.append('BAND = ' + kpath_phonon)
        bandfile = open('band.conf','w')
        for pi in range(len(pband)):
            bandfile.write(pband[pi]+'\n')	
        bandfile.close()
        bandorder = 'phonopy -p -s --readfc -c POSCAR-unitcell band.conf >>log ' 
        os.system(bandorder)
        os.system('phonopy-bandplot --gnuplot band.yaml > band.dat')
        os.chdir('../')
        cfile = open('calculation.dat','w')
        cfile.write('phonon_finished!')
        cfile.close()
    
if wan == 1:
    if not os.path.exists('wannier'):
    # decide wannier90.x is or not exist
        os.system('mkdir wannier')
        if relax == 1:
            os.system('cp POTCAR ./wannier')
            os.system('cp ./relax/CONTCAR ./wannier/POSCAR')
        else:
            os.system('cp POTCAR POSCAR ./wannier')
        os.system('cp ./scf/CHGCAR ./wannier/')
        os.system('cp wannier90.win ./wannier/')
        os.system('cp INCAR_wan ./wannier/INCAR')
        os.system('cp KPOINTS_wan ./wannier/KPOINTS')
        os.chdir('./wannier/')
        if wan_type == 'normal':
            os.system('mpirun -np ' + str(npr) + ' ' + vasp + ' ' + '>./log ')
            try:
                os.system('wannier90.x wannier90 >wanlog' )                
            except:
                print ("wannier90.x is not found or running wrong!!!")
                sys.exit(1)
        elif wan_type == 'spin-polarized':
            print ('This type is not implemented: wan_type = ' + wan_type)
            sys.exit(1)
        elif wan_type == 'noncol':
            print ('This type is not implemented: wan_type = ' + wan_type)
            sys.exit(1)
        else:
            print ('Undefined value for wan_type!!!!')
            sys.exit(1)
        cfile = open('calculation.dat','w')
        cfile.write('wan_finished!')
        cfile.close()