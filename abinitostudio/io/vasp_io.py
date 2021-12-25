'''
Created on 2014.  05.  14.

@author: nwan
@author: hanwooh
'''
import numpy as np
import re
import itertools


def findReg(reg, file):
    f = open(file)
    lines = f.readlines()
    f.close()
    find = []
    for line in lines:
        m = re.findall(reg, line)
        find += m
    return find

def readPROCAR(fileName):
    f = open(fileName)
    read_lines = f.readlines()
    n_kpoints = int(read_lines[1].split()[3])
    n_bands = int(read_lines[1].split()[7])
    n_ions = int(read_lines[1].split()[11])
    # Orbital contributions
    total_band_atom = []
    total_k_atom = []
    total_atoms = []
    each_atom = []
    # Get number of rows
    n_ion_rows = []
    n_k_rows = []
    n_band_rows = []
    for index, value in enumerate(read_lines):
        # atomic rows
        if value == read_lines[7]:
            n_ion_rows.append(index + 1)
        # k-point rows
        if "k-point" in value.split():
            n_k_rows.append(index)
        # band rows
        if "band" in value.split():
            n_band_rows.append(index)
    # Get all orbital contributions per atom per energy band
    k_y = []  # Total vertical coordinates
    k_y_k = []  # Each k points, 180 points, 16 bars
    for index, value in enumerate(n_band_rows):
        numbers = read_lines[value].split()[4]
        # print(index + 1)
        k_y_k.append(float(numbers))
        if (index + 1) % n_bands == 0 and index != 0:
            # print(index)
            k_y.append(k_y_k)
            k_y_k = []
    for index, k in enumerate(n_ion_rows):  # 16 bands *180 k-points
        # Get total_k_atom
        for j in range(n_ions + 1):
            for i in range(1, 11):  # Invariant from s to tot
                each_atom.append(
                    float(read_lines[k + j].split()[i]))  # Get contribution per atom Num rows + num of atoms
            total_atoms.append(each_atom)  # Add each atom to the total atom
            each_atom = []  # Each atomic list is cleared
        # print(total_atoms)  # The contributions of all atoms in an energy band are stored in total_atoms
        total_k_atom.append(total_atoms)
        total_atoms = []
        if len(total_k_atom) == n_bands:  # Divide 2880 total_k_atom into 180 into total_band_atom
            total_band_atom.append(total_k_atom)
            total_k_atom = []
    # Bands horizontal coordinate
    kpts = []
    for i in n_k_rows:
        numbers = np.array(list(map(float, read_lines[i].split()[3:6])))  # Lists first, then arrays
        kpts.append(numbers)
        # break
    # print(Kpts)
    k_x = []
    kpt_tmp = 0.0
    for i in range(n_kpoints):  # profile[0]=180，Num K-point values
        if i == 0:
            kpt_tmp = 0
            k_x.append(kpt_tmp)  # k_x=[0]
        else:
            kpt_tmp = kpt_tmp + np.linalg.norm(kpts[i] - kpts[i - 1])
            k_x.append(kpt_tmp)
    # print(len(k_x))
    # Bands vertical coordinates
    k_y = []  # Total vertical coordinates
    k_y_k = []  # Each k points, 180 points, 16 bars
    for index, value in enumerate(n_band_rows):
        numbers = read_lines[value].split()[4]
        # print(index + 1)
        k_y_k.append(float(numbers))
        if (index + 1) % n_bands == 0 and index != 0:
            # print(index)
            k_y.append(k_y_k)
            k_y_k = []
        # break
    return total_band_atom, k_x, k_y, n_kpoints, n_bands
    # return atomic contribution, bands horizontal coordinates, bands vertical coordinates,k points, bands num


