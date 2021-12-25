import sys, re
import os
from threading import Thread
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.QtCore import QDir
from abinitostudio.ui.UI_vasp_scf import Ui_Form_UI_vasp_scf
from abinitostudio.ui.UI_vasp_scf_noncal import Ui_Form_UI_vasp_scf_noncal
from abinitostudio.ui.UI_vasp_band import Ui_Form_UI_vasp_band
from abinitostudio.ui.UI_vasp_band_noncal import Ui_Form_UI_vasp_band_noncal
from abinitostudio.ui.UI_vasp_DOS import Ui_Form_UI_vasp_DOS
from abinitostudio.ui.UI_vasp_phonon import Ui_Form_UI_vasp_phonon
from abinitostudio.ui.UI_vasp_wannier import Ui_Form_UI_vasp_wannier


import time
from pathlib import Path

import paramiko
import socket


class Vasp_calculation():
    def __init__(self):
        self.remote_session = None
        self.output = None
        self.local_path = None
        self.node_path = None
        self.get_ip_info = None
        self.code_path = None
        self.tran_cal_vasp = False

    def set_order_connection(self):
        hostname = socket.gethostname()
        my_ip = socket.gethostbyname(hostname)

        self.vm = paramiko.SSHClient()
        self.vm.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.vm.connect(self.jumpnodeip, username=self.jumpnodeuser, password=self.jumpnodepass)
        #
        vmtransport = self.vm.get_transport()
        dest_addr = (self.nodeip, 22)  # edited#
        local_addr = (my_ip, 22)  # edited#
        vmchannel = vmtransport.open_channel("direct-tcpip", dest_addr, local_addr)
        #
        self.order_session = paramiko.SSHClient()
        self.order_session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # jhost.load_host_keys('/home/osmanl/.ssh/known_hosts') #disabled#
        self.order_session.connect(self.nodeip, username=self.nodeuser, password=self.nodepass, sock=vmchannel)

    def close_order_connection(self):
        self.order_session.close()
        self.vm.close()

    def get_ip_information(self, jumpnodeip, jumpnodeuser, jumpnodepass, nodeip, nodeuser, nodepass):
        self.jumpnodeip = jumpnodeip
        self.jumpnodeuser = jumpnodeuser
        self.jumpnodepass = jumpnodepass

        self.nodeip = nodeip
        self.nodeuser = nodeuser
        self.nodepass = nodepass

    def set_output(self, text_output):
        self.output = text_output

    def set_struc(self, struc):
        self.struc = struc

    def set_connection(self, remote_node, have_connected):
        self.remote_session = remote_node
        self.get_ip_info = have_connected

    def set_path(self, local, node, code):
        self.local_path = local
        self.node_path = node
        self.code_path = code

    def write_file_vasp(self, filename, filetext):
        with open(filename, 'w') as f:
            f.write(filetext)

    def transport_file(self, filename, cal_path):
        file_path = cal_path + '\\' + filename
        des = self.node_path + '/' + filename
        self.remote_session.put(file_path, des)

    def transport_pos(self, cal_path):
        # transport file POSCAR
        try:
            self.transport_file('POSCAR', cal_path)
        except:
            self.output.append("POSCAR can't be found or tranported!!")
            sys.exit()

    def transport_cal_vasp(self):
        # transport file cal_vasp_single.py
        program_dir = 'scripts'
        code_path = self.code_path
        py_path = os.path.join(code_path, program_dir)
        file_path_cal_vasp_single = py_path + r'\cal_vasp_single.py'
        des_cal_vasp_single = self.node_path + r'/cal_vasp_single.py'
        self.remote_session.put(file_path_cal_vasp_single, des_cal_vasp_single)
        self.tran_cal_vasp = True

    def wait_to_finish(self, process):
        flag = 0
        found = False
        while True:
            time.sleep(60)
            flag = flag + 1
            print(flag)

            cal_path = self.node_path + '/' + self.cal_path_name + '/calculation.dat'
            # print(cal_path)
            path_exist = self.remote_session.exists(cal_path)
            if path_exist:
                win = self.local_path + '\\' + 'calculation.dat'
                # print(win)
                self.remote_session.get(remote_path=cal_path, local_path=win)
                with open(win, 'r') as foo:
                    for line in foo.readlines():
                        # print(line)
                        if process in line:
                            found = True
            if found:
                break

    # Calculation
    def scf_calculation(self):
        def scf_run():  # Tasks that need to open up new threads
            if not self.tran_cal_vasp:
                self.transport_cal_vasp()

            win_path = os.path.join(self.local_path, self.cal_path_name)
            if not os.path.exists(win_path):
                os.mkdir(win_path)

            # Change current working directory to self.local_path
            os.chdir(win_path)
            self.struc.structure.to(fmt='poscar', filename=win_path + '\\POSCAR')
            self.transport_pos(win_path)

            if self.scf_relax:
                self.write_file_vasp('INCAR_relax', self.rel_INCAR)
                self.transport_file('INCAR_relax', win_path)
                self.write_file_vasp('KPOINTS_relax', self.rel_KPOINTS)
                self.transport_file('KPOINTS_relax', win_path)

            # scf
            self.write_file_vasp('INCAR_scf', self.scf_INCAR)
            self.transport_file('INCAR_scf', win_path)
            self.write_file_vasp('KPOINTS_scf', self.scf_KPOINTS)
            self.transport_file('KPOINTS_scf', win_path)

            order1 = 'cd ' + self.node_path + '; '
            order2 = "python cal_vasp_single.py "
            order_npr = 'npr=' + self.np_wannier + ' '
            order_vasp = 'vasp=' + self.vasp_order + ' '
            order_psdir = 'psdir=' + self.POTCAR_path + ' '
            order_listps = "listps=" + "\'" + self.elements + "\'" + ' '
            order_caldir = "cal_dir=" + self.cal_path_name + ' '
            if self.scf_relax:
                order3 = 'relax=1 scf=1 '
            else:
                order3 = 'relax=0 scf=1'
            order_all = order1 + order2 + order_npr + order_vasp + order_psdir + order_listps + order_caldir + order3
            print(order_all)
            self.output.append("The calculation is started")
            QApplication.processEvents()

            self.set_order_connection()
            stdin, stdout, stderr = self.order_session.exec_command(order_all, get_pty=False)
            self.close_order_connection()
            self.wait_to_finish('scf_finished!')
            self.output.append("The calculation is ended")
            QApplication.processEvents()

            if not os.path.exists(os.path.join(self.local_path, self.cal_path_name, "scf")):
                os.mkdir(os.path.join(self.local_path, self.cal_path_name, "scf"))
            eigfile = self.node_path + '/' + self.cal_path_name + '/scf/CHGCAR'
            print(eigfile)
            win = self.local_path + '\\' + self.cal_path_name + '\\scf\\' + 'CHGCAR'

            self.remote_session.get(remote_path=eigfile, local_path=win)
            self.output.append("Task completed, vasp_scf file returned")
            QApplication.processEvents()

        scf_thread = Thread(target=scf_run, args=())  # Instantiate a thread
        scf_thread.start()  # Start thread

    def band_calculation(self):
        def band_run():
            if not self.tran_cal_vasp:
                self.transport_cal_vasp()

            win_path = os.path.join(self.local_path, self.cal_path_name)
            if not os.path.exists(win_path):
                os.mkdir(win_path)

            # Change current working directory to self.local_path
            os.chdir(win_path)
            self.struc.structure.to(fmt='poscar', filename=win_path + '\\POSCAR')
            self.transport_pos(win_path)

            # Writing VASP files and transport files
            if self.band_relax:  # relax is or not True
                self.write_file_vasp('INCAR_relax', self.rel_INCAR)
                self.transport_file('INCAR_relax', win_path)
                self.write_file_vasp('KPOINTS_relax', self.rel_KPOINTS)
                self.transport_file('KPOINTS_relax', win_path)
            # scf
            self.write_file_vasp('INCAR_scf', self.scf_INCAR)
            self.transport_file('INCAR_scf', win_path)
            self.write_file_vasp('KPOINTS_scf', self.scf_KPOINTS)
            self.transport_file('KPOINTS_scf', win_path)
            # band
            self.write_file_vasp('INCAR_band', self.band_INCAR)
            self.transport_file('INCAR_band', win_path)
            self.write_file_vasp('KPOINTS_band', self.band_KPOINTS)
            self.transport_file('KPOINTS_band', win_path)
            # order
            order1 = 'cd ' + self.node_path + '; '
            order2 = "python cal_vasp_single.py "
            order_npr = 'npr=' + self.np_wannier + ' '
            order_vasp = 'vasp=' + self.vasp_order + ' '
            order_psdir = 'psdir=' + self.POTCAR_path + ' '
            order_listps = "listps=" + "\'" + self.elements + "\'" + ' '
            order_caldir = "cal_dir=" + self.cal_path_name + ' '
            if self.band_relax:
                order3 = 'relax=1 scf=1 band=1'
            else:
                order3 = 'scf=1 band=1'
            order_all = order1 + order2 + order_npr + order_vasp + order_psdir + order_listps + order_caldir + order3
            print(order_all)
            self.output.append("The calculation is started")
            QApplication.processEvents()
            self.set_order_connection()
            stdin, stdout, stderr = self.order_session.exec_command(order_all, get_pty=False)
            self.close_order_connection()
            self.wait_to_finish('band_finished!')
            self.output.append("The calculation is ended")
            QApplication.processEvents()

            if not os.path.exists(os.path.join(self.local_path, self.cal_path_name, "band")):
                os.mkdir(os.path.join(self.local_path, self.cal_path_name, "band"))
            eigfile = self.node_path + '/' + self.cal_path_name + '/band/EIGENVAL'
            win = self.local_path + '\\' + self.cal_path_name + '\\band\\' + 'EIGENVAL'
            print(eigfile, win)
            self.remote_session.get(remote_path=eigfile, local_path=win)
            self.output.append("Task completed, vasp_band file returned")
            QApplication.processEvents()

        band_thread = Thread(target=band_run, args=())
        band_thread.start()

    def dos_calculation(self):
        def dos_run():
            if not self.tran_cal_vasp:
                self.transport_cal_vasp()

            win_path = os.path.join(self.local_path, self.cal_path_name)
            if not os.path.exists(win_path):
                os.mkdir(win_path)

            # Change current working directory to self.local_path
            os.chdir(win_path)
            self.struc.structure.to(fmt='poscar', filename=win_path + '\\POSCAR')
            self.transport_pos(win_path)
            # Writing VASP files and transport files
            if self.dos_relax:  # relax is or not True
                self.write_file_vasp('INCAR_relax', self.rel_INCAR)
                self.transport_file('INCAR_relax', win_path)
                self.write_file_vasp('KPOINTS_relax', self.rel_KPOINTS)
                self.transport_file('KPOINTS_relax', win_path)
            # scf
            self.write_file_vasp('INCAR_scf', self.scf_INCAR)
            self.transport_file('INCAR_scf', win_path)
            self.write_file_vasp('KPOINTS_scf', self.scf_KPOINTS)
            self.transport_file('KPOINTS_scf', win_path)
            # dos_scf
            self.write_file_vasp('INCAR_dos', self.scf_INCAR)
            self.transport_file('INCAR_dos', win_path)
            self.write_file_vasp('KPOINTS_dos', self.scf_KPOINTS)
            self.transport_file('KPOINTS_dos', win_path)
            # order
            order1 = 'cd ' + self.node_path + '; '
            order2 = "python cal_vasp_single.py "
            order_npr = 'npr=' + self.np_wannier + ' '
            order_vasp = 'vasp=' + self.vasp_order + ' '
            order_psdir = 'psdir=' + self.POTCAR_path + ' '
            order_listps = "listps=" + "\'" + self.elements + "\'" + ' '
            order_caldir = "cal_dir=" + self.cal_path_name + ' '
            if self.dos_relax:
                order3 = 'relax=1 scf=1 dos=1'
            else:
                order3 = 'scf=1 dos=1'
            order_all = order1 + order2 + order_npr + order_vasp + order_psdir + order_listps + order_caldir + order3
            print(order_all)
            self.output.append("The calculation is started")
            QApplication.processEvents()
            self.set_order_connection()
            stdin, stdout, stderr = self.order_session.exec_command(order_all, get_pty=False)
            self.close_order_connection()
            self.wait_to_finish('dos_finished!')
            self.output.append("The calculation is ended")
            QApplication.processEvents()
            if not os.path.exists(os.path.join(self.local_path, self.cal_path_name, "dos")):
                os.mkdir(os.path.join(self.local_path, self.cal_path_name, "dos"))
            eigfile = self.node_path + '/' + self.cal_path_name + '/dos/DOSCAR'
            win = self.local_path + '\\' + self.cal_path_name + '\\dos\\' + 'DOSCAR'
            print(eigfile, win)
            self.remote_session.get(remote_path=eigfile, local_path=win)
            self.output.append("Task completed, vasp_band file returned")
            QApplication.processEvents()

        dos_thread = Thread(target=dos_run, args=())
        dos_thread.start()

    def phonon_calculation(self):
        def phonon_run():
            if not self.tran_cal_vasp:
                self.transport_cal_vasp()

            win_path = os.path.join(self.local_path, self.cal_path_name)
            if not os.path.exists(win_path):
                os.mkdir(win_path)

            # Change current working directory to self.local_path
            os.chdir(win_path)
            self.struc.structure.to(fmt='poscar', filename=win_path + '\\POSCAR')
            self.transport_pos(win_path)

            # Writing VASP files and transport files
            self.write_file_vasp('INCAR_phonon_relax', self.rel_INCAR_relax)
            self.transport_file('INCAR_phonon_relax', win_path)
            self.write_file_vasp('KPOINTS_phonon_relax', self.rel_KPOINTS_relax)
            self.transport_file('KPOINTS_phonon_relax', win_path)
            # phonon
            self.write_file_vasp('INCAR_phonon', self.rel_INCAR_phonon)
            self.transport_file('INCAR_phonon', win_path)
            self.write_file_vasp('KPOINTS_phonon', self.rel_KPOINTS_phonon)
            self.transport_file('KPOINTS_phonon', win_path)
            # order
            order1 = 'cd ' + self.node_path + '; '
            order2 = "python cal_vasp_single.py "
            order_npr = 'npr=' + self.np_wannier + ' '
            order_vasp = 'vasp=' + self.vasp_order + ' '
            order_psdir = 'psdir=' + self.POTCAR_path + ' '
            order_listps = "listps=" + "\'" + self.elements + "\'" + ' '
            order_caldir = "cal_dir=" + self.cal_path_name + ' '
            order_path = "kpath_phonon=" + self.kp_path + ' '
            order_supercell = 'dim=' + self.supercell + ' '
            order3 = 'phonon=1'
            order_all = order1 + order2 + order_npr + order_vasp + order_psdir + \
                        order_listps + order_caldir + order_path + order_supercell + order3
            self.output.append("The calculation is started")
            QApplication.processEvents()
            print(order_all)
            self.set_order_connection()
            stdin, stdout, stderr = self.order_session.exec_command(order_all, get_pty=False)
            self.close_order_connection()
            self.wait_to_finish('phonon_finished!')
            self.output.append("The calculation is ended")
            QApplication.processEvents()

            if not os.path.exists(os.path.join(self.local_path, self.cal_path_name, "phonon")):
                os.mkdir(os.path.join(self.local_path, self.cal_path_name, "phonon"))
            eigfile = self.node_path + '/' + self.cal_path_name + '/phonon/band.dat'
            win = self.local_path + '\\' + self.cal_path_name + '\\phonon\\' + 'band.dat'
            self.remote_session.get(remote_path=eigfile, local_path=win)
            eigfile = self.node_path + '/' + self.cal_path_name + '/phonon/band.pdf'
            win = self.local_path + '\\' + self.cal_path_name + '\\phonon\\' + 'band.pdf'
            self.remote_session.get(remote_path=eigfile, local_path=win)
            self.output.append("Task completed, vasp_phonon file returned")
            QApplication.processEvents()

        phonon_thread = Thread(target=phonon_run, args=())
        phonon_thread.start()

    def wannier_calculation(self):
        def wannier_run():
            if not self.tran_cal_vasp:
                self.transport_cal_vasp()

            win_path = os.path.join(self.local_path, self.cal_path_name)
            if not os.path.exists(win_path):
                os.mkdir(win_path)

            # Change current working directory to self.local_path
            os.chdir(win_path)
            self.struc.structure.to(fmt='poscar', filename=win_path + '\\POSCAR')
            self.transport_pos(win_path)
            # scf
            self.write_file_vasp('INCAR_wan', self.scf_INCAR)
            self.transport_file('INCAR_wan', win_path)
            self.write_file_vasp('KPOINTS_wan', self.scf_KPOINTS)
            self.transport_file('KPOINTS_wan', win_path)
            # band
            self.write_file_vasp('wannier90.win', self.wannier90_win)
            self.transport_file('wannier90.win', win_path)
            # order
            order1 = 'cd ' + self.node_path + '; '
            order2 = "python cal_vasp_single.py "
            order_npr = 'npr=' + self.np_wannier + ' '
            order_vasp = 'vasp=' + self.vasp_order + ' '
            order_psdir = 'psdir=' + self.POTCAR_path + ' '
            order_listps = "listps=" + "\'" + self.elements + "\'" + ' '
            order_caldir = "cal_dir=" + self.cal_path_name + ' '
            order3 = 'wan=1 wan_type=normal '
            order_all = order1 + order2 + order_npr + order_vasp + order_psdir + order_listps + order_caldir + order3
            self.output.append("The calculation is started")
            QApplication.processEvents()
            self.set_order_connection()
            stdin, stdout, stderr = self.order_session.exec_command(order_all, get_pty=False)
            self.close_order_connection()
            self.wait_to_finish('wan_finished!')
            self.output.append("The calculation is ended")
            QApplication.processEvents()

            if not os.path.exists(os.path.join(self.local_path, self.cal_path_name, "wan")):
                os.mkdir(os.path.join(self.local_path, self.cal_path_name, "wan"))
            eigfile = self.node_path + '/' + self.cal_path_name + '/wan/wannier90_band.dat'
            win = self.local_path + '\\' + self.cal_path_name + '\\wan\\' + 'wannier90_band.dat'
            print(eigfile, win)
            self.remote_session.get(remote_path=eigfile, local_path=win)
            self.output.append("Task completed, vasp_wan file returned")
            QApplication.processEvents()

        wannier_thread = Thread(target=wannier_run, args=())
        wannier_thread.start()

    # Vasp
    def vasp_scf(self):
        self.dialog_vasp_scf = Vasp_table_scf()
        # dialog.setModal(True)  # Set modal window
        self.dialog_vasp_scf.show()

        self.scf_relax = False

        # get scf parameter
        def vasp_scf_get_par():
            if self.dialog_vasp_scf.checkBox.checkState() == 2:
                self.scf_relax = True
            # relax
            self.rel_INCAR = self.dialog_vasp_scf.textEdit.toPlainText()
            self.rel_KPOINTS = self.dialog_vasp_scf.textEdit_2.toPlainText()
            # scf
            self.scf_INCAR = self.dialog_vasp_scf.textEdit_13.toPlainText()
            self.scf_KPOINTS = self.dialog_vasp_scf.textEdit_14.toPlainText()
            #
            self.POTCAR_path = self.dialog_vasp_scf.lineEdit.text()
            self.elements = self.dialog_vasp_scf.lineEdit_2.text()
            self.cal_path_name = self.dialog_vasp_scf.lineEdit_3.text()
            self.vasp_order = self.dialog_vasp_scf.lineEdit_4.text()
            self.np_wannier = self.dialog_vasp_scf.lineEdit_5.text()
            # judge relax
            if self.scf_relax:
                print("Structure relax")
            else:
                print("No need for structural relax")
            # run function
            self.dialog_vasp_scf.close()
            self.output.append("Sent vasp_scf task")
            QApplication.processEvents()

        # read scf parameter
        def vasp_scf_read_par():
            txt_path = os.path.join(self.code_path, r'default/scf.txt')
            node_info_path = Path(txt_path)
            # print(txt_path)
            if node_info_path.is_file():
                data = open(txt_path, 'r')
                lines = data.readlines()
                data_str = ''
                for line in lines:
                    data_str = data_str + line
                scf_relax_INCAR = re.findall(r'# relax_INCAR\n([\s\S]*)# relax_KPOINTS', data_str)
                scf_relax_KPOINTS = re.findall(r'# relax_KPOINTS\n([\s\S]*)# scf_INCAR', data_str)
                scf_scf_INCAR = re.findall(r'# scf_INCAR\n([\s\S]*)# scf_KPOINTS', data_str)
                scf_scf_KPOINTS = re.findall(r'# scf_KPOINTS\n([\s\S]*)# POTCAR_path', data_str)
                scf_POTCAR_path = re.findall(r'# POTCAR_path\n([\s\S]*)# Elements_order', data_str)
                scf_Elements_order = re.findall(r'# Elements_order\n([\s\S]*)# Calculation_path', data_str)
                scf_Calculation_path = re.findall(r'# Calculation_path\n([\s\S]*)# VASP_command', data_str)
                scf_VASP_command = re.findall(r'# VASP_command\n([\s\S]*)# Number_of_task_cores', data_str)
                scf_Number_of_task_cores = re.findall(r'# Number_of_task_cores\n([\s\S]*)', data_str)
                self.dialog_vasp_scf.textEdit.setText(scf_relax_INCAR[0])
                self.dialog_vasp_scf.textEdit_2.setText(scf_relax_KPOINTS[0])
                self.dialog_vasp_scf.textEdit_13.setText(scf_scf_INCAR[0])
                self.dialog_vasp_scf.textEdit_14.setText(scf_scf_KPOINTS[0])
                self.dialog_vasp_scf.lineEdit.setText(scf_POTCAR_path[0].replace('\n', '').replace('\r', ''))
                self.dialog_vasp_scf.lineEdit_2.setText(scf_Elements_order[0].replace('\n', '').replace('\r', ''))
                self.dialog_vasp_scf.lineEdit_3.setText(scf_Calculation_path[0].replace('\n', '').replace('\r', ''))
                self.dialog_vasp_scf.lineEdit_4.setText(scf_VASP_command[0].replace('\n', '').replace('\r', ''))
                self.dialog_vasp_scf.lineEdit_5.setText(scf_Number_of_task_cores[0].replace('\n', '').replace('\r', ''))

        self.dialog_vasp_scf.pushButton_2.clicked.connect(vasp_scf_get_par)
        self.dialog_vasp_scf.pushButton_2.clicked.connect(self.scf_calculation)
        self.dialog_vasp_scf.pushButton_3.clicked.connect(vasp_scf_read_par)
        self.dialog_vasp_scf.exec_()

    def vasp_scf_noncal(self):
        self.dialog_vasp_scf_noncal = Vasp_table_scf_noncal()
        # dialog.setModal(True)  # Set modal window
        self.dialog_vasp_scf_noncal.show()

        # get scf_noncal parameter
        def vasp_scf_noncal_get_par():
            # relax
            self.rel_INCAR = self.dialog_vasp_scf_noncal.textEdit.toPlainText()
            self.rel_KPOINTS = self.dialog_vasp_scf_noncal.textEdit_2.toPlainText()
            # scf
            self.scf_INCAR = self.dialog_vasp_scf_noncal.textEdit_13.toPlainText()
            self.scf_KPOINTS = self.dialog_vasp_scf_noncal.textEdit_14.toPlainText()
            #
            self.POTCAR_path = self.dialog_vasp_scf_noncal.lineEdit.text()
            self.elements = self.dialog_vasp_scf_noncal.lineEdit_2.text()
            self.cal_path_name = self.dialog_vasp_scf_noncal.lineEdit_3.text()
            self.vasp_order = self.dialog_vasp_scf_noncal.lineEdit_4.text()
            self.np_wannier = self.dialog_vasp_scf_noncal.lineEdit_5.text()
            # judge relax
            if self.dialog_vasp_scf_noncal.checkBox.checkState() == 2:
                print("Structure relax")
                self.scf_relax = True
            else:
                print("No need for structural relax")
            # run function
            pass
            self.dialog_vasp_scf_noncal.close()
            self.output.append("Sent vasp_scf_noncal task")
            QApplication.processEvents()

        # read scf_noncal parameter
        def vasp_scf_noncal_read_par():
            txt_path = os.path.join(self.code_path, r'default/scf_noncal.txt')
            node_info_path = Path(txt_path)
            if node_info_path.is_file():
                data = open(txt_path, 'r')
                lines = data.readlines()
                data_str = ''
                for line in lines:
                    data_str = data_str + line
                scf_noncal_relax_INCAR = re.findall(r'# relax_INCAR\n([\s\S]*)# relax_KPOINTS', data_str)
                scf_noncal_relax_KPOINTS = re.findall(r'# relax_KPOINTS\n([\s\S]*)# scf_INCAR', data_str)
                scf_noncal_scf_INCAR = re.findall(r'# scf_INCAR\n([\s\S]*)# scf_KPOINTS', data_str)
                scf_noncal_scf_KPOINTS = re.findall(r'# scf_KPOINTS\n([\s\S]*)# POTCAR_path', data_str)
                scf_noncal_POTCAR_path = re.findall(r'# POTCAR_path\n([\s\S]*)# Elements_order', data_str)
                scf_noncal_Elements_order = re.findall(r'# Elements_order\n([\s\S]*)# Calculation_path', data_str)
                scf_noncal_Calculation_path = re.findall(r'# Calculation_path\n([\s\S]*)# VASP_command', data_str)
                scf_noncal_VASP_command = re.findall(r'# VASP_command\n([\s\S]*)# Number_of_task_cores', data_str)
                scf_noncal_Number_of_task_cores = re.findall(r'# Number_of_task_cores\n([\s\S]*)', data_str)
                self.dialog_vasp_scf_noncal.textEdit.setText(scf_noncal_relax_INCAR[0])
                self.dialog_vasp_scf_noncal.textEdit_2.setText(scf_noncal_relax_KPOINTS[0])
                self.dialog_vasp_scf_noncal.textEdit_13.setText(scf_noncal_scf_INCAR[0])
                self.dialog_vasp_scf_noncal.textEdit_14.setText(scf_noncal_scf_KPOINTS[0])
                self.dialog_vasp_scf_noncal.lineEdit.setText(
                    scf_noncal_POTCAR_path[0].replace('\n', '').replace('\r', ''))
                self.dialog_vasp_scf_noncal.lineEdit_2.setText(
                    scf_noncal_Elements_order[0].replace('\n', '').replace('\r', ''))
                self.dialog_vasp_scf_noncal.lineEdit_3.setText(
                    scf_noncal_Calculation_path[0].replace('\n', '').replace('\r', ''))
                self.dialog_vasp_scf_noncal.lineEdit_4.setText(
                    scf_noncal_VASP_command[0].replace('\n', '').replace('\r', ''))
                self.dialog_vasp_scf_noncal.lineEdit_5.setText(
                    scf_noncal_Number_of_task_cores[0].replace('\n', '').replace('\r', ''))

        self.dialog_vasp_scf_noncal.pushButton_2.clicked.connect(vasp_scf_noncal_get_par)
        self.dialog_vasp_scf_noncal.pushButton_2.clicked.connect(self.scf_calculation)
        self.dialog_vasp_scf_noncal.pushButton_3.clicked.connect(vasp_scf_noncal_read_par)
        self.dialog_vasp_scf_noncal.exec_()

    def vasp_band(self):
        self.dialog_vasp_band = Vasp_table_band()
        # dialog.setModal(True)  # Set modal window
        self.dialog_vasp_band.show()

        self.band_relax = False

        # get band parameter
        def vasp_band_get_par():
            # relax
            self.rel_INCAR = self.dialog_vasp_band.textEdit.toPlainText()
            self.rel_KPOINTS = self.dialog_vasp_band.textEdit_2.toPlainText()
            # scf
            self.scf_INCAR = self.dialog_vasp_band.textEdit_13.toPlainText()
            self.scf_KPOINTS = self.dialog_vasp_band.textEdit_14.toPlainText()
            # band
            self.band_INCAR = self.dialog_vasp_band.textEdit_19.toPlainText()
            self.band_KPOINTS = self.dialog_vasp_band.textEdit_20.toPlainText()
            #
            self.POTCAR_path = self.dialog_vasp_band.lineEdit.text()
            self.elements = self.dialog_vasp_band.lineEdit_2.text()
            self.cal_path_name = self.dialog_vasp_band.lineEdit_3.text()
            self.vasp_order = self.dialog_vasp_band.lineEdit_4.text()
            self.np_wannier = self.dialog_vasp_band.lineEdit_5.text()
            # judge relax
            if self.dialog_vasp_band.checkBox.checkState() == 2:
                print("Structral relax is turned on!")
                self.band_relax = True
            else:
                print("Structral relax is turned off!")
            self.dialog_vasp_band.close()
            self.output.append("Sent vasp_band task")
            QApplication.processEvents()

        # read band parameter
        def vasp_band_read_par():
            txt_path = os.path.join(self.code_path, r'default/band.txt')
            node_info_path = Path(txt_path)
            if node_info_path.is_file():
                data = open(txt_path, 'r')
                lines = data.readlines()
                data_str = ''
                for line in lines:
                    data_str = data_str + line
                band_relax_INCAR = re.findall(r'# relax_INCAR\n([\s\S]*)# relax_KPOINTS', data_str)
                band_relax_KPOINTS = re.findall(r'# relax_KPOINTS\n([\s\S]*)# scf_INCAR', data_str)
                band_scf_INCAR = re.findall(r'# scf_INCAR\n([\s\S]*)# scf_KPOINTS', data_str)
                band_scf_KPOINTS = re.findall(r'# scf_KPOINTS\n([\s\S]*)# band_INCAR', data_str)
                band_band_INCAR = re.findall(r'# band_INCAR\n([\s\S]*)# band_KPOINTS', data_str)
                band_band_KPOINTS = re.findall(r'# band_KPOINTS\n([\s\S]*)# POTCAR_path', data_str)
                band_POTCAR_path = re.findall(r'# POTCAR_path\n([\s\S]*)# Elements_order', data_str)
                band_Elements_order = re.findall(r'# Elements_order\n([\s\S]*)# Calculation_path', data_str)
                band_Calculation_path = re.findall(r'# Calculation_path\n([\s\S]*)# VASP_command', data_str)
                band_VASP_command = re.findall(r'# VASP_command\n([\s\S]*)# Number_of_task_cores', data_str)
                band_Number_of_task_cores = re.findall(r'# Number_of_task_cores\n([\s\S]*)', data_str)
                self.dialog_vasp_band.textEdit.setText(band_relax_INCAR[0])
                self.dialog_vasp_band.textEdit_2.setText(band_relax_KPOINTS[0])
                self.dialog_vasp_band.textEdit_13.setText(band_scf_INCAR[0])
                self.dialog_vasp_band.textEdit_14.setText(band_scf_KPOINTS[0])
                self.dialog_vasp_band.textEdit_19.setText(band_band_INCAR[0])
                self.dialog_vasp_band.textEdit_20.setText(band_band_KPOINTS[0])
                self.dialog_vasp_band.lineEdit.setText(band_POTCAR_path[0].replace('\n', '').replace('\r', ''))
                self.dialog_vasp_band.lineEdit_2.setText(band_Elements_order[0].replace('\n', '').replace('\r', ''))
                self.dialog_vasp_band.lineEdit_3.setText(band_Calculation_path[0].replace('\n', '').replace('\r', ''))
                self.dialog_vasp_band.lineEdit_4.setText(band_VASP_command[0].replace('\n', '').replace('\r', ''))
                self.dialog_vasp_band.lineEdit_5.setText(
                    band_Number_of_task_cores[0].replace('\n', '').replace('\r', ''))

        self.dialog_vasp_band.pushButton_2.clicked.connect(vasp_band_get_par)
        self.dialog_vasp_band.pushButton_2.clicked.connect(self.band_calculation)
        self.dialog_vasp_band.pushButton_3.clicked.connect(vasp_band_read_par)
        self.dialog_vasp_band.exec_()

    def vasp_band_noncal(self):
        print("vasp_band_noncal")
        self.dialog_vasp_band_noncal = Vasp_table_band_noncal()
        # dialog.setModal(True)  # Set modal window
        self.dialog_vasp_band_noncal.show()

        # get band_noncal parameter
        def vasp_band_noncal_get_par():
            # relax
            self.rel_INCAR = self.dialog_vasp_band_noncal.textEdit.toPlainText()
            self.rel_KPOINTS = self.dialog_vasp_band_noncal.textEdit_2.toPlainText()
            # scf
            self.scf_INCAR = self.dialog_vasp_band_noncal.textEdit_13.toPlainText()
            self.scf_KPOINTS = self.dialog_vasp_band_noncal.textEdit_14.toPlainText()
            # band
            self.band_INCAR = self.dialog_vasp_band_noncal.textEdit_19.toPlainText()
            self.band_KPOINTS = self.dialog_vasp_band_noncal.textEdit_20.toPlainText()
            #
            self.POTCAR_path = self.dialog_vasp_band_noncal.lineEdit.text()
            self.elements = self.dialog_vasp_band_noncal.lineEdit_2.text()
            self.cal_path_name = self.dialog_vasp_band_noncal.lineEdit_3.text()
            self.vasp_order = self.dialog_vasp_band_noncal.lineEdit_4.text()
            self.np_wannier = self.dialog_vasp_band_noncal.lineEdit_5.text()
            # judge relax
            if self.dialog_vasp_band_noncal.checkBox.checkState() == 2:
                print("Structure relax")
            else:
                print("No need for structural relax")
            # run function
            pass
            self.dialog_vasp_band_noncal.close()
            self.output.append("Sent vasp_band_noncal task")
            QApplication.processEvents()

        # read band_noncal parameter
        def vasp_band_noncal_read_par():
            txt_path = os.path.join(self.code_path, r'default/band_noncal.txt')
            node_info_path = Path(txt_path)
            if node_info_path.is_file():
                data = open(txt_path, 'r')
                lines = data.readlines()
                data_str = ''
                for line in lines:
                    data_str = data_str + line
                band_noncal_relax_INCAR = re.findall(r'# relax_INCAR\n([\s\S]*)# relax_KPOINTS', data_str)
                band_noncal_relax_KPOINTS = re.findall(r'# relax_KPOINTS\n([\s\S]*)# scf_INCAR', data_str)
                band_noncal_scf_INCAR = re.findall(r'# scf_INCAR\n([\s\S]*)# scf_KPOINTS', data_str)
                band_noncal_scf_KPOINTS = re.findall(r'# scf_KPOINTS\n([\s\S]*)# band_INCAR', data_str)
                band_noncal_band_INCAR = re.findall(r'# band_INCAR\n([\s\S]*)# band_KPOINTS', data_str)
                band_noncal_band_KPOINTS = re.findall(r'# band_KPOINTS\n([\s\S]*)# POTCAR_path', data_str)
                band_noncal_POTCAR_path = re.findall(r'# POTCAR_path\n([\s\S]*)# Elements_order', data_str)
                band_noncal_Elements_order = re.findall(r'# Elements_order\n([\s\S]*)# Calculation_path', data_str)
                band_noncal_Calculation_path = re.findall(r'# Calculation_path\n([\s\S]*)# VASP_command', data_str)
                band_noncal_VASP_command = re.findall(r'# VASP_command\n([\s\S]*)# Number_of_task_cores', data_str)
                band_noncal_Number_of_task_cores = re.findall(r'# Number_of_task_cores\n([\s\S]*)', data_str)
                self.dialog_vasp_band_noncal.textEdit.setText(band_noncal_relax_INCAR[0])
                self.dialog_vasp_band_noncal.textEdit_2.setText(band_noncal_relax_KPOINTS[0])
                self.dialog_vasp_band_noncal.textEdit_13.setText(band_noncal_scf_INCAR[0])
                self.dialog_vasp_band_noncal.textEdit_14.setText(band_noncal_scf_KPOINTS[0])
                self.dialog_vasp_band_noncal.textEdit_19.setText(band_noncal_band_INCAR[0])
                self.dialog_vasp_band_noncal.textEdit_20.setText(band_noncal_band_KPOINTS[0])
                self.dialog_vasp_band_noncal.lineEdit.setText(
                    band_noncal_POTCAR_path[0].replace('\n', '').replace('\r', ''))
                self.dialog_vasp_band_noncal.lineEdit_2.setText(
                    band_noncal_Elements_order[0].replace('\n', '').replace('\r', ''))
                self.dialog_vasp_band_noncal.lineEdit_3.setText(
                    band_noncal_Calculation_path[0].replace('\n', '').replace('\r', ''))
                self.dialog_vasp_band_noncal.lineEdit_4.setText(
                    band_noncal_VASP_command[0].replace('\n', '').replace('\r', ''))
                self.dialog_vasp_band_noncal.lineEdit_5.setText(
                    band_noncal_Number_of_task_cores[0].replace('\n', '').replace('\r', ''))

        self.dialog_vasp_band_noncal.pushButton_2.clicked.connect(vasp_band_noncal_get_par)
        self.dialog_vasp_band_noncal.pushButton_2.clicked.connect(self.band_calculation)
        self.dialog_vasp_band_noncal.pushButton_3.clicked.connect(vasp_band_noncal_read_par)
        self.dialog_vasp_band_noncal.exec_()

    def vasp_DOS(self):
        print("vasp_DOS")
        self.dialog_vasp_DOS = Vasp_table_DOS()
        # dialog.setModal(True)  # Set modal window
        self.dialog_vasp_DOS.show()

        self.dos_relax = False

        # get DOS parameter
        def vasp_DOS_get_par():
            # relax
            self.rel_INCAR = self.dialog_vasp_DOS.textEdit.toPlainText()
            self.rel_KPOINTS = self.dialog_vasp_DOS.textEdit_2.toPlainText()
            # scf
            self.scf_INCAR = self.dialog_vasp_DOS.textEdit_13.toPlainText()
            self.scf_KPOINTS = self.dialog_vasp_DOS.textEdit_14.toPlainText()
            # band
            self.band_INCAR = self.dialog_vasp_DOS.textEdit_19.toPlainText()
            self.band_KPOINTS = self.dialog_vasp_DOS.textEdit_20.toPlainText()
            #
            self.POTCAR_path = self.dialog_vasp_DOS.lineEdit.text()
            self.elements = self.dialog_vasp_DOS.lineEdit_2.text()
            self.cal_path_name = self.dialog_vasp_DOS.lineEdit_3.text()
            self.vasp_order = self.dialog_vasp_DOS.lineEdit_4.text()
            self.np_wannier = self.dialog_vasp_DOS.lineEdit_5.text()
            # judge relax
            if self.dialog_vasp_DOS.checkBox.checkState() == 2:
                self.dos_relax = True
                print("Structure relax")
            else:
                print("No need for structural relax")
            # run function

            self.dialog_vasp_DOS.close()
            self.output.append("Sent vasp_DOS task")
            QApplication.processEvents()

        # read DOS parameter
        def vasp_DOS_read_par():
            txt_path = os.path.join(self.code_path, r'default/DOS.txt')
            node_info_path = Path(txt_path)
            if node_info_path.is_file():
                data = open(txt_path, 'r')
                lines = data.readlines()
                data_str = ''
                for line in lines:
                    data_str = data_str + line
                DOS_relax_INCAR = re.findall(r'# relax_INCAR\n([\s\S]*)# relax_KPOINTS', data_str)
                DOS_relax_KPOINTS = re.findall(r'# relax_KPOINTS\n([\s\S]*)# scf_INCAR', data_str)
                DOS_scf_INCAR = re.findall(r'# scf_INCAR\n([\s\S]*)# scf_KPOINTS', data_str)
                DOS_scf_KPOINTS = re.findall(r'# scf_KPOINTS\n([\s\S]*)# DOS_INCAR', data_str)
                DOS_band_INCAR = re.findall(r'# DOS_INCAR\n([\s\S]*)# DOS_KPOINTS', data_str)
                DOS_band_KPOINTS = re.findall(r'# DOS_KPOINTS\n([\s\S]*)# POTCAR_path', data_str)
                DOS_POTCAR_path = re.findall(r'# POTCAR_path\n([\s\S]*)# Elements_order', data_str)
                DOS_Elements_order = re.findall(r'# Elements_order\n([\s\S]*)# Calculation_path', data_str)
                DOS_Calculation_path = re.findall(r'# Calculation_path\n([\s\S]*)# VASP_command', data_str)
                DOS_VASP_command = re.findall(r'# VASP_command\n([\s\S]*)# Number_of_task_cores', data_str)
                DOS_Number_of_task_cores = re.findall(r'# Number_of_task_cores\n([\s\S]*)', data_str)
                self.dialog_vasp_DOS.textEdit.setText(DOS_relax_INCAR[0])
                self.dialog_vasp_DOS.textEdit_2.setText(DOS_relax_KPOINTS[0])
                self.dialog_vasp_DOS.textEdit_13.setText(DOS_scf_INCAR[0])
                self.dialog_vasp_DOS.textEdit_14.setText(DOS_scf_KPOINTS[0])
                self.dialog_vasp_DOS.textEdit_19.setText(DOS_band_INCAR[0])
                self.dialog_vasp_DOS.textEdit_20.setText(DOS_band_KPOINTS[0])
                self.dialog_vasp_DOS.lineEdit.setText(DOS_POTCAR_path[0].replace('\n', '').replace('\r', ''))
                self.dialog_vasp_DOS.lineEdit_2.setText(DOS_Elements_order[0].replace('\n', '').replace('\r', ''))
                self.dialog_vasp_DOS.lineEdit_3.setText(DOS_Calculation_path[0].replace('\n', '').replace('\r', ''))
                self.dialog_vasp_DOS.lineEdit_4.setText(DOS_VASP_command[0].replace('\n', '').replace('\r', ''))
                self.dialog_vasp_DOS.lineEdit_5.setText(DOS_Number_of_task_cores[0].replace('\n', '').replace('\r', ''))

        self.dialog_vasp_DOS.pushButton_2.clicked.connect(vasp_DOS_get_par)
        self.dialog_vasp_DOS.pushButton_2.clicked.connect(self.dos_calculation)
        self.dialog_vasp_DOS.pushButton_3.clicked.connect(vasp_DOS_read_par)
        self.dialog_vasp_DOS.exec_()

    def vasp_phonon(self):
        print("vasp_phonon")
        self.dialog_vasp_phonon = Vasp_table_phonon()
        # dialog.setModal(True)  # Set modal window
        self.dialog_vasp_phonon.show()

        # get phonon parameter
        def vasp_phonon_get_par():
            # relax
            self.rel_INCAR_relax = self.dialog_vasp_phonon.textEdit.toPlainText()
            self.rel_KPOINTS_relax = self.dialog_vasp_phonon.textEdit_2.toPlainText()
            # phonon
            self.rel_INCAR_phonon = self.dialog_vasp_phonon.textEdit_3.toPlainText()
            self.rel_KPOINTS_phonon = self.dialog_vasp_phonon.textEdit_4.toPlainText()
            #
            self.POTCAR_path = self.dialog_vasp_phonon.lineEdit.text()
            self.elements = self.dialog_vasp_phonon.lineEdit_2.text()
            self.cal_path_name = self.dialog_vasp_phonon.lineEdit_3.text()
            self.vasp_order = self.dialog_vasp_phonon.lineEdit_4.text()
            self.np_wannier = self.dialog_vasp_phonon.lineEdit_5.text()
            self.kp_path = self.dialog_vasp_phonon.lineEdit_6.text()
            self.supercell = self.dialog_vasp_phonon.lineEdit_8.text()
            self.dialog_vasp_phonon.close()
            self.output.append("Sent vasp_phonon task")
            QApplication.processEvents()

        # read phonon parameter
        def vasp_phonon_read_par():
            txt_path = os.path.join(self.code_path, r'default/phonon.txt')
            node_info_path = Path(txt_path)
            if node_info_path.is_file():
                data = open(txt_path, 'r')
                lines = data.readlines()
                data_str = ''
                for line in lines:
                    data_str = data_str + line
                phonon_relax_INCAR = re.findall(r'# relax_INCAR\n([\s\S]*)# relax_KPOINTS', data_str)
                phonon_relax_KPOINTS = re.findall(r'# relax_KPOINTS\n([\s\S]*)# phonon_INCAR', data_str)
                phonon_INCAR = re.findall(r'# phonon_INCAR\n([\s\S]*)# phonon_KPOINTS', data_str)
                phonon_KPOINTS = re.findall(r'# phonon_KPOINTS\n([\s\S]*)# POTCAR_path', data_str)
                phonon_POTCAR_path = re.findall(r'# POTCAR_path\n([\s\S]*)# Elements_order', data_str)
                phonon_Elements_order = re.findall(r'# Elements_order\n([\s\S]*)# Calculation_path', data_str)
                phonon_Calculation_path = re.findall(r'# Calculation_path\n([\s\S]*)# VASP_command', data_str)
                phonon_VASP_command = re.findall(r'# VASP_command\n([\s\S]*)# Number_of_task_cores', data_str)
                phonon_Number_of_task_cores = re.findall(r'# Number_of_task_cores\n([\s\S]*)# K-Path：', data_str)
                phonon_K_Path = re.findall(r'# K-Path：\n([\s\S]*)# Supercell', data_str)
                phonon_Supercell = re.findall(r'# Supercell\n([\s\S]*)', data_str)
                self.dialog_vasp_phonon.textEdit.setText(phonon_relax_INCAR[0])
                self.dialog_vasp_phonon.textEdit_2.setText(phonon_relax_KPOINTS[0])
                self.dialog_vasp_phonon.textEdit_3.setText(phonon_INCAR[0])
                self.dialog_vasp_phonon.textEdit_4.setText(phonon_KPOINTS[0])
                self.dialog_vasp_phonon.lineEdit.setText(phonon_POTCAR_path[0].replace('\n', '').replace('\r', ''))
                self.dialog_vasp_phonon.lineEdit_2.setText(phonon_Elements_order[0].replace('\n', '').replace('\r', ''))
                self.dialog_vasp_phonon.lineEdit_3.setText(
                    phonon_Calculation_path[0].replace('\n', '').replace('\r', ''))
                self.dialog_vasp_phonon.lineEdit_4.setText(phonon_VASP_command[0].replace('\n', '').replace('\r', ''))
                self.dialog_vasp_phonon.lineEdit_5.setText(
                    phonon_Number_of_task_cores[0].replace('\n', '').replace('\r', ''))
                self.dialog_vasp_phonon.lineEdit_6.setText(phonon_K_Path[0].replace('\n', '').replace('\r', ''))
                self.dialog_vasp_phonon.lineEdit_8.setText(phonon_Supercell[0].replace('\n', '').replace('\r', ''))

        self.dialog_vasp_phonon.pushButton_2.clicked.connect(vasp_phonon_get_par)
        self.dialog_vasp_phonon.pushButton_2.clicked.connect(self.phonon_calculation)
        self.dialog_vasp_phonon.pushButton_3.clicked.connect(vasp_phonon_read_par)
        self.dialog_vasp_phonon.exec_()

    def vasp_wannier(self):
        print("vasp_wannier")
        self.dialog_vasp_wannier = Vasp_table_wannier()
        # dialog.setModal(True)  # Set modal window
        self.dialog_vasp_wannier.show()

        # get wannier parameter
        def vasp_wannier_get_par():
            self.INCAR = self.dialog_vasp_wannier.textEdit.toPlainText()
            self.KPOINTS = self.dialog_vasp_wannier.textEdit_2.toPlainText()
            self.wannier90_win = self.dialog_vasp_wannier.textEdit_3.toPlainText()
            #
            self.POTCAR_path = self.dialog_vasp_wannier.lineEdit.text()
            self.elements = self.dialog_vasp_wannier.lineEdit_2.text()
            self.cal_path_name = self.dialog_vasp_wannier.lineEdit_3.text()
            self.vasp_order = self.dialog_vasp_wannier.lineEdit_4.text()
            self.np_wannier = self.dialog_vasp_wannier.lineEdit_5.text()
            # run function
            pass
            self.dialog_vasp_wannier.close()
            self.output.append("Sent vasp_wannier task")
            QApplication.processEvents()

        # read wannier parameter
        def vasp_wannier_read_par():
            txt_path = os.path.join(self.code_path, r'default/wannier.txt')
            node_info_path = Path(txt_path)
            if node_info_path.is_file():
                data = open(txt_path, 'r')
                lines = data.readlines()
                data_str = ''
                for line in lines:
                    data_str = data_str + line
                wannier_ready_INCAR = re.findall(r'# ready_INCAR\n([\s\S]*)# ready_KPOINTS', data_str)
                wannier_ready_KPOINTS = re.findall(r'# ready_KPOINTS\n([\s\S]*)# wannier90_win', data_str)
                wannier_wannier90_win = re.findall(r'# wannier90_win\n([\s\S]*)# POTCAR_path', data_str)
                wannier_POTCAR_path = re.findall(r'# POTCAR_path\n([\s\S]*)# Elements_order', data_str)
                wannier_Elements_order = re.findall(r'# Elements_order\n([\s\S]*)# Calculation_path', data_str)
                wannier_Calculation_path = re.findall(r'# Calculation_path\n([\s\S]*)# VASP_command', data_str)
                wannier_VASP_command = re.findall(r'# VASP_command\n([\s\S]*)# Number_of_task_cores', data_str)
                wannier_Number_of_task_cores = re.findall(r'# Number_of_task_cores\n([\s\S]*)', data_str)
                self.dialog_vasp_wannier.textEdit.setText(wannier_ready_INCAR[0])
                self.dialog_vasp_wannier.textEdit_2.setText(wannier_ready_KPOINTS[0])
                self.dialog_vasp_wannier.textEdit_3.setText(wannier_wannier90_win[0])
                self.dialog_vasp_wannier.lineEdit.setText(wannier_POTCAR_path[0].replace('\n', '').replace('\r', ''))
                self.dialog_vasp_wannier.lineEdit_2.setText(
                    wannier_Elements_order[0].replace('\n', '').replace('\r', ''))
                self.dialog_vasp_wannier.lineEdit_3.setText(
                    wannier_Calculation_path[0].replace('\n', '').replace('\r', ''))
                self.dialog_vasp_wannier.lineEdit_4.setText(wannier_VASP_command[0].replace('\n', '').replace('\r', ''))
                self.dialog_vasp_wannier.lineEdit_5.setText(
                    wannier_Number_of_task_cores[0].replace('\n', '').replace('\r', ''))

        self.dialog_vasp_wannier.pushButton_2.clicked.connect(vasp_wannier_get_par)
        self.dialog_vasp_wannier.pushButton_2.clicked.connect(self.wannier_calculation)
        self.dialog_vasp_wannier.pushButton_3.clicked.connect(vasp_wannier_read_par)
        self.dialog_vasp_wannier.exec_()




