import sys, os, re, ase.io.vasp
from pathlib import Path
from pyxtal import pyxtal
from jumpssh import SSHSession
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5 import QtWidgets
from PyQt5.QtCore import QDir
from PyQt5.QtGui import QDragEnterEvent
from PyQt5.QtWidgets import QDesktopWidget, QDialog, QMainWindow, QMessageBox, \
    QWidget, QVBoxLayout, QColorDialog, QFileDialog, QApplication
from traits.api import HasTraits, Instance, on_trait_change
from traitsui.api import View, Item
from mayavi.core.ui.api import MayaviScene, MlabSceneModel, SceneEditor
from abinitostudio.calculation.vasp_calculation import Vasp_calculation
from abinitostudio.plot.plot_calculation import Plot_calculation
from abinitostudio.plot.plot_vasp import plot_CHGCAR
from abinitostudio.structure.plot_structure import structure_plot
from abinitostudio.ui import UI
from abinitostudio.ui.UI_pyxtal import Ui_Form_UI_pyxtal
from abinitostudio.ui.UI_setting import Ui_Form_UI_setting
from abinitostudio.ui.UI_lattice import Ui_Lattice
from abinitostudio.ui.UI_structure import Ui_structure
from abinitostudio.ui.UI_download import Ui_Form_UI_download
from abinitostudio.ui.UI_introduction import Ui_Form_UI_introduction
from abinitostudio.structure.abinito_structure import abinito_structrue
import numpy as np
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
import paramiko
import socket
import webbrowser

# Global Variables
pos_path = ''