def readPROCAR1(fileName='PROCAR', orbital=-1):
    f = open(fileName)
    buffer = f.readlines()

    ''' # of k-points:   14         # of bands: 450         # of ions:  85 '''
    nKpt = int(re.search('(?<=# of k-points:)\s+\d+', buffer[1]).group(0))
    nBands = int(re.search('(?<=# of bands:)\s+\d+', buffer[1]).group(0))
    nIons = int(re.search('(?<=# of ions:)\s+\d+', buffer[1]).group(0))

    nOrbits = len(buffer[7].split()) - 1
    Proj = np.zeros((nKpt, nBands, nIons, nOrbits))
    Kpts = np.zeros((nKpt, 3))
    Eigs = np.zeros((nKpt, nBands))
    Occs = np.zeros((nKpt, nBands))

    kptInfoLength = 1
    for i in [line.find(' k-point') for line in buffer[3 + 1:]]:
        kptInfoLength -= i
        if i == 0: break

    for kpt in range(nKpt):
        # read k-th band projection to ion orbital
        # read k-point
        kptLineNum = 2 + 1 + kptInfoLength * kpt
        kptLine = buffer[kptLineNum]

        kVec = re.search('(?<=:)\s*([-]?[0-9]*\.?[0-9]+)\s*([-]?[0-9]*\.?[0-9]+)\s*([-]?[0-9]*\.?[0-9]+)', kptLine)
        kVec = np.array([float(kVec.group(1)), float(kVec.group(2)), float(kVec.group(3))])
        Kpts[kpt, :] = kVec

        kp_weight = float(re.search('(?<=weight =)\s*[-]?[0-9]*\.?[0-9]+', kptLine).group(0))

        bandInfoLength = 1
        for i in [line.find('band') for line in buffer[kptLineNum + 2 + 1:]]:
            bandInfoLength -= i
            if i == 0: break
        # print (bandInfoLength)

        for band in range(nBands):
            # bandLineNum = kptLineNum + 2 + band * (nIons *3 +6) #works for only non-S*L coupling
            bandLineNum = kptLineNum + 2 + band * bandInfoLength
            eig = float(re.search('(?<=energy)\s+[-]?[0-9]*\.?[0-9]+', buffer[bandLineNum]).group(0))
            occ = float(re.search('(?<=occ.)\s+[-]?[0-9]*\.?[0-9]+', buffer[bandLineNum]).group(0))

            Eigs[kpt, band] = eig
            Occs[kpt, band] = occ

            for ion in range(nIons):
                ionLineNum = bandLineNum + 3 + ion

                orbital_proj = [float(o) for o in buffer[ionLineNum].split()[1:]]
                Proj[kpt, band, ion, :] = orbital_proj

    return nKpt, nBands, nIons, Kpts, Eigs, Proj, Occs
    #返回k点数，能带条数，原子数，nKpt行3列的数组，


def get_reciprocal_lattice(fileName='CONTCAR'):
    lat_const, lat_mat, atomSetDirect = readCONTCAR(fileName)
    lat_mat = np.array(lat_mat) * lat_const

    rec_mat = np.empty((3, 3))

    for index in range(3):
        cross = np.cross(lat_mat[(index + 1) % 3], lat_mat[(index + 2) % 3])
        rec_mat[index, :] = cross / np.dot(lat_mat[index], cross)

    return rec_mat * 2. * np.pi


def readCONTCAR(fileName='CONTCAR', rtspecies=False):
    latticeVecs = []
    atomSet = []
    atomSetDirect = []
    sd = False
    f = open(fileName, 'r')
    # read first & second line
    f.readline()
    latConst = float(f.readline())
    # read lattice vectors
    latVec = np.array([float(i) * latConst for i in f.readline().split()])
    latticeVecs.append(latVec)
    latVec = np.array([float(i) * latConst for i in f.readline().split()])
    latticeVecs.append(latVec)
    latVec = np.array([float(i) * latConst for i in f.readline().split()])
    latticeVecs.append(latVec)

    # read species
    species = f.readline().split()
    numSpecies = [int(i) for i in f.readline().split()]

    line = f.readline().strip()

    if line == 'Selective dynamics':
        DorC = f.readline()
    else:
        DorC = line

    # read coordinate
    k = 0
    for symbol in species:
        for n in range(numSpecies[k]):
            coord = np.array([float(i) for i in f.readline().split()[:3]])

            atomSetDirect.append([symbol, coord])
            if DorC[0] == 'D' or DorC[0] == 'd':  # Direct
                coord = latticeVecs[0] * coord[0] + latticeVecs[1] * coord[1] + latticeVecs[2] * coord[2]
            else:
                print("check coord! it's not direct form")

            atomSet.append([symbol, coord])
        k += 1
    f.close()

    for i, latVec in enumerate(latticeVecs):
        latticeVecs[i] = latVec / latConst
    if rtspecies == True:
        return [latConst, latticeVecs, atomSetDirect, species]
    else:
        return [latConst, latticeVecs, atomSetDirect]