# Setting VASP Dialog
class Vasp_table_scf(QDialog, Ui_Form_UI_vasp_scf):
    def __init__(self):
        super(Vasp_table_scf, self).__init__()
        self.setupUi(self)
        # self.resize(1500, 1000)


class Vasp_table_scf_noncal(QDialog, Ui_Form_UI_vasp_scf_noncal):
    def __init__(self):
        super(Vasp_table_scf_noncal, self).__init__()
        self.setupUi(self)
        # self.resize(1500, 1000)


class Vasp_table_band(QDialog, Ui_Form_UI_vasp_band):
    def __init__(self):
        super(Vasp_table_band, self).__init__()
        self.setupUi(self)
        # self.resize(1500, 1000)


class Vasp_table_band_noncal(QDialog, Ui_Form_UI_vasp_band_noncal):
    def __init__(self):
        super(Vasp_table_band_noncal, self).__init__()
        self.setupUi(self)
        # self.resize(1500, 1000)


class Vasp_table_DOS(QDialog, Ui_Form_UI_vasp_DOS):
    def __init__(self):
        super(Vasp_table_DOS, self).__init__()
        self.setupUi(self)
        # self.resize(1500, 1000)


class Vasp_table_phonon(QDialog, Ui_Form_UI_vasp_phonon):
    def __init__(self):
        super(Vasp_table_phonon, self).__init__()
        self.setupUi(self)
        # self.resize(1500, 1000)


class Vasp_table_wannier(QDialog, Ui_Form_UI_vasp_wannier):
    def __init__(self):
        super(Vasp_table_wannier, self).__init__()
        self.setupUi(self)
        # self.resize(1500, 1000)