class MainWindow(QMainWindow, Plot_calculation):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = UI.Ui_MainWindow()
        self.ui.setupUi(self)
        self.center()  # Window centering
        # Splitter control scale
        self.ui.splitter.setStretchFactor(0, 1)
        self.ui.splitter.setStretchFactor(1, 1)
        self.ui.splitter_2.setStretchFactor(0, 3)
        self.ui.splitter_2.setStretchFactor(1, 2)
        # Mayavi window
        self.mayavi_widget = MayaviQWidget()  # Instantiate the MayaviQWidget class
        self.scene = self.mayavi_widget.visualization.scene
        self.ui.verticalLayout_2.addWidget(self.mayavi_widget)
        # Matplotlib drawing
        self.plt_pattern = Figure_Canvas(self, width=5, height=4, dpi=100)
        self.axes = self.plt_pattern.fig.add_subplot(111)
        self.plt_toolbar = NavigationToolbar(self.plt_pattern, self)
        self.__cid = self.plt_pattern.mpl_connect("scroll_event", self.do_scrollZoom)  # Mouse scrolling zoom
        self.ui.verticalLayout.addWidget(self.plt_toolbar)
        self.ui.verticalLayout.addWidget(self.plt_pattern)
        # Turn on drag-and-drop events
        self.setAcceptDrops(True)
        self.ui.textBrowser.setAcceptDrops(True)
        # File
        self.ui.actionvisual.triggered.connect(self.load_POSCAR)
        self.ui.actionbuild.triggered.connect(self.build_structure)
        # Calculation_Pyxtal
        self.ui.actiontest.triggered.connect(self.pyxtal)
        # Calculation_VASP
        self.ui.actionscf.triggered.connect(lambda: self.calculation_vasp_interface('scf'))
        self.ui.actionscf_noncal.triggered.connect(lambda: self.calculation_vasp_interface('scf_noncal'))
        self.ui.actionbands.triggered.connect(lambda: self.calculation_vasp_interface('band'))
        self.ui.actionband_noncal.triggered.connect(lambda: self.calculation_vasp_interface('band_noncal'))
        self.ui.actionDOS.triggered.connect(lambda: self.calculation_vasp_interface('dos'))
        self.ui.actionphonon.triggered.connect(lambda: self.calculation_vasp_interface('phonon'))
        self.ui.actionwannier.triggered.connect(lambda: self.calculation_vasp_interface('wannier'))
        # Plot
        self.ui.actionband.triggered.connect(self.show_Dialog_bands)
        self.ui.actionprojectionband.triggered.connect(self.show_Dialog_PB)
        self.ui.actiondos.triggered.connect(self.show_Dialog_DOS)
        self.ui.actionchgcar2D.triggered.connect(self.show_Dialog_CHGCAR_2D)
        self.ui.actionchgcar3D.triggered.connect(self.show_Dialog_CHGCAR_3D)
        # Tools
        self.struc_plot = structure_plot(self.scene)
        self.struc_is_defined = False
        self.ui.actionsupercell.triggered.connect(self.struc_plot.build_supercell)
        self.ui.actiontype_of_cell.triggered.connect(self.adjust_lattice)
        self.ui.actiondownload.triggered.connect(self.download_vasp)
        # Settings
        self.ui.actionsetting.triggered.connect(self.setting)
        # Help
        self.ui.actioninstruction.triggered.connect(self.instruction)
        self.ui.actionabout.triggered.connect(self.about)
        # Move atom
        self.ui.actionup.triggered.connect(self.move_atom_up)
        self.ui.actiondown.triggered.connect(self.move_atom_down)
        self.ui.actionleft.triggered.connect(self.move_atom_left)
        self.ui.actionright.triggered.connect(self.move_atom_right)
        #
        self.code_path = os.getcwd()
        self.have_connected = False
        self.get_ip_info = False

    def adjust_lattice(self):
        if self.struc_is_defined:
            if self.get_ip_info:
                self.struc_adjust = Structure_Dialog()
                self.struc_adjust.show()

                def adjust():
                    # self.local_path = 'E:\python\project_1\my_project\AbinitoStudio_zhou\AbinitoStudio_1222\examples'
                    if self.struc_adjust.radioButton_2.isChecked() == True:
                        self.struc.structure = self.struc.structure.get_primitive_structure()
                        self.struc.structure.to(fmt='poscar', filename=self.local_path + '\\POSCAR')
                        self.plot_pos(self.local_path + '\\POSCAR')
                    if self.struc_adjust.radioButton.isChecked() == True:
                        SGA = SpacegroupAnalyzer(self.struc.structure)
                        self.struc.structure = SGA.get_conventional_standard_structure()
                        self.struc.structure.to(fmt='poscar', filename=self.local_path + '\\POSCAR')
                        self.plot_pos(self.local_path + '\\POSCAR')

                    self.struc_adjust.close()

                self.struc_adjust.pushButton.clicked.connect(adjust)  # Add button is clicked
                self.struc_adjust.exec_()
            else:
                self.warning_1()
        else:
            self.warning_4()

    # Insert to the last line
    def add_row(self):
        self.structure_table.tableWidget.insertRow(self.structure_table.tableWidget.rowCount())

    def romove_row(self):
        self.structure_table.tableWidget.removeRow(self.structure_table.tableWidget.currentRow())

    # Clear all data, not including header
    def clear_contents(self):
        self.structure_table.tableWidget.clearContents()

    def build_structure(self):
        self.structure_table = Lattice_Dialog()

        def show_parameters():
            print(f'space group：{self.space_group}')
            print(f'Lattice mode：{self.lattice_model}')
            print(f'Length{self.length_a}、{self.length_b}、{self.length_c}，'
                  f'Angle{self.angle_alpha}、{self.angle_beta}、{self.angle_gamma}')
            print(f'Matrix：\n{self.lattice_matrix}')
            print(f'Frac or Cart：{self.coordinate_model}')
            print(f'Element and positions{self.table_item}')

        # Get all parameters on the panel
        def get_parameters():
            # Space group
            self.space_group = self.structure_table.lineEdit.text()
            # Lattice input mode
            if self.structure_table.radioButton.isChecked() == True:
                self.lattice_model = 'lattice_coordinate'
            else:
                self.lattice_model = 'lattice_matrix'
            # Lattice length and angle
            self.length_a = self.structure_table.lineEdit_2.text()
            self.length_b = self.structure_table.lineEdit_3.text()
            self.length_c = self.structure_table.lineEdit_4.text()
            self.angle_alpha = self.structure_table.lineEdit_8.text()
            self.angle_beta = self.structure_table.lineEdit_9.text()
            self.angle_gamma = self.structure_table.lineEdit_10.text()
            # Lattice matrix
            self.lattice_matrix = np.array([[float(self.structure_table.lineEdit_11.text()),
                                             float(self.structure_table.lineEdit_12.text()),
                                             float(self.structure_table.lineEdit_13.text())],
                                            [float(self.structure_table.lineEdit_14.text()),
                                             float(self.structure_table.lineEdit_15.text()),
                                             float(self.structure_table.lineEdit_16.text())],
                                            [float(self.structure_table.lineEdit_17.text()),
                                             float(self.structure_table.lineEdit_18.text()),
                                             float(self.structure_table.lineEdit_19.text())]])
            # Coordinate input mode
            if self.structure_table.radioButton_4.isChecked() == True:
                self.coordinate_model = 'Fractional'
            else:
                self.coordinate_model = 'Cartesian'
            # Read tableWidget data
            num_row = self.structure_table.tableWidget.rowCount()
            num_col = self.structure_table.tableWidget.columnCount()
            self.table_item = []
            self.elem = []
            try:
                for i in range(num_row):
                    row_text = f"{i + 1} row："
                    row_list = []
                    elem_tmp = self.structure_table.tableWidget.item(i, 0).text()
                    self.elem.append(elem_tmp)
                    for j in range(1, num_col):
                        row_item = self.structure_table.tableWidget.item(i, j)
                        row_text = row_text + row_item.text()
                        row_list.append(float(row_item.text()))
                    self.table_item.append(row_list)
            except:
                print('Input information is available')
                self.table_item = []

            self.table_item = np.array(self.table_item)

            print(self.elem, self.table_item)

            self.struc = abinito_structrue()
            self.struc_is_defined = True
            if self.space_group.strip() != '':
                try:
                    spg = int(self.space_group)
                    self.struc.set_spacegroup(spg)
                except:
                    self.struc.set_spacegroup(spg)
            if self.structure_table.radioButton.isChecked() == True:
                lattice = self.struc.lattice_from_parameters(float(self.length_a),
                                                             float(self.length_b),
                                                             float(self.length_c),
                                                             float(self.angle_alpha),
                                                             float(self.angle_beta),
                                                             float(self.angle_gamma))
            else:
                lattice = self.lattice_matrix
            # print(lattice)
            if self.get_ip_info:
                try:
                    self.struc.build_structure(lattice,
                                               self.elem,
                                               self.table_item)
                    self.struc.structure.to(fmt='poscar', filename=self.local_path + '\\POSCAR')
                    self.plot_pos(self.local_path + '\\POSCAR')
                    # Printing parameters
                    show_parameters()
                    self.structure_table.close()
                except:
                    self.warning_3()
            else:
                self.warning_1()

        # dialog.setModal(True)  # Set modal window
        self.structure_table.show()
        self.structure_table.pushButton.clicked.connect(self.add_row)  # Add button is clicked
        self.structure_table.pushButton_4.clicked.connect(self.romove_row)  # Remove button is clicked
        self.structure_table.pushButton_3.clicked.connect(self.clear_contents)  # Clear button is clicked
        self.structure_table.pushButton_2.clicked.connect(get_parameters)  # Enter button is clicked
        self.structure_table.exec_()

    # Mobile atomic response event
    # self.lineEdit.text()
    def move_atom_up(self):
        print(f'Atom moves up {self.ui.doubleSpinBox.value()} unit')

    def move_atom_down(self):
        print(f'Atom moves dowm {self.ui.doubleSpinBox.value()} unit')

    def move_atom_left(self):
        print(f'Atom moves left {self.ui.doubleSpinBox.value()} unit')

    def move_atom_right(self):
        print(f'Atom moves right {self.ui.doubleSpinBox.value()} unit')

    def plot_pos(self, path):
        self.scene.scene_editor._tool_bar.setVisible(True)
        islattice = True
        supercell = (1, 1, 1)
        linecolor = (0, 0, 0)
        linesize = 0.03
        self.struc_plot.adjust_cell(islattice, supercell, linesize, linecolor)
        self.struc_plot.read_poscar(path)
        self.struc_plot.get_info_poscar()
        self.struc_plot.plot_str()

    # Drag events
    def dragEnterEvent(self, e: QDragEnterEvent):
        if e.mimeData().hasUrls():
            for url in e.mimeData().urls():
                self.ui.textBrowser.append("Open a POSCAR in the path: \n" + url.path()[1:] + "\n")
            filename = e.mimeData().urls()[0].path()[1:]
            full_path = url.path()[1:]
            basename, ext = os.path.splitext(os.path.basename(filename))
            # print(ext)
            # print(basename)
            if basename == 'POSCAR':
                global pos_path
                pos_path = filename
                self.struc = abinito_structrue()
                self.struc_is_defined = True
                self.struc.build_structure_from_file(full_path)
                self.plot_pos(full_path)

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, 'Message',
                                               'Are you sure you want to exit?',
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    # run test function
    def pyxtal_func(self):
        self.get_parm_pyxtal()
        my_crystal = pyxtal()
        path = self.path  # "C:\\Users\\Administrator\\Desktop"
        # my_crystal.from_random(2, 51, ['C', 'N'], [1, 3])
        my_crystal.from_random(self.dim, self.spa_group, self.ele_type, self.ele_num)
        ase_struc = my_crystal.to_ase()
        str_type = 'pos'
        filename = ''
        if str_type == 'pos':
            filename = path + '\\POSCAR'
            ase.io.vasp.write_vasp(filename, ase_struc, vasp5=True)
            # file_open = filename
        elif str_type == 'cif':
            filename = path + '\\case' + '.cif'
            ase_struc.write(filename, format='cif')
        self.load_POSCAR_direct()
        self.dialog_test.close()

    # get test parameter
    def get_parm_pyxtal(self):
        # If haven't this file directory, create a new one
        if not os.path.exists(self.dialog_test.lineEdit.text()):
            os.mkdir(self.dialog_test.lineEdit.text())
        self.path = self.dialog_test.lineEdit.text()  # Save file directory
        self.dim = int(self.dialog_test.lineEdit_2.text())  # Dimensions
        self.spa_group = int(self.dialog_test.lineEdit_3.text())  # Space group
        self.ele_type = eval(self.dialog_test.lineEdit_4.text())  # Element type
        self.ele_num = eval(self.dialog_test.lineEdit_5.text())  # Number of elements
        self.thickness = self.dialog_test.lineEdit_6.text()  # Thickness

    def pyxtal(self):
        self.dialog_test = Pyxtal_table()
        # get desktop path
        self.dialog_test.lineEdit.setText(os.path.join(os.path.expanduser('~'), "Desktop\\VASP_files"))
        # self.dialog_test.setModal(True)  # Set modal window
        self.dialog_test.show()
        self.dialog_test.pushButton.clicked.connect(self.pyxtal_func)
        self.ui.actionclose.triggered.connect(self.dialog_test.close)
        self.ui.textBrowser.append("A random structure have been produced.")
        self.dialog_test.exec_()

    # the POSCAR generated by test is opened directly
    def load_POSCAR_direct(self):
        path = self.path + "\\POSCAR"
        self.struc = abinito_structrue()
        self.struc_is_defined = True
        self.struc.build_structure_from_file(path)
        self.plot_pos(path)

    # 3D atomic structure
    def load_POSCAR(self):
        curPath = QDir.currentPath()  # Get the current directory of the system
        dlgTitle = "Choose a POSCAR"  # Dialog title
        filt = "All files(*.*);; Text files(*.txt);;figure files(*.jpg *.gif *.png)"  # File filters
        filename, filtUsed = QFileDialog.getOpenFileName(self, dlgTitle, curPath, filt)
        global pos_path
        pos_path = filename
        extractfileName = (os.path.basename(filename))[0:6]
        if extractfileName == "POSCAR":
            self.struc = abinito_structrue()
            self.struc_is_defined = True
            self.struc.build_structure_from_file(pos_path)
            self.plot_pos(filename)
            self.ui.textBrowser.append(f"Open a POSCAR in the path: \n{filename}")

    def get_ip_information(self):
        node_info_path = Path(r'default/node_information.txt')
        if node_info_path.is_file():
            cfile = open('default/node_information.txt', 'r')
            lines = cfile.readlines()

            ip_info = {}
            for i in range(len(lines)):
                tmpArr = lines[i].split(':', 1)
                if tmpArr[0].strip() == 'jump':
                    ip_info['jump'] = tmpArr[1].strip()
                elif tmpArr[0].strip() == 'jump_ip':
                    ip_info['jump_ip'] = tmpArr[1].strip()
                elif tmpArr[0].strip() == 'jump_username':
                    ip_info['jump_username'] = tmpArr[1].strip()
                elif tmpArr[0].strip() == 'jump_password':
                    ip_info['jump_password'] = tmpArr[1].strip()
                elif tmpArr[0].strip() == 'cal_ip':
                    ip_info['cal_ip'] = tmpArr[1].strip()
                elif tmpArr[0].strip() == 'cal_username':
                    ip_info['cal_username'] = tmpArr[1].strip()
                elif tmpArr[0].strip() == 'cal_password':
                    ip_info['cal_password'] = tmpArr[1].strip()
                elif tmpArr[0].strip() == 'remote_path':
                    ip_info['remote_path'] = tmpArr[1].strip()
                elif tmpArr[0].strip() == 'local_path':
                    ip_info['local_path'] = tmpArr[1].strip()
            # print(ip_info)
            cfile.close()
        else:
            ip_info = None
        return ip_info

    # Setting
    def setting(self):
        self.dialog_setting = Setting_table()

        # get setting parameter
        def setting_read_par():
            txt_path = os.path.join(self.code_path, r'default/node_information.txt')
            node_info_path = Path(txt_path)
            # print(txt_path)
            if node_info_path.is_file():
                data = open(txt_path, 'r')
                lines = data.readlines()
                data_str = ''
                for line in lines:
                    data_str = data_str + line
                set_jump_ip = re.findall(r'jump_ip：([\s\S]*?)\n', data_str)
                set_jump_username = re.findall(r'jump_username：([\s\S]*?)\n', data_str)
                set_jump_password = re.findall(r'jump_password：([\s\S]*?)\n', data_str)
                set_cal_ip = re.findall(r'cal_ip：([\s\S]*?)\n', data_str)
                set_cal_username = re.findall(r'cal_username：([\s\S]*?)\n', data_str)
                set_cal_password = re.findall(r'cal_password：([\s\S]*?)\n', data_str)
                set_remote_path = re.findall(r'remote_path：([\s\S]*?)\n', data_str)
                set_local_path = re.findall(r'local_path：([\s\S]*)', data_str)
                self.dialog_setting.lineEdit_6.setText(set_jump_ip[0].replace('\n', '').replace('\r', ''))
                self.dialog_setting.lineEdit_8.setText(set_jump_username[0].replace('\n', '').replace('\r', ''))
                self.dialog_setting.lineEdit_7.setText(set_jump_password[0].replace('\n', '').replace('\r', ''))
                self.dialog_setting.lineEdit.setText(set_cal_ip[0].replace('\n', '').replace('\r', ''))
                self.dialog_setting.lineEdit_2.setText(set_cal_username[0].replace('\n', '').replace('\r', ''))
                self.dialog_setting.lineEdit_3.setText(set_cal_password[0].replace('\n', '').replace('\r', ''))
                self.dialog_setting.lineEdit_4.setText(set_remote_path[0].replace('\n', '').replace('\r', ''))
                # self.dialog_setting.lineEdit_5.setText(set_local_path[0].replace('\n', '').replace('\r', ''))
                self.dialog_setting.lineEdit_5.setText(os.path.join(os.path.expanduser('~'), "Desktop\\VASP_files"))
            else:
                self.ui.textBrowser.append('node_information.txt can\'t be found. '
                                           'Please input the node information manually!!!')

        if self.get_ip_info:
            self.recover_ip_information()

        # dialog.setModal(True)  # Set modal window
        self.dialog_setting.show()
        self.dialog_setting.pushButton.clicked.connect(self.setting_func)
        self.dialog_setting.pushButton_2.clicked.connect(setting_read_par)
        self.dialog_setting.exec_()

    # run setting function
    def setting_func(self):
        self.setting_parameter()
        # if os.path.exists(os.path.join(os.path.expanduser('~'), "Desktop\\VASP_files")):
        if os.path.exists(self.local_path):
            if self.dialog_setting.checkBox.checkState() == 2:
                try:
                    self.gateway_session = SSHSession(self.jumpnodeip,
                                                      username=self.jumpnodeuser,
                                                      password=self.jumpnodepass).open()
                    self.remote_session = self.gateway_session.get_remote_session(self.nodeip,
                                                                                  username=self.nodeuser,
                                                                                  password=self.nodepass)
                except:
                    self.warning_2()
            else:
                try:
                    self.remote_session = SSHSession(self.nodeip,
                                                     username=self.nodeuser,
                                                     password=self.nodepass).open()
                    self.ui.textBrowser.append("Node connection successful.")
                except:
                    self.ui.textBrowser.append("Node connection failed.")
                    self.warning_2()

            hostname = socket.gethostname()
            my_ip = socket.gethostbyname(hostname)

            vm = paramiko.SSHClient()
            vm.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            vm.connect(self.jumpnodeip, username=self.jumpnodeuser, password=self.jumpnodepass)
            #
            vmtransport = vm.get_transport()
            dest_addr = (self.nodeip, 22)  # edited#
            local_addr = (my_ip, 22)  # edited#
            vmchannel = vmtransport.open_channel("direct-tcpip", dest_addr, local_addr)
            #
            self.order_session = paramiko.SSHClient()
            self.order_session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # jhost.load_host_keys('/home/osmanl/.ssh/known_hosts') #disabled#
            self.order_session.connect(self.nodeip, username=self.nodeuser, password=self.nodepass, sock=vmchannel)

            self.get_ip_info = True
        else:
            self.warning_6()

    def recover_ip_information(self):
        if self.jump:
            self.dialog_setting.checkBox.setChecked(True)
            self.dialog_setting.lineEdit_6.setEnabled(True)
            self.dialog_setting.lineEdit_7.setEnabled(True)
            self.dialog_setting.lineEdit_8.setEnabled(True)
        self.dialog_setting.lineEdit.setText(self.nodeip)
        self.dialog_setting.lineEdit_2.setText(self.nodeuser)
        self.dialog_setting.lineEdit_3.setText(self.nodepass)
        self.dialog_setting.lineEdit_4.setText(self.nodepath)
        self.dialog_setting.lineEdit_5.setText(self.local_path)

        self.dialog_setting.lineEdit_6.setText(self.jumpnodeip)
        self.dialog_setting.lineEdit_8.setText(self.jumpnodeuser)
        self.dialog_setting.lineEdit_7.setText(self.jumpnodepass)

    # get setting parameter
    def setting_parameter(self):
        # Node Info
        self.nodeip = self.dialog_setting.lineEdit.text()  # node ip
        self.nodeuser = self.dialog_setting.lineEdit_2.text()  # node user name
        self.nodepass = self.dialog_setting.lineEdit_3.text()  # node password
        self.nodepath = self.dialog_setting.lineEdit_4.text()  # node path
        # Jump Node Info
        self.jumpnodeip = self.dialog_setting.lineEdit_6.text()  # jump ip
        self.jumpnodeuser = self.dialog_setting.lineEdit_8.text()  # jump user name
        self.jumpnodepass = self.dialog_setting.lineEdit_7.text()  # jump password
        # Local Info
        self.local_path = self.dialog_setting.lineEdit_5.text()  # win local path
        # If haven't this file directory, create a new one