def readLOCPOT(fileName='LOCPOT'):
    return readCHGCAR(fileName)


def readCHGCAR(file_name='CHGCAR'):
    '''
    read CHGCAR
    '''
    import math
    VALUE_PER_LINE = 5
    with open(file_name) as chgcar_file:
        buffer = chgcar_file.readlines()
        lat_const = float(buffer[1])
        lattice_matrix = [[float(item) for item in line.split()]
                          for line in buffer[2:5]]
        n_atom = sum([int(i) for i in buffer[6].split()])
        grids = [int(grid) for grid in buffer[9 + n_atom].split()]

        value = [line for line in buffer[10 + n_atom:
                                         10 + n_atom + int(math.ceil(np.prod(grids) / VALUE_PER_LINE))]]
        # avoid read augmentation occupancy
        # value = list(itertools.takewhile(lambda line: 'augmentation' not in line, value))
        value = np.array([float(item) for line in value
                          for item in line.split()])
        CHGCAR = value.reshape(grids[::-1]).T

    return lat_const, lattice_matrix, CHGCAR


def readKPOINTS_linemode(fileName='KPOINTS'):
    f = open(fileName)
    buffer = f.readlines()
    f.close()
    comment = buffer[0]

    lables = []
    nkpt_line = int(buffer[1].split()[0])

    m = re.search('\s\w([-\s]\w)*$', comment)
    if False and m:
        special_kpoints = m.group(0).strip()
        # print (special_kpoints)
        for i, kpt in enumerate(special_kpoints):
            if kpt.isalpha() and not special_kpoints[i - 1] == ' ':
                lables.append(kpt)
            elif kpt == ' ':
                lables[-1] = lables[-1] + '|' + special_kpoints[i + 1]
    else:
        for line in buffer[4:]:
            # print (line)
            m = re.search('(?<=! )\s*[\\\$\w]+\s*$', line)
            if m:
                lables.append(m.group(0).strip())

        lables_merged = [lables[0]]
        for i in range(1, len(lables), 2):
            l_1 = lables[i]
            if i + 1 > len(lables) - 1 or lables[i] == lables[i + 1]:
                lables_merged.append(lables[i])
            else:
                lables_merged.append(lables[i] + '|' + lables[i + 1])

        lables = lables_merged
        for i, l in enumerate(lables):
            if 'G' in l:
                lables[i] = '$\Gamma$'
    return nkpt_line, lables


def readEIGENVAL(fileName='EIGENVAL', NELECT=False, lweight=False):
    # read EIGENVAL
    f = open(fileName)
    buffer = f.readlines()
    f.close()
    [nKpt, nBand] = [int(i) for i in buffer[5].split()][1:]
    n_elect = int(buffer[5].split()[0])
    # bandInfo = []
    kpoints = []
    weight = []
    eigenvals_1 = np.zeros((nKpt, nBand))
    eigenvals_2 = np.zeros((nKpt, nBand))
    panduan = buffer[0 + 8 + (nBand + 2) * 0].split()
    if len(panduan) == 2:
        for j in range(nKpt):
            kpoint = buffer[-1 + 8 + (nBand + 2) * j].split()[-4:-1]
            kpoint = np.array([float(k) for k in kpoint])
            kpoints.append(kpoint)
            weight.append(float(buffer[-1 + 8 + (nBand + 2) * j].split()[-1]))

            for i in range(nBand):
                eigenval = buffer[i + 8 + (nBand + 2) * j].split()
                eigenval_1 = float(eigenval[1])
                eigenvals_1[j, i] = eigenval_1
        returns = len(panduan), eigenvals_1
    if len(panduan) == 3:
        for j in range(nKpt):
            kpoint = buffer[-1 + 8 + (nBand + 2) * j].split()[-4:-1]
            kpoint = np.array([float(k) for k in kpoint])
            kpoints.append(kpoint)
            weight.append(float(buffer[-1 + 8 + (nBand + 2) * j].split()[-1]))

            for i in range(nBand):
                eigenval = buffer[i + 8 + (nBand + 2) * j].split()
                eigenval_1 = float(eigenval[1])
                eigenvals_1[j, i] = eigenval_1
                eigenval_2 = float(eigenval[2])
                eigenvals_2[j, i] = eigenval_2
        returns = len(panduan), eigenvals_1, eigenvals_2
    return returns