#        if not os.path.exists(self.local_path):
#            os.mkdir(self.local_path)
        # run function
        if self.dialog_setting.checkBox.checkState() == 2:
            self.jump = True
            self.ui.textBrowser.append("A jump server is used!!")
        self.dialog_setting.close()

    def calculation_vasp_interface(self, cal_type):
        if self.get_ip_info:
            vasp_cal = Vasp_calculation()
            vasp_cal.get_ip_information(self.jumpnodeip, self.jumpnodeuser, self.jumpnodepass, self.nodeip,
                                        self.nodeuser, self.nodepass)
            vasp_cal.set_output(self.ui.textBrowser)
            vasp_cal.set_connection(self.remote_session, self.get_ip_info)
            vasp_cal.set_path(self.local_path, self.nodepath, self.code_path)
            if self.struc_is_defined:
                vasp_cal.set_struc(self.struc)
                if cal_type == 'scf':
                    vasp_cal.vasp_scf()
                elif cal_type == 'scf_noncal':
                    vasp_cal.vasp_scf_noncal()
                elif cal_type == 'band':
                    vasp_cal.vasp_band()
                elif cal_type == 'band_noncal':
                    vasp_cal.vasp_band_noncal()
                elif cal_type == 'dos':
                    vasp_cal.vasp_DOS()
                elif cal_type == 'phonon':
                    vasp_cal.vasp_phonon()
                elif cal_type == 'wannier':
                    vasp_cal.vasp_wannier()
            else:
                self.warning_4()
        else:
            self.warning_1()

    def plot_vasp_interface(self, file_type):
        if file_type == 'CHGCAR':
            plot_CHGCAR(self.scene)

    def type_of_cell(self):
        self.dialog_test = Pyxtal_table()
        # get desktop path
        self.dialog_test.lineEdit.setText(os.path.join(os.path.expanduser('~'), "Desktop\\VASP_files"))
        # self.dialog_test.setModal(True)  # Set modal window
        self.dialog_test.show()
        self.dialog_test.pushButton.clicked.connect(self.pyxtal_func)
        self.ui.actionclose.triggered.connect(self.dialog_test.close)
        self.ui.textBrowser.append("A random structure have been produced.")
        self.dialog_test.exec_()

    def download_vasp(self):
        if self.get_ip_info:
            self.dialog_download = Download_table()
            # dialog.setModal(True)  # Set modal window
            self.dialog_download.show()
            self.dialog_download.lineEdit_3.setText(self.nodeip)
            self.dialog_download.lineEdit_4.setText(self.nodeuser)
            self.dialog_download.lineEdit_5.setText(self.nodepath)

            # get local path
            def get_local_path():
                curPath = QDir.currentPath()
                dlgTitle = "Select a local path to save the file"
                self.selectedDir = QFileDialog.getExistingDirectory(caption=dlgTitle, directory=curPath)
                self.dialog_download.lineEdit_2.setText(self.selectedDir)

            # get download path and download file
            def download_vasp_file():

                # get download path
                server_path = self.dialog_download.lineEdit.text()
                local_path = self.dialog_download.lineEdit_2.text()
                self.dialog_download.close()
                # self.output.append("Start downloading files")
                QApplication.processEvents()

                # download vasp file
                # order_all = 'cd /home/zhoupan/luxin/be2si_repet/band;ls'
                # stdin, stdout, stderr = self.order_session.exec_command(order_all, get_pty=False)
                # print(self.order_session.exec_command(order_all))
                # result = stdout.read()  # get result
                # print(result.decode("utf-8"))

                # Check whether the path is correct
                try:
                    self.remote_session.get(server_path, local_path)
                except:
                    self.warning_5()

                # close
                self.dialog_download.close()
                QApplication.processEvents()

            self.dialog_download.pushButton.clicked.connect(download_vasp_file)
            self.dialog_download.pushButton_2.clicked.connect(get_local_path)
            self.dialog_download.exec_()
        else:
            self.warning_1()

    # Instruction
    def instruction(self):
        # webbrowser.open("http://www.baidu.com")
        self.dialog_introduction = Introduction_table()
        # self.dialog_introduction.setModal(True)  # Set modal window
        self.dialog_introduction.show()
        # self.dialog_introduction.label.setText('self.nodeip')
        self.dialog_introduction.exec_()

    # About
    def about(self):
        dlgTitle = "About"
        strInfo = "Abinito Studio V1.0.0\n\n" \
                  "The developer has made every effort to ensure the accuracy of this software, but inevitably there will be omissions. " \
                  "You are welcome to give us feedback on the problems you find to help us improve the quality of the software.\n\n" \
                  "Contact us by\n" \
                  "QQ group: 461248214\n" \
                  "Email: zhoupan71234@xtu.edu.cn\n"
        QMessageBox.information(self, dlgTitle, strInfo)  # about

    # Zoom by mouse wheel
    def do_scrollZoom(self, event):
        ax = event.inaxes  # Generate event axes objects
        if ax == None:
            return
        # Push the current view limits and position onto the stack，this is the way to restore.
        self.plt_toolbar.push_current()
        xmin, xmax = ax.get_xbound()
        xlen = xmax - xmin
        ymin, ymax = ax.get_ybound()
        ylen = ymax - ymin
        # step [scalar],positive = ’up’, negative ='down'
        xchg = event.step * xlen / 20
        xmin = xmin + xchg
        xmax = xmax - xchg
        ychg = event.step * ylen / 20
        ymin = ymin + ychg
        ymax = ymax - ychg
        ax.set_xbound(xmin, xmax)
        ax.set_ybound(ymin, ymax)
        event.canvas.draw()

    # Color selection
    def Color_choose(self):
        self.color = QColorDialog.getColor()  # QColor gets the current color
        self.color_sum = self.color.name()

    # Center the main window
    def center(self):
        # Get screen coordinates
        screen = QDesktopWidget().screenGeometry()
        # Get window coordinates
        size = self.geometry()
        # Main window width and height
        width = 800
        height = 550
        self.resize(width, height)
        newLeft = (screen.width() - size.width() - (width / 2)) / 2
        newTop = (screen.height() - size.height() - (height / 2)) / 2
        self.move(newLeft, newTop)

    def warning_1(self):
        dlgTitle = "Warning"
        strInfo = "Please set the information about the node！"
        QMessageBox.warning(self, dlgTitle, strInfo)

    def warning_2(self):
        dlgTitle = "Warning"
        strInfo = "Remote connection failed.\n" \
                  "Please check the node information input!"
        QMessageBox.warning(self, dlgTitle, strInfo)

    def warning_3(self):
        dlgTitle = "Warning"
        strInfo = "The parameters of the crystal structure is not matched！"
        QMessageBox.warning(self, dlgTitle, strInfo)

    def warning_4(self):
        dlgTitle = "Warning"
        strInfo = "A structure is not opened！"
        QMessageBox.warning(self, dlgTitle, strInfo)

    def warning_5(self):
        dlgTitle = "Warning"
        strInfo = "Path is wrong. Please check and try again！"
        QMessageBox.warning(self, dlgTitle, strInfo)

    def warning_6(self):
        dlgTitle = "Warning"
        strInfo = "Local Path does not exist！"
        QMessageBox.warning(self, dlgTitle, strInfo)


class Figure_Canvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=100)
        super(Figure_Canvas, self).__init__(self.fig)
        self.setParent(parent)
        # Chinese font setting - bold
        plt.rcParams['font.sans-serif'] = ['SimHei']
        # Resolves saving images with a negative '-' sign displayed as a block
        plt.rcParams['axes.unicode_minus'] = False
        # Set the direction of the axis tick mark inward
        plt.rcParams['xtick.direction'] = 'in'
        plt.rcParams['ytick.direction'] = 'in'
        plt.rcParams['ytick.right'] = plt.rcParams['ytick.labelright'] = False
        plt.rcParams['ytick.left'] = plt.rcParams['ytick.labelleft'] = False
        plt.rcParams['xtick.bottom'] = plt.rcParams['xtick.labelbottom'] = False
        plt.rcParams['xtick.top'] = plt.rcParams['xtick.labeltop'] = False


# Middle mayavi window
class MayaviQWidget(QWidget):  # Mayavi window
    def __init__(self, parent=None):  # Initialization
        QWidget.__init__(self, parent)
        layout = QVBoxLayout(self)  # Vertical layout
        # Content margin, the distance from the control to the four surrounding edges (left, top, right, bottom)
        layout.setContentsMargins(0, 0, 0, 0)
        # The distance between the top and bottom of the control and the form
        layout.setSpacing(0)
        self.visualization = Visualization()  # Visualization
        self.ui = self.visualization.edit_traits(parent=self, kind='subpanel').control
        layout.addWidget(self.ui)  # Add self.ui to the layout, which is a vertical layout
        self.ui.setParent(self)  # Parent window fis itself