def readDOSCAR(fileName, atomNum):
    f = open(fileName)  # d打开DOSCAR文件
    data = f.readlines()  # 读取整个文件所有行，保存在一个列表(list)变量中，每行作为一个元素,2723行
    f.close()
    numAtom = data[0]  # DOSCAR第一行   8   8   1   0
    numAtom = numAtom.split()  # 指定分隔符对字符串进行切片,返回列表
    numAtom = int(numAtom[0])  # 返回列表第一个元素转整数型 8

    '''
    read PDOS
    '''
    '''go to data of atom selected'''  # 转到选定原子的数据

    # eSet = []
    # sDOSSet = []
    # pDOSSet = []
    # dDOSSet = []

    head = data[5].split()  # 第6行分割
    numRow = int(head[2])  # 行数，第六行第3个数301
    fermiE = float(head[3])  # 费米能，第6行第4个数-4.34441556

    eSet = []
    tDOSSet = []
    iDOSSet = []
    '''read total dos'''  # 阅读全部dos
    for i in range(6, 6 + numRow):  # 第7行开始到第6+301行，numRow=301
        row = data[i].split()  # 把每一行分割得到列表['-26.535', '0.0000E+00', '0.0000E+00']
        e = float(row[0]) - fermiE  # 能量，第一个数减费米能
        tDOS = float(row[1])  # 列表的第2个元素
        iDOS = float(row[2])  # 列表的第3个元素
        # 把每行(301行)都读取添加
        eSet.append(e)
        tDOSSet.append(tDOS)
        iDOSSet.append(iDOS)
    tDOSSet = np.array(tDOSSet)  # 列表转数组
    iDOSSet = np.array(iDOSSet)
    ''' read average pdos or specific atom pdos '''  # 读取平均pdos或特定的原子pdos
    if atomNum > 0:
        atomSet = [atomNum]
    else:
        atomSet = range(numAtom)

    ''' read pdos  '''
    sDOSSetSum = np.zeros(numRow)  # 创建元素为0的数组，numRow=301
    p_yDOSSetSum = np.zeros(numRow)
    p_zDOSSetSum = np.zeros(numRow)
    p_xDOSSetSum = np.zeros(numRow)
    d_xyDOSSetSum = np.zeros(numRow)
    d_yzDOSSetSum = np.zeros(numRow)
    d_z2DOSSetSum = np.zeros(numRow)
    d_xzDOSSetSum = np.zeros(numRow)
    d_x2_y2DOSSetSum = np.zeros(numRow)
    for atomNum_i in range(numAtom):  # numAtom=8，从0-7
        # eSet=[]
        sDOSSet = []
        p_yDOSSet = []
        p_zDOSSet = []
        p_xDOSSet = []
        d_xyDOSSet = []
        d_yzDOSSet = []
        d_z2DOSSet = []
        d_xzDOSSet = []
        d_x2_y2DOSSet = []
        sRow = 5 + (atomNum_i + 1) * (numRow + 1)  # 5+(0+1)*(301+1)
        # 307,609,911,1213,1515,1817,2119,2421
        head = data[sRow].split()

        # print('numRow',numRow)

        for i in range(sRow + 1, sRow + 1 + numRow):
            row = data[i].split()
            # e=float(row[0])-fermiE
            sDOS = float(row[1])  # s轨道
            p_yDOS = float(row[2])  # p_y轨道
            p_zDOS = float(row[3])
            p_xDOS = float(row[4])
            d_xyDOS = float(row[5])
            d_yzDOS = float(row[6])
            d_z2DOS = float(row[7])
            d_xzDOS = float(row[8])
            d_x2_y2DOS = float(row[9])
            # eSet.append(e)
            sDOSSet.append(sDOS)
            p_yDOSSet.append(p_yDOS)
            p_zDOSSet.append(p_zDOS)
            p_xDOSSet.append(p_xDOS)
            d_xyDOSSet.append(d_xyDOS)
            d_yzDOSSet.append(d_yzDOS)
            d_z2DOSSet.append(d_z2DOS)
            d_xzDOSSet.append(d_xzDOS)
            d_x2_y2DOSSet.append(d_x2_y2DOS)
        sDOSSetSum += np.array(sDOSSet)
        p_yDOSSetSum += np.array(p_yDOSSet)
        p_zDOSSetSum += np.array(p_zDOSSet)
        p_xDOSSetSum += np.array(p_xDOSSet)
        d_xyDOSSetSum += np.array(d_xyDOSSet)
        d_yzDOSSetSum += np.array(d_yzDOSSet)
        d_z2DOSSetSum += np.array(d_z2DOSSet)
        d_xzDOSSetSum += np.array(d_xzDOSSet)
        d_x2_y2DOSSetSum += np.array(d_x2_y2DOSSet)
    # print (numRow)
    sDOSSet = sDOSSetSum
    p_yDOSSet = p_yDOSSetSum
    p_zDOSSet = p_zDOSSetSum
    p_xDOSSet = p_xDOSSetSum
    d_xyDOSSet = d_xyDOSSetSum
    d_yzDOSSet = d_yzDOSSetSum
    d_z2DOSSet = d_z2DOSSetSum
    d_xzDOSSet = d_xzDOSSetSum
    d_x2_y2DOSSet = d_x2_y2DOSSetSum

    eSet = np.array(eSet)

    return [eSet, tDOSSet, iDOSSet, sDOSSet, p_yDOSSet, p_zDOSSet, p_xDOSSet,
            d_xyDOSSet, d_yzDOSSet, d_z2DOSSet, d_xzDOSSet, d_x2_y2DOSSet]


def writePOSCAR(output, latConst, latticeVecs, atomSetDirect, lSelective=False, lDirect=True):
    species = [atom[0] for atom in atomSetDirect]
    species1 = list(set(species))
    species1.sort(key=species.index)
    species = species1

    f = open(output, 'w')
    f.write('system\n')
    f.write(str(latConst) + '\n')

    for latticeVec in latticeVecs:
        for i in range(3):
            f.write(str(latticeVec[i]) + ' ')
        f.write('\n')

    for s in species:
        f.write(s + ' ')
    f.write('\n')

    for s in species:
        n = len([atom for atom in atomSetDirect if atom[0] == s])
        f.write(str(n) + ' ')
    f.write('\n')

    if lSelective: f.write('Selective dynamics\n')
    if lDirect:
        f.write('Direct\n')
    else:
        f.write('Cartesian\n')
    for atom in atomSetDirect:
        f.write(str(atom[1][0]) + ' ' + str(atom[1][1]) + ' ' + str(atom[1][2]) + ' ')
        if lSelective:
            # print (lSelective)
            f.write(str(atom[2][0]) + ' ' + str(atom[2][1]) + ' ' + str(atom[2][2]) + ' ')
        f.write('\n')

    f.close()


def getNELECT(OUTCAR):
    '   NELECT =     338.0000    total number of electrons'
    nelect = findReg('(?<=NELECT =)\s+\d+', OUTCAR)
    return int(nelect[0])


def getVBM(EIGENVAL, band_no=0):
    if band_no == 0:
        band_no = getNELECT('OUTCAR') / 2
    eigenval = findReg('(?<=^' + str(band_no).rjust(5) + ')\s+[-]?[0-9]*\.?[0-9]+', EIGENVAL)
    vbm = [float(e) for e in eigenval]
    vbm = max(vbm)
    return vbm