# Scientific Computing 3D Visualization - Listening of Traits Properties
class Visualization(HasTraits):
    scene = Instance(MlabSceneModel, ())

    # Scientific Computing 3D Visualization - Listening for Traits Attributes
    @on_trait_change('scene.activated')
    def update_plot(self):
        self.scene.mlab.clf()  # Clear the current scene
        self.scene.background = (1, 1, 1)
        self.scene.parallel_projection = True

    view = View(Item('scene',
                     editor=SceneEditor(scene_class=MayaviScene),
                     height=250,
                     width=300,
                     show_label=False),
                resizable=True)  # The height and width of the middle Mayavi window


# Parameter Input Dialog
class Pyxtal_table(QDialog, Ui_Form_UI_pyxtal):
    def __init__(self):
        super(Pyxtal_table, self).__init__()
        self.setupUi(self)


# Setting Input Dialog
class Setting_table(QDialog, Ui_Form_UI_setting):
    def __init__(self):
        super(Setting_table, self).__init__()
        self.setupUi(self)
        # self.resize(1000, 500)


class Lattice_Dialog(QtWidgets.QDialog, Ui_Lattice):
    def __init__(self):
        super(Lattice_Dialog, self).__init__()
        self.setupUi(self)


class Structure_Dialog(QtWidgets.QDialog, Ui_structure):
    def __init__(self):
        super(Structure_Dialog, self).__init__()
        self.setupUi(self)


class Download_table(QDialog, Ui_Form_UI_download):
    def __init__(self):
        super(Download_table, self).__init__()
        self.setupUi(self)
        # self.resize(1000, 500)


class Introduction_table(QDialog, Ui_Form_UI_introduction):
    def __init__(self):
        super(Introduction_table, self).__init__()
        self.setupUi(self)
        # self.resize(1000, 500)