def getCBM(EIGENVAL, band_no=0):
    if band_no == 0:
        band_no = getNELECT('OUTCAR') / 2 + 1
    eigenval = findReg('(?<=^' + str(band_no).rjust(5) + ')\s+[-]?[0-9]*\.?[0-9]+', EIGENVAL)
    cbm = [float(e) for e in eigenval]
    cbm = min(cbm)
    return cbm


def getEgap(OUTCAR, EIGENVAL):
    n_elect = getNELECT(OUTCAR)
    vbm = getVBM(EIGENVAL, n_elect / 2)
    cbm = getCBM(EIGENVAL, n_elect / 2 + 1)
    egap = cbm - vbm
    return egap


def getTotE(OSZICAR):
    ' 1 F= -.54010511E+03 E0= -.54010511E+03  d E =-.786584E-14'
    energy = findReg('(?<=F=)\s+[-+]?[0-9]*\.?[0-9]+[eE][-+]?[0-9]+? ', OSZICAR)
    totE = [float(e) for e in energy]
    totE = totE[len(totE) - 1]
    return totE


def get_tot_E_outcar(outcar, enthalpy=None):
    # get total energy from line of outcar
    '  free  energy   TOTEN  =       -53.472728 eV'
    '''
    FREE ENERGIE OF THE ION-ELECTRON SYSTEM (eV)
    ---------------------------------------------------
    free  energy   TOTEN  =      -178.22800012 eV

    energy  without entropy=     -178.22769568  energy(sigma->0) =     -178.22789864
    enthalpy is  TOTEN    =      -153.45223930 eV   P V=       24.77576082
    '''
    if not enthalpy:
        for line in outcar:
            enthalpy = 'enthalpy' in line
            if enthalpy:
                break
    if enthalpy:
        reg = '(?<=enthalpy is  TOTEN)\s*=\s+[-+]?[0-9]*\.?[0-9]+'
    else:
        reg = '(?<=free  energy   TOTEN)\s*=\s+[-+]?[0-9]*\.?[0-9]+'
    find = []
    for line in outcar:
        m = re.findall(reg, line)
        find += m
    tot_E = float(find[-1].replace('=', ''))
    return tot_E


def readOUTCAR(OUTCAR='OUTCAR'):
    f = open(OUTCAR, 'r')
    outcar = f.readlines()
    f.close()
    return outcar


def writeOUTCAR(outcar, output_file='OUTCAR'):
    f = open(output_file, 'w')
    f.writelines(outcar)
    f.close()


def get_enthalpy(dir_name):
    outcar = readOUTCAR('{}/OUTCAR' % dir_name)
    # get total energy from line of outcar
    '  free  energy   TOTEN  =       -53.472728 eV'
    reg = '(?<=TOTEN  =)\s+[-+]?[0-9]*\.?[0-9]+'
    find = []
    for line in outcar:
        m = re.findall(reg, line)
        find += m
    tot_E = float(find[-1])
    return tot_E


def get_eps(OUTCAR='./OUTCAR'):
    """
    return diagonal component of macroscopic dielectric constant
    """
    reg = '(?<=diag\[e\(oo\)\]=\()\s+([\d\.\-]+\s+){3}'
    try:
        with open(OUTCAR) as outcar:
            data = []
            for line in outcar.readlines():
                m = re.search(reg, line)
                if m is not None:
                    # print (m.group(1).split())
                    data += m.group().split()
        eps = []
        for item in data:
            if '-' not in item:
                eps.append(float(item))
        eps = [item for idx, item in enumerate(eps) if idx % 2 == 0]
        return eps
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
        return None


if __name__ == '__main__':
    path = '../01_bulk/111/00_000/'
    eps = get_eps('{}/OUTCAR'.format(path))
    gap = getEgap('{}/00_SCF/OUTCAR'.format(path), '{}/00_SCF/EIGENVAL'.format(path))
    print(eps)
    print(gap)
