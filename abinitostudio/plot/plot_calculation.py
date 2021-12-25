import os
import numpy as np
import matplotlib.pyplot as plt
from threading import Thread
from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import QDialog, QFileDialog, QColorDialog, QMessageBox
from abinitostudio.ui.Dialog_DOS import Ui_Dialog_DOS
from abinitostudio.ui.Dialog_PB import Ui_Dialog_PB
from abinitostudio.ui.Dialog_band import Ui_Dialog_band
from abinitostudio.ui.Dialog_CHGCAR_2D import Ui_Dialog_CHGCAR_2D
from abinitostudio.ui.Dialog_CHGCAR_3D import Ui_Dialog_CHGCAR_3D
from abinitostudio.io.vasp_io import readEIGENVAL, readDOSCAR, readPROCAR, readCHGCAR

from tvtk.api import tvtk

# Class Plot
class Plot_calculation():
    def __init__(self):
        pass

    # Bands
    def show_Dialog_bands(self):
        # Get the current directory of the system
        curPath = QDir.currentPath()
        dlgTitle = "Choose a EIGENVAL file"
        filt = "All files(*.*);;Text file(*.txt);;figure file(*.jpg *.gif *.png)"  # File filters
        filename, filtUsed = QFileDialog.getOpenFileName(self, dlgTitle, curPath, filt)
        extractfileName = (os.path.basename(filename))[0:8]
        if extractfileName == "EIGENVAL":
            dialog_bands = Bounced_bands()
            dialog_bands.setModal(True)  # Set up modal windows
            dialog_bands.show()

            def get_parameters_dialog_bands():
                self.fermi_level = float(dialog_bands.lineEdit.text())
                self.dots_num_bands = int(dialog_bands.lineEdit_9.text())
                self.high_symmetry_point = eval(dialog_bands.lineEdit_10.text())

                self.y_max_bands = float(dialog_bands.lineEdit_11.text())
                self.y_min_bands = float(dialog_bands.lineEdit_12.text())

                self.y_label_bands = dialog_bands.lineEdit_7.text()
                self.y_labelbold_bands = dialog_bands.spinBox_7.value()

                self.title_bands = dialog_bands.lineEdit_8.text()
                self.titlebold_bands = dialog_bands.spinBox_6.value()

                self.dotlinewidth = dialog_bands.spinBox_4.value()
                self.solidlinewidth = dialog_bands.spinBox_5.value()

                self.axis_bold = dialog_bands.spinBox.value()
                self.tick_orientation = dialog_bands.comboBox.currentText()
                self.tick_bold = dialog_bands.spinBox_2.value()
                self.tick_lable_bold = dialog_bands.spinBox_3.value()

                self.saving_dpi = dialog_bands.spinBox_10.value()

                self.load_EIGENVAL(filename)
                dialog_bands.close()

            dialog_bands.pushButton.clicked.connect(get_parameters_dialog_bands)
            dialog_bands.exec_()
        else:
            self.ui.textBrowser.setText("The file you choose is not a EIGENVAL file.")

    def load_EIGENVAL(self, fileName):
        plt.rcParams['savefig.dpi'] = self.saving_dpi  # Picture pixel
        plt.rcParams['figure.dpi'] = self.saving_dpi  # Picture resolution
        self.axes.cla()  # Empty the sketchpad
        eigfile_1 = readEIGENVAL(fileName)[1]
        nk, num_band = np.shape(eigfile_1)  # 180,32
        # each dimension is from 0 to 240 (horizontal coordinates)
        e_tmp = np.array(eigfile_1).T
        self.x_max_bands = len(e_tmp[0])  # Horizontal coordinate maximum 240
        self.period_dots_num = len(e_tmp[0]) / (self.dots_num_bands)
        # Coordinate axis bold
        self.axes.spines['bottom'].set_linewidth(self.axis_bold)
        self.axes.spines['left'].set_linewidth(self.axis_bold)
        self.axes.spines['right'].set_linewidth(self.axis_bold)
        self.axes.spines['top'].set_linewidth(self.axis_bold)
        # Coordinate scale line, coordinate scale
        self.axes.tick_params(top=False, bottom=False, right=False,
                              pad=7.5,
                              direction=self.tick_orientation,
                              width=self.tick_bold,
                              labelsize=self.tick_lable_bold)
        # Draw a dotted line
        self.axes.axhline(y=0, ls=":", c="black", linewidth=self.dotlinewidth)  # Add horizontal line
        xticks = []
        for i in range(self.dots_num_bands):
            if i != 0:
                self.axes.axvline(x=i * self.period_dots_num, ls=":", c="black",
                                  linewidth=self.dotlinewidth)  # Add vertical line
            xticks.append(int(i * self.period_dots_num))
        xticks.append(int(self.x_max_bands))
        # Set the x-axis label
        self.axes.set_xticks(xticks)
        self.axes.set_xticklabels(self.high_symmetry_point, fontdict={'family': 'Times New Roman'})
        # Set the y-axis label and title
        self.axes.set_ylabel(self.y_label_bands,
                             fontsize=self.y_labelbold_bands,
                             fontdict={'family': 'Times New Roman'})
        self.axes.set_title(self.title_bands,
                            fontsize=self.titlebold_bands,
                            fontdict={'family': 'Times New Roman'})
        # Set the minimum and maximum values of the x-axis and y-axis
        self.axes.set_xlim(0, self.x_max_bands)
        self.axes.set_ylim(self.y_min_bands, self.y_max_bands)
        for i in range(num_band):  # num_band is the number of energy bands of 32
            self.axes.plot((e_tmp[i]) - (self.fermi_level), c='b', linewidth=self.solidlinewidth)
        if readEIGENVAL(fileName)[0] == 3:
            eigfile_2 = readEIGENVAL(fileName)[2]
            e_tmp_2 = np.array(eigfile_2).T
            for i in range(num_band):  # num_band is the number of energy bands of 32
                self.axes.plot((e_tmp_2[i]) - (self.fermi_level), c='r')
            self.axes.plot((e_tmp[0]) - (self.fermi_level), c='b', label='$spin-up$')
            self.axes.plot((e_tmp_2[0]) - (self.fermi_level), c='r', label='$spin-down$')
        self.ui.textBrowser.setText(f"\nThe number of bands：{len(e_tmp)}\n")
        self.ui.textBrowser.append(f"\n you open a EIGENVAL file, the path is：\n{fileName}")
        self.plt_pattern.draw()  # refresh the palette to draw

    # Projection bands
    def show_Dialog_PB(self):
        curPath = QDir.currentPath()  # Get system current directory
        dlgTitle = "Choose a PROCAR file"  # Dialog title
        filt = "All files(*.*);;Text file(*.txt);;figure file(*.jpg *.gif *.png)"  # File filter
        filename, filtUsed = QFileDialog.getOpenFileName(self, dlgTitle, curPath, filt)
        extractfileName = (os.path.basename(filename))[0:6]
        if extractfileName == "PROCAR":
            dialog_PB = Bounced_PB()
            dialog_PB.setModal(True)  # Set modal window
            dialog_PB.show()
            self.color_sum = "#0055ff"

            self.color_s = "#0055ff"
            self.color_p = "#ff0000"
            self.color_d = "#00aa00"
            self.color_tol = "#5500ff"

            self.color_p_y = "#aa5500"
            self.color_p_z = "#aa55ff"
            self.color_p_x = "#ff5500"

            self.color_d_xy = "#ff557f"
            self.color_d_yz = "#55aa7f"
            self.color_d_z2 = "#aaaa7f"
            self.color_d_xz = "#ffaa7f"
            self.color_d_x2_y2 = "#ffff7f"

            def get_parameters_dialog_PB():
                # Passing parameters from a PB diglog
                self.fermi_level = float(dialog_PB.lineEdit.text())
                self.high_point_num = int(dialog_PB.lineEdit_16.text())
                self.y_min_pb = float(dialog_PB.lineEdit_4.text())
                self.y_max_pb = float(dialog_PB.lineEdit_5.text())
                self.y_label_pb = dialog_PB.lineEdit_7.text()
                self.title_pb = dialog_PB.lineEdit_8.text()
                self.ratio = float(dialog_PB.lineEdit_9.text())
                self.listatom_input = dialog_PB.lineEdit_12.text()
                self.atomname_atom = dialog_PB.lineEdit_15.text()
                self.radioButton = dialog_PB.radioButton

                self.state_s_pb = dialog_PB.checkBox.checkState()
                self.state_p_tol_pb = dialog_PB.checkBox_2.checkState()
                self.state_d_tol_pb = dialog_PB.checkBox_3.checkState()
                self.state_tol_pb = dialog_PB.checkBox_4.checkState()

                self.state_p_y_pb = dialog_PB.checkBox_5.checkState()
                self.state_p_z_pb = dialog_PB.checkBox_6.checkState()
                self.state_p_x_pb = dialog_PB.checkBox_7.checkState()

                self.state_d_xy_pb = dialog_PB.checkBox_8.checkState()
                self.state_d_yz_pb = dialog_PB.checkBox_9.checkState()
                self.state_d_z2_pb = dialog_PB.checkBox_10.checkState()
                self.state_d_xz_pb = dialog_PB.checkBox_11.checkState()
                self.state_d_x2_y2_pb = dialog_PB.checkBox_12.checkState()

                self.narrow = int(dialog_PB.lineEdit_17.text())
                self.ion_orb_num = int(dialog_PB.lineEdit_18.text())

                self.zorder_s = int(dialog_PB.lineEdit_10.text())
                self.zorder_p_tol = int(dialog_PB.lineEdit_11.text())
                self.zorder_d_tol = int(dialog_PB.lineEdit_13.text())
                self.zorder_tol = int(dialog_PB.lineEdit_14.text())
                self.zorder_p_y = int(dialog_PB.lineEdit_19.text())
                self.zorder_p_z = int(dialog_PB.lineEdit_20.text())
                self.zorder_p_x = int(dialog_PB.lineEdit_21.text())
                self.zorder_d_xy = int(dialog_PB.lineEdit_22.text())
                self.zorder_d_yz = int(dialog_PB.lineEdit_23.text())
                self.zorder_d_z2 = int(dialog_PB.lineEdit_24.text())
                self.zorder_d_xz = int(dialog_PB.lineEdit_25.text())
                self.zorder_d_x2_y2 = int(dialog_PB.lineEdit_26.text())
                # The function load_PROCAR is the actual drawing function
                self.load_PROCAR(filename)
                dialog_PB.close()

            def Color_choose_s():
                self.color = QColorDialog.getColor()  # QColor gets the current color
                self.color_s = self.color.name()
                dialog_PB.pushButton_3.setStyleSheet('QPushButton {background-color:%s}' % self.color_s)

            def Color_choose_p():
                self.color = QColorDialog.getColor()  # QColor gets the current color
                self.color_p = self.color.name()
                dialog_PB.pushButton_4.setStyleSheet('QPushButton {background-color:%s}' % self.color_p)

            def Color_choose_d():
                self.color = QColorDialog.getColor()  # QColor gets the current color
                self.color_d = self.color.name()
                dialog_PB.pushButton_5.setStyleSheet('QPushButton {background-color:%s}' % self.color_d)

            def Color_choose_tol():
                self.color = QColorDialog.getColor()  # QColor gets the current color
                self.color_tol = self.color.name()
                dialog_PB.pushButton_6.setStyleSheet('QPushButton {background-color:%s}' % self.color_tol)

            def Color_choose_p_y():
                self.color = QColorDialog.getColor()  # QColor gets the current color
                self.color_p_y = self.color.name()
                dialog_PB.pushButton_7.setStyleSheet('QPushButton {background-color:%s}' % self.color_p_y)

            def Color_choose_p_z():
                self.color = QColorDialog.getColor()  # QColor gets the current color
                self.color_p_z = self.color.name()
                dialog_PB.pushButton_8.setStyleSheet('QPushButton {background-color:%s}' % self.color_p_z)

            def Color_choose_p_x():
                self.color = QColorDialog.getColor()  # QColor gets the current color
                self.color_p_x = self.color.name()
                dialog_PB.pushButton_9.setStyleSheet('QPushButton {background-color:%s}' % self.color_p_x)

            def Color_choose_d_xy():
                self.color = QColorDialog.getColor()  # QColor gets the current color
                self.color_d_xy = self.color.name()
                dialog_PB.pushButton_10.setStyleSheet('QPushButton {background-color:%s}' % self.color_d_xy)

            def Color_choose_d_yz():
                self.color = QColorDialog.getColor()  # QColor gets the current color
                self.color_d_yz = self.color.name()
                dialog_PB.pushButton_11.setStyleSheet('QPushButton {background-color:%s}' % self.color_d_yz)

            def Color_choose_d_z2():
                self.color = QColorDialog.getColor()  # QColor gets the current color
                self.color_d_z2 = self.color.name()
                dialog_PB.pushButton_12.setStyleSheet('QPushButton {background-color:%s}' % self.color_d_z2)

            def Color_choose_d_xz():
                self.color = QColorDialog.getColor()  # QColor gets the current color
                self.color_d_xz = self.color.name()
                dialog_PB.pushButton_13.setStyleSheet('QPushButton {background-color:%s}' % self.color_d_xz)

            def Color_choose_d_x2_y2():
                self.color = QColorDialog.getColor()  # QColor gets the current color
                self.color_d_x2_y2 = self.color.name()
                dialog_PB.pushButton_14.setStyleSheet('QPushButton {background-color:%s}' % self.color_d_x2_y2)

            dialog_PB.pushButton.clicked.connect(get_parameters_dialog_PB)
            # Incoming color
            dialog_PB.pushButton_2.clicked.connect(self.Color_choose)
            dialog_PB.pushButton_3.clicked.connect(Color_choose_s)
            dialog_PB.pushButton_4.clicked.connect(Color_choose_p)
            dialog_PB.pushButton_5.clicked.connect(Color_choose_d)
            dialog_PB.pushButton_6.clicked.connect(Color_choose_tol)
            dialog_PB.pushButton_7.clicked.connect(Color_choose_p_y)
            dialog_PB.pushButton_8.clicked.connect(Color_choose_p_z)
            dialog_PB.pushButton_9.clicked.connect(Color_choose_p_x)
            dialog_PB.pushButton_10.clicked.connect(Color_choose_d_xy)
            dialog_PB.pushButton_11.clicked.connect(Color_choose_d_yz)
            dialog_PB.pushButton_12.clicked.connect(Color_choose_d_z2)
            dialog_PB.pushButton_13.clicked.connect(Color_choose_d_xz)
            dialog_PB.pushButton_14.clicked.connect(Color_choose_d_x2_y2)
            self.ui.textBrowser.setText("Preparing to draw the projection band...")
            dialog_PB.exec_()
        else:
            self.ui.textBrowser.setText("The file you choose is not a PROCAR file.")

    def load_PROCAR(self, fileName):
        total_band_atom = readPROCAR(fileName)[0]
        k_x = readPROCAR(fileName)[1]  # 180 abscissas
        k_y = readPROCAR(fileName)[2]  # 180 ordinates each *16
        n_kpoints = readPROCAR(fileName)[3]  # k points
        n_bands = readPROCAR(fileName)[4]  # Number of bands
        narrow = self.narrow  # Scaling factor
        ion_orb_num = self.ion_orb_num  # Atomic orbital subscript index
        self.axes.cla()  # Empty the drawing board
        # p
        if self.state_p_y_pb == 2:
            self.ui.textBrowser.append("\np_y orbital selected")

            def threadFunc():
                for i in range(int(n_kpoints // narrow)):  # Cycle 180 k points
                    for j in range(n_bands):  # Each k point has 16 bands
                        # The extra points are not drawn
                        if self.y_min_pb < (k_y[i * narrow][j]) - self.fermi_level < self.y_max_pb:
                            # total_band_atom[1st k point] [1st band] [1st atom] [s orbital]
                            self.axes.scatter(k_x[i * narrow],
                                              k_y[i * narrow][j] - self.fermi_level,
                                              s=self.ratio * np.absolute(
                                                  total_band_atom[i * narrow][j][ion_orb_num][1]),
                                              marker='o', c=self.color_p_y, zorder=self.zorder_p_y)

                self.axes.scatter(k_x[-1], k_y[-1][-1] - self.fermi_level, s=10,
                                  c=self.color_p_y, label=self.atomname_atom + '$-p-y$')
                self.axes.legend()  # Automatically generate legend
                self.plt_pattern.draw()

            thread = Thread(target=threadFunc, args=())
            thread.start()
            self.ui.textBrowser.append("The color selected by the p_y orbital is:"
                                       + f"<font color={self.color_p_y}>{self.color_p_y}</font>\n")
        if self.state_p_z_pb == 2:
            self.ui.textBrowser.append("\np_z orbital selected")

            def threadFunc():
                for i in range(int(n_kpoints // narrow)):
                    for j in range(n_bands):
                        if self.y_min_pb < (k_y[i * narrow][j]) - self.fermi_level < self.y_max_pb:
                            self.axes.scatter(k_x[i * narrow], k_y[i * narrow][j] - self.fermi_level,
                                              s=self.ratio * np.absolute(
                                                  total_band_atom[i * narrow][j][ion_orb_num][2]),
                                              marker='o', c=self.color_p_z, zorder=self.zorder_p_z)

                self.axes.scatter(k_x[-1], k_y[-1][-1] - self.fermi_level,
                                  s=10, c=self.color_p_z, label=self.atomname_atom + '$-p-z$')
                self.axes.legend()
                self.plt_pattern.draw()

            thread = Thread(target=threadFunc, args=())
            thread.start()
            self.ui.textBrowser.append("The color selected by the p_z orbital is:"
                                       + f"<font color={self.color_p_z}>{self.color_p_z}</font>\n")
        if self.state_p_x_pb == 2:
            self.ui.textBrowser.append("\np_x orbital selected")

            def threadFunc():
                for i in range(int(n_kpoints // narrow)):
                    for j in range(n_bands):
                        if self.y_min_pb < (k_y[i * narrow][j]) - self.fermi_level < self.y_max_pb:
                            self.axes.scatter(k_x[i * narrow], k_y[i * narrow][j] - self.fermi_level,
                                              s=self.ratio * np.absolute(
                                                  total_band_atom[i * narrow][j][ion_orb_num][3]),
                                              marker='o', c=self.color_p_x, zorder=self.zorder_p_x)

                self.axes.scatter(k_x[-1], k_y[-1][-1] - self.fermi_level,
                                  s=10, c=self.color_p_x, label=self.atomname_atom + '$-p-x$')
                self.axes.legend()
                self.plt_pattern.draw()

            thread = Thread(target=threadFunc, args=())
            thread.start()
            self.ui.textBrowser.append("The color selected by the p_x orbital is:"
                                       + f"<font color={self.color_p_x}>{self.color_p_x}</font>\n")
        # d
        if self.state_d_xy_pb == 2:
            self.ui.textBrowser.append("\nd_xy orbital selected")

            def threadFunc():
                for i in range(int(n_kpoints // narrow)):
                    for j in range(n_bands):
                        if self.y_min_pb < (k_y[i * narrow][j]) - self.fermi_level < self.y_max_pb:
                            self.axes.scatter(k_x[i * narrow], k_y[i * narrow][j] - self.fermi_level,
                                              s=self.ratio * np.absolute(
                                                  total_band_atom[i * narrow][j][ion_orb_num][4]),
                                              marker='o', c=self.color_d_xy, zorder=self.zorder_d_xy)

                self.axes.scatter(k_x[-1], k_y[-1][-1] - self.fermi_level,
                                  s=10, c=self.color_d_xy, label=self.atomname_atom + '$-d-xy$')
                self.axes.legend()
                self.plt_pattern.draw()

            thread = Thread(target=threadFunc, args=())
            thread.start()
            self.ui.textBrowser.append("The color selected by the d_xy orbital is:"
                                       + f"<font color={self.color_d_xy}>{self.color_d_xy}</font>\n")
        if self.state_d_yz_pb == 2:
            self.ui.textBrowser.append("\nd_yz orbital selected")

            def threadFunc():
                for i in range(int(n_kpoints // narrow)):
                    for j in range(n_bands):
                        if self.y_min_pb < (k_y[i * narrow][j]) - self.fermi_level < self.y_max_pb:
                            self.axes.scatter(k_x[i * narrow], k_y[i * narrow][j] - self.fermi_level,
                                              s=self.ratio * np.absolute(
                                                  total_band_atom[i * narrow][j][ion_orb_num][5]),
                                              marker='o', c=self.color_d_yz, zorder=self.zorder_d_yz)

                self.axes.scatter(k_x[-1], k_y[-1][-1] - self.fermi_level,
                                  s=10, c=self.color_d_yz, label=self.atomname_atom + '$-d-yz$')
                self.axes.legend()
                self.plt_pattern.draw()

            thread = Thread(target=threadFunc, args=())
            thread.start()
            self.ui.textBrowser.append("The color selected by the d_yz orbital is:"
                                       + f"<font color={self.color_d_yz}>{self.color_d_yz}</font>\n")
        if self.state_d_z2_pb == 2:
            self.ui.textBrowser.append("\nd_z2 orbital selected")

            def threadFunc():
                for i in range(int(n_kpoints // narrow)):
                    for j in range(n_bands):
                        if self.y_min_pb < (k_y[i * narrow][j]) - self.fermi_level < self.y_max_pb:
                            self.axes.scatter(k_x[i * narrow], k_y[i * narrow][j] - self.fermi_level,
                                              s=self.ratio * np.absolute(
                                                  total_band_atom[i * narrow][j][ion_orb_num][6]),
                                              marker='o', c=self.color_d_z2, zorder=self.zorder_d_z2)

                self.axes.scatter(k_x[-1], k_y[-1][-1] - self.fermi_level,
                                  s=10, c=self.color_d_z2, label=self.atomname_atom + '$-d-z2$')
                self.axes.legend()
                self.plt_pattern.draw()

            thread = Thread(target=threadFunc, args=())
            thread.start()
            self.ui.textBrowser.append("The color selected by the d_z2 orbital is:"
                                       + f"<font color={self.color_d_z2}>{self.color_d_z2}</font>\n")
        if self.state_d_xz_pb == 2:
            self.ui.textBrowser.append("\nd_xz orbital selected")

            def threadFunc():
                for i in range(int(n_kpoints // narrow)):
                    for j in range(n_bands):
                        if self.y_min_pb < (k_y[i * narrow][j]) - self.fermi_level < self.y_max_pb:
                            self.axes.scatter(k_x[i * narrow], k_y[i * narrow][j] - self.fermi_level,
                                              s=self.ratio * np.absolute(
                                                  total_band_atom[i * narrow][j][ion_orb_num][7]),
                                              marker='o', c=self.color_d_xz, zorder=self.zorder_d_xz)

                self.axes.scatter(k_x[-1], k_y[-1][-1] - self.fermi_level,
                                  s=10, c=self.color_d_xz, label=self.atomname_atom + '$-d-xz$')
                self.axes.legend()
                self.plt_pattern.draw()

            thread = Thread(target=threadFunc, args=())
            thread.start()
            self.ui.textBrowser.append("The color selected by the d_xz orbital is:"
                                       + f"<font color={self.color_d_xz}>{self.color_d_xz}</font>\n")
        if self.state_d_x2_y2_pb == 2:
            self.ui.textBrowser.append("\nd_x2_y2 orbital selected")

            def threadFunc():
                for i in range(int(n_kpoints // narrow)):
                    for j in range(n_bands):
                        if self.y_min_pb < (k_y[i * narrow][j]) - self.fermi_level < self.y_max_pb:
                            self.axes.scatter(k_x[i * narrow], k_y[i * narrow][j] - self.fermi_level,
                                              s=self.ratio * np.absolute(
                                                  total_band_atom[i * narrow][j][ion_orb_num][8]),
                                              marker='o', c=self.color_d_x2_y2, zorder=self.zorder_d_x2_y2)

                self.axes.scatter(k_x[-1], k_y[-1][-1] - self.fermi_level,
                                  s=10, c=self.color_d_x2_y2, label=self.atomname_atom + '$-d-x2-y2$')
                self.axes.legend()
                self.plt_pattern.draw()

            thread = Thread(target=threadFunc, args=())
            thread.start()
            self.ui.textBrowser.append("The color selected by the d_x2_y2 orbital is:"
                                       + f"<font color={self.color_d_x2_y2}>{self.color_d_x2_y2}</font>\n")
        # total
        if self.state_s_pb == 2:
            self.ui.textBrowser.append("\ns orbital selected")

            def threadFunc():
                for i in range(int(n_kpoints // narrow)):
                    for j in range(n_bands):
                        if self.y_min_pb < (k_y[i * narrow][j]) - self.fermi_level < self.y_max_pb:
                            self.axes.scatter(k_x[i * narrow], k_y[i * narrow][j] - self.fermi_level,
                                              s=self.ratio * np.absolute(
                                                  total_band_atom[i * narrow][j][ion_orb_num][0]),
                                              marker='o', c=self.color_s, zorder=self.zorder_s)

                self.axes.scatter(k_x[-1], k_y[-1][-1] - self.fermi_level,
                                  s=10, c=self.color_s, label=self.atomname_atom + '$-s$')
                self.axes.legend()
                self.plt_pattern.draw()

            thread = Thread(target=threadFunc, args=())
            thread.start()
            self.ui.textBrowser.append("The color selected by the s orbital is:"
                                       + f"<font color={self.color_s}>{self.color_s}</font>\n")
        if self.state_p_tol_pb == 2:
            self.ui.textBrowser.append("\np orbital selected")

            def threadFunc():
                for i in range(int(n_kpoints // narrow)):
                    for j in range(n_bands):
                        if self.y_min_pb < (k_y[i * narrow][j]) - self.fermi_level < self.y_max_pb:
                            self.axes.scatter(k_x[i * narrow], k_y[i * narrow][j] - self.fermi_level,
                                              s=self.ratio * np.absolute(
                                                  total_band_atom[i * narrow][j][ion_orb_num][1] +
                                                  total_band_atom[i * narrow][j][ion_orb_num][2] +
                                                  total_band_atom[i * narrow][j][ion_orb_num][3]),
                                              marker='o', c=self.color_p, zorder=self.zorder_p_tol)

                self.axes.scatter(k_x[-1], k_y[-1][-1] - self.fermi_level,
                                  s=10, c=self.color_p, label=self.atomname_atom + '$-p-tol$')
                self.axes.legend()
                self.plt_pattern.draw()

            thread = Thread(target=threadFunc, args=())
            thread.start()
            self.ui.textBrowser.append("The color selected by the p orbital is:"
                                       + f"<font color={self.color_p}>{self.color_p}</font>\n")
        if self.state_d_tol_pb == 2:
            self.ui.textBrowser.append("\nd orbital selected")

            def threadFunc():
                for i in range(int(n_kpoints // narrow)):
                    for j in range(n_bands):
                        if self.y_min_pb < (k_y[i * narrow][j]) - self.fermi_level < self.y_max_pb:
                            self.axes.scatter(k_x[i * narrow], k_y[i * narrow][j] - self.fermi_level,
                                              s=self.ratio * np.absolute(
                                                  total_band_atom[i * narrow][j][ion_orb_num][4] +
                                                  total_band_atom[i * narrow][j][ion_orb_num][5] +
                                                  total_band_atom[i * narrow][j][ion_orb_num][6] +
                                                  total_band_atom[i * narrow][j][ion_orb_num][7] +
                                                  total_band_atom[i * narrow][j][ion_orb_num][8]),
                                              marker='o', c=self.color_d, zorder=self.zorder_d_tol)

                self.axes.scatter(k_x[-1], k_y[-1][-1] - self.fermi_level,
                                  s=10, c=self.color_d, label=self.atomname_atom + '$-d-tol$')
                self.axes.legend()
                self.plt_pattern.draw()

            thread = Thread(target=threadFunc, args=())
            thread.start()
            self.ui.textBrowser.append("The color selected by the d orbital is:"
                                       + f"<font color={self.color_d}>{self.color_d}</font>\n")
        if self.state_tol_pb == 2:
            self.ui.textBrowser.append("\ntotal orbital selected")

            def threadFunc():
                for i in range(int(n_kpoints // narrow)):
                    for j in range(n_bands):
                        if self.y_min_pb < (k_y[i * narrow][j]) - self.fermi_level < self.y_max_pb:
                            self.axes.scatter(k_x[i * narrow], k_y[i * narrow][j] - self.fermi_level,
                                              s=self.ratio * np.absolute(
                                                  total_band_atom[i * narrow][j][ion_orb_num][9]),
                                              marker='o', c=self.color_tol, zorder=self.zorder_tol)

                self.axes.scatter(k_x[-1], k_y[-1][-1] - self.fermi_level,
                                  s=10, c=self.color_tol, label=self.atomname_atom + '$-total$')
                self.axes.legend()
                self.plt_pattern.draw()

            thread = Thread(target=threadFunc, args=())
            thread.start()
            self.ui.textBrowser.append("The color selected by the total orbital is:"
                                       + f"<font color={self.color_tol}>{self.color_tol}</font>\n")
        # Legend settings
        self.axes.set_title(self.title_pb)  # Picture title
        self.axes.set_xlim(0, max(k_x))
        self.axes.set_ylim(self.y_min_pb, self.y_max_pb)
        self.axes.set_xticks([])  # Do not display the x coordinate
        self.period_dots_num = int(len(k_x) / (self.high_point_num))  # 180/3=60
        for i in range(self.high_point_num):
            if i != 0:
                x = k_x[i * self.period_dots_num - 1]
                self.axes.axvline(x, ls=":", c="black")  # Add a vertical line
        self.axes.axhline(y=0, ls=":", c="black")  # Add horizontal line
        self.plt_pattern.draw()

    # Density of states
    def show_Dialog_DOS(self):
        curPath = QDir.currentPath()
        dlgTitle = "Choose a DOSCAR file"
        filt = "All files(*.*);;Text file(*.txt);;figure file(*.jpg *.gif *.png)"
        filename, filtUsed = QFileDialog.getOpenFileName(self, dlgTitle, curPath, filt)
        extractfileName = (os.path.basename(filename))[0:6]
        if extractfileName == "DOSCAR":
            dialog_DOS = Bounced_DOS()
            dialog_DOS.setModal(True)
            dialog_DOS.show()

            def get_parameters_dialog_DOS():
                self.x_label_dos = dialog_DOS.lineEdit_5.text()
                self.y_label_dos = dialog_DOS.lineEdit_6.text()
                self.title_dos = dialog_DOS.lineEdit_7.text()
                self.state_tol_DOS = dialog_DOS.checkBox_2.checkState()
                self.state_up_DOS = dialog_DOS.checkBox_3.checkState()
                self.state_down_DOS = dialog_DOS.checkBox_15.checkState()
                self.state_s_DOS = dialog_DOS.checkBox_4.checkState()
                self.state_p_tol_DOS = dialog_DOS.checkBox_5.checkState()
                self.state_d_tol_DOS = dialog_DOS.checkBox_6.checkState()
                self.state_p_y_DOS = dialog_DOS.checkBox_7.checkState()
                self.state_p_z_DOS = dialog_DOS.checkBox_8.checkState()
                self.state_p_x_DOS = dialog_DOS.checkBox_9.checkState()
                self.state_d_xy_DOS = dialog_DOS.checkBox_10.checkState()
                self.state_d_yz_DOS = dialog_DOS.checkBox_11.checkState()
                self.state_d_z2_DOS = dialog_DOS.checkBox_12.checkState()
                self.state_d_xz_DOS = dialog_DOS.checkBox_13.checkState()
                self.state_d_x2_y2_DOS = dialog_DOS.checkBox_14.checkState()

                self.load_DOSCAR(filename)
                dialog_DOS.close()

            dialog_DOS.pushButton.clicked.connect(get_parameters_dialog_DOS)
            dialog_DOS.exec_()
        else:
            self.ui.textBrowser.setText("The file you choose is not a DOSCAR file.")

    def load_DOSCAR(self, fileName):
        self.axes.cla()  # empty the sketchpad
        #
        dosfile = readDOSCAR(fileName, 0)  # dosfile is a list, len(dosfile)=5
        x_dos = dosfile[0]
        y_dos_t = dosfile[1]
        y_dos_i = dosfile[2]
        y_dos_s = dosfile[3]
        y_dos_py = dosfile[4]
        y_dos_pz = dosfile[5]
        y_dos_px = dosfile[6]
        y_dos_p_tol = y_dos_py + y_dos_pz + y_dos_px
        y_dos_d_xy = dosfile[7]
        y_dos_d_yz = dosfile[8]
        y_dos_d_z2 = dosfile[9]
        y_dos_d_xz = dosfile[10]
        y_dos_d_x2_y2 = dosfile[11]
        y_dos_d_tol = y_dos_d_xy + y_dos_d_yz + y_dos_d_z2 + y_dos_d_xz + y_dos_d_x2_y2
        y_tol = y_dos_s + y_dos_p_tol + y_dos_d_tol
        self.x_min_dos = min(x_dos)
        self.x_max_dos = max(x_dos)
        self.y_min_dos = min(y_dos_t)
        self.y_max_dos = (max(y_dos_t)) * 1.1
        # s
        if self.state_s_DOS == 2:
            self.y_max_dos = (max(y_dos_s)) * 1.1
            self.axes.plot(x_dos, y_dos_s, label='$s-DOS$')
        # p
        if self.state_p_y_DOS == 2:
            self.y_max_dos = (max(y_dos_py)) * 1.1
            self.axes.plot(x_dos, y_dos_py, label='$p-y-DOS$')
        if self.state_p_z_DOS == 2:
            self.y_max_dos = (max(y_dos_pz)) * 1.1
            self.axes.plot(x_dos, y_dos_pz, label='$p-z-DOS$')
        if self.state_p_x_DOS == 2:
            self.y_max_dos = (max(y_dos_px)) * 1.1
            self.axes.plot(x_dos, y_dos_px, label='$p-x-DOS$')
        if self.state_p_tol_DOS == 2:
            self.y_max_dos = (max(y_dos_p_tol)) * 1.1
            self.axes.plot(x_dos, y_dos_p_tol, label='$p-tol-DOS$')
        # d
        if self.state_d_xy_DOS == 2:
            self.y_max_dos = (max(y_dos_d_xy)) * 1.1
            self.axes.plot(x_dos, y_dos_d_xy, label='$d-xy-DOS$')
        if self.state_d_yz_DOS == 2:
            self.y_max_dos = (max(y_dos_d_yz)) * 1.1
            self.axes.plot(x_dos, y_dos_d_yz, label='$d-yz-DOS$')
        if self.state_d_z2_DOS == 2:
            self.y_max_dos = (max(y_dos_d_z2)) * 1.1
            self.axes.plot(x_dos, y_dos_d_z2, label='$d-z2-DOS$')
        if self.state_d_xz_DOS == 2:
            self.y_max_dos = (max(y_dos_d_xz)) * 1.1
            self.axes.plot(x_dos, y_dos_d_xz, label='$d-xz-DOS$')
        if self.state_d_x2_y2_DOS == 2:
            self.y_max_dos = (max(y_dos_d_x2_y2)) * 1.1
            self.axes.plot(x_dos, y_dos_d_x2_y2, label='$d-x2-y2-DOS$')
        if self.state_d_tol_DOS == 2:
            self.y_max_dos = (max(y_dos_p_tol)) * 1.1
            self.axes.plot(x_dos, y_dos_d_tol, label='$d-tol-DOS$')
        # tol
        if self.state_tol_DOS == 2:
            self.y_max_dos = (max(y_tol)) * 1.1
            self.axes.plot(x_dos, y_tol, label='$tol-DOS$')
        if self.state_up_DOS == 2:
            self.y_max_dos = (max(y_dos_t)) * 1.1
            self.axes.plot(x_dos, y_dos_t, label='$up-DOS$')
        if self.state_down_DOS == 2:
            self.y_max_dos = (max(y_dos_i)) * 1.1
            self.axes.plot(x_dos, y_dos_i, label='$down-DOS$')
        self.axes.set_xlim(self.x_min_dos, self.x_max_dos)
        self.axes.set_ylim(self.y_min_dos, self.y_max_dos)
        self.axes.set(xlabel=self.x_label_dos, ylabel=self.y_label_dos,
                      title=self.title_dos)
        self.ui.textBrowser.setText(f"X minimum value:{np.round(self.x_min_dos)}\n"
                                    f"X maximum value:{np.round(self.x_max_dos)}\n"
                                    f"Y minimum value:{np.round(self.y_min_dos)}\n"
                                    f"Y maximum value:{np.round((self.y_max_dos) / 1.1)}")
        self.ui.textBrowser.append(f"\nOpen the DOSCAR file, the path is:\n {fileName}")
        self.plt_pattern.draw()  # refresh the palette to draw

    # CHGCAR 2D
    def show_Dialog_CHGCAR_2D(self):
        curPath = QDir.currentPath()
        dlgTitle = "Choose a CHGCAR file"
        filt = "All files(*.*);;Text file(*.txt);;figure file(*.jpg *.gif *.png)"
        filename, filtUsed = QFileDialog.getOpenFileName(self, dlgTitle, curPath, filt)
        extractfileName = (os.path.basename(filename))[0:6]
        if extractfileName == "CHGCAR":
            if True:
                dialog_CHGCAR_2D = Bounced_CHGCAR_2D()
                # dialog_CHGCAR_2D.setModal(True)
                dialog_CHGCAR_2D.show()

                def get_parameters_dialog_CHGCAR():
                #     # Choose a plane
                #     # 1, 2, and 3 respectively represent the xy, xz, and yz planes
                #     if dialog_CHGCAR_2D.radioButton.isChecked() == True:
                #         # self.chooseplane = 1
                    self.Origin = dialog_CHGCAR_2D.lineEdit.text()
                #     if dialog_CHGCAR_2D.radioButton_2.isChecked() == True:
                #         # self.chooseplane = 2
                    self.Offset = dialog_CHGCAR_2D.lineEdit_2.text()
                #     if dialog_CHGCAR_2D.radioButton_3.isChecked() == True:
                #         # self.chooseplane = 3
                #         self.offset = dialog_CHGCAR_2D.lineEdit_3.text()
                    # Select offset
                    # self.offset = dialog_CHGCAR_2D.spinBox.value()
                    # self.offset = dialog_CHGCAR_2D.lineEdit.text()
                    dialog_CHGCAR_2D.close()
                    self.load_CHGCAR_2D(filename)

                dialog_CHGCAR_2D.pushButton.clicked.connect(get_parameters_dialog_CHGCAR)
                # dialog_CHGCAR_2D.buttonBox.accepted.connect(get_parameters_dialog_CHGCAR)
                # self.buttonBox.rejected.connect(Form.reject)
                # dialog_CHGCAR_2D.pushButton.clicked.connect(get_parameters_dialog_CHGCAR)
                dialog_CHGCAR_2D.exec_()

            else:
                self.ui.textBrowser.setText("The file you choose is not a CHGCAR file.")

    def load_CHGCAR_2D(self, fileName):
        self.scene.mlab.clf()
        contant, ucell, self.data = readCHGCAR(fileName)
        # print(np.shape(self.data))
        # Draw the unit cell:
        repeat = (1, 1, 1)
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
            cell_box = self.scene.mlab.plot3d(Cxyz[0], Cxyz[1], Cxyz[2],
                                              tube_radius=cell_linewidth,
                                              color=cell_linecolor,
                                              name='CellBox')
            cell_box.mlab_source.dataset.lines = np.array(conn)
        x, y, z = self.produce_grid(ucell, self.data)

        def generate_structured_grid(x, y, z, scalars):
            pts = np.empty(z.shape + (3,), dtype=float)
            pts[..., 0] = x
            pts[..., 1] = y
            pts[..., 2] = z

            pts = pts.transpose(2, 1, 0, 3).copy()
            pts.shape = int(pts.size / 3), 3
            scalars = scalars.T.copy()

            sg = tvtk.StructuredGrid(dimensions=x.shape, points=pts)
            sg.point_data.scalars = scalars.ravel()
            sg.point_data.scalars.name = 'scalars'
            return sg

        sgrid = generate_structured_grid(x, y, z, self.data)
        self.src = self.scene.mlab.pipeline.add_dataset(sgrid)

        self.chgcar_cut()

    # def func_CHGCAR_2D(self, fileName):
    #     # print(self.chooseplane)
    #     # print(self.offset)
    #     self.scene.mlab.clf()
    #     contant, ucell, self.data = readCHGCAR(fileName)
    #     # if self.offset <= min(np.shape(self.data)):
    #     #     print(min(np.shape(self.data)))
    #     if self.chooseplane == 1:
    #         if self.offset > 0 and self.offset <= np.size(self.data, 2):
    #             # print(np.size(self.data, 2))
    #             self.scene.mlab.imshow(self.data[:, :, self.offset-1])
    #         else:
    #             self.warning_5(1, np.size(self.data, 2))
    #     elif self.chooseplane == 2:
    #         if self.offset > 0 and self.offset <= np.size(self.data, 1):
    #             self.scene.mlab.imshow(self.data[:, self.offset-1, :])
    #         else:
    #             self.warning_5(1, np.size(self.data, 1))
    #     elif self.chooseplane == 3:
    #         if self.offset > 0 and self.offset <= np.size(self.data, 0):
    #             self.scene.mlab.imshow(self.data[self.offset-1, :, :])
    #         else:
    #             self.warning_5(1, np.size(self.data, 0))

    # CHGCAR 3D
    def show_Dialog_CHGCAR_3D(self):
        curPath = QDir.currentPath()
        dlgTitle = "Choose a CHGCAR file"
        filt = "All files(*.*);;Text file(*.txt);;figure file(*.jpg *.gif *.png)"
        filename, filtUsed = QFileDialog.getOpenFileName(self, dlgTitle, curPath, filt)
        extractfileName = (os.path.basename(filename))[0:6]
        if extractfileName == "CHGCAR":
            if True:
                dialog_CHGCAR_3D = Bounced_CHGCAR_3D()
                dialog_CHGCAR_3D.setModal(True)
                dialog_CHGCAR_3D.show()

                def get_parameters_dialog_CHGCAR():
                    self.strline = dialog_CHGCAR_3D.lineEdit.text()
                    # self.chgcar_check_cut = dialog_CHGCAR_3D.checkBox.checkState()
                    # self.chgcar_check_vol = dialog_CHGCAR_3D.checkBox_2.checkState()
                    # self.chgcar_check_contour = dialog_CHGCAR_3D.checkBox_3.checkState()
                    self.load_CHGCAR_3D(filename)
                    dialog_CHGCAR_3D.close()

                dialog_CHGCAR_3D.pushButton.clicked.connect(get_parameters_dialog_CHGCAR)
                dialog_CHGCAR_3D.exec_()
            else:
                self.ui.textBrowser.setText("The file you choose is not a CHGCAR file.")

    def produce_grid(self, cell, data):
        cell = np.array(cell)
        dim = np.shape(data)
        xdim = complex(0.0, dim[0]);
        ydim = complex(0.0, dim[1]);
        zdim = complex(0.0, dim[2])
        xtmp, ytmp, ztmp = np.mgrid[0:1.0:xdim, 0:1.0:ydim, 0:1.0:zdim]
        x, y, z = np.mgrid[0:1.0:xdim, 0:1.0:ydim, 0:1.0:zdim]
        for i in range(dim[0]):
            for j in range(dim[1]):
                for k in range(dim[2]):
                    tmp = xtmp[i][j][k] * cell[0] + ytmp[i][j][k] * cell[1] + ztmp[i][j][k] * cell[2]
                    x[i][j][k] = tmp[0];
                    y[i][j][k] = tmp[1];
                    z[i][j][k] = tmp[2];
        return x, y, z

    def load_CHGCAR_3D(self, fileName):
        self.scene.mlab.clf()
        contant, ucell, self.data = readCHGCAR(fileName)
        # print(np.shape(self.data))
        # Draw the unit cell:
        repeat = (1, 1, 1)
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
            cell_box = self.scene.mlab.plot3d(Cxyz[0], Cxyz[1], Cxyz[2],
                                              tube_radius=cell_linewidth,
                                              color=cell_linecolor,
                                              name='CellBox')
            cell_box.mlab_source.dataset.lines = np.array(conn)
        x, y, z = self.produce_grid(ucell, self.data)

        def generate_structured_grid(x, y, z, scalars):
            pts = np.empty(z.shape + (3,), dtype=float)
            pts[..., 0] = x
            pts[..., 1] = y
            pts[..., 2] = z

            pts = pts.transpose(2, 1, 0, 3).copy()
            pts.shape = int(pts.size / 3), 3
            scalars = scalars.T.copy()

            sg = tvtk.StructuredGrid(dimensions=x.shape, points=pts)
            sg.point_data.scalars = scalars.ravel()
            sg.point_data.scalars.name = 'scalars'
            return sg

        sgrid = generate_structured_grid(x, y, z, self.data)
        self.src = self.scene.mlab.pipeline.add_dataset(sgrid)
        # if self.chgcar_check_cut == 2:
        #     self.chgcar_cut()
        #     print('cut was checked')
        # if self.chgcar_check_contour == 2:
        self.chgcar_contour()
        print('contour was checked')

    def chgcar_cut(self):
        # s = self.scene.mlab.pipeline.scalar_cut_plane(self.src)
        # cutpoint = 1 / 2, 1 / 2, 1 / 2
        # s.implicit_plane.normal = (1, 1, 0)  # x cut
        cutpoint = self.Origin.replace('，',',')
        para = self.Offset.replace('，',',')

        try:
            s = self.scene.mlab.pipeline.scalar_cut_plane(self.src)
            s.implicit_plane.normal = eval(para)
            # eval('s.implicit_plane.normal = (%s)' % para)
            s.implicit_plane.origin = eval(cutpoint)
            s.implicit_plane.widget.enabled = True
        except:
            self.warning_5()
        # s.implicit_plane.normal = eval(para)
        # # eval('s.implicit_plane.normal = (%s)' % para)
        # s.implicit_plane.origin = eval(cutpoint)

        # s = self.scene.mlab.pipeline.contour_grid_plane(self.src)
        # s.grid_plane.axis = 'y'
        # s.grid_plane.position = 15

    def chgcar_contour(self):
        para1 = 'self.src,'
        para2 = self.strline
        para = para1 + para2
        try:
            eval('self.scene.mlab.pipeline.iso_surface(%s)' % para)
        except:
            self.warning_5_1()

        # self.scene.mlab.pipeline.iso_surface(self.src, contours=[self.data.min() + 0.1 * self.data.ptp(), ],
        #                                      opacity=0.1)
        # self.scene.mlab.pipeline.iso_surface(self.src, contours=[self.data.max() - 0.1 * self.data.ptp(), ], )
        # self.scene.mlab.pipeline.iso_surface(self.src, contours=3, transparent=True)

        # ,int_value,end_value
    def warning_5(self):
        dlgTitle = "Warning"
        strInfo ='Please enter the data in the form of the example'
        # strInfo = "Displacement should be in the range of [" + str(int_value) + ',' + str(end_value) + ']'
        QMessageBox.warning(self, dlgTitle, strInfo)

    def warning_5_1(self):
        dlgTitle = "Warning"
        strInfo = 'The input data is incorrect, please check and re-enter'
        # strInfo = "Displacement should be in the range of [" + str(int_value) + ',' + str(end_value) + ']'
        QMessageBox.warning(self, dlgTitle, strInfo)

# Plot Dialog
class Bounced_bands(QDialog, Ui_Dialog_band):
    def __init__(self):
        super(Bounced_bands, self).__init__()
        self.setupUi(self)


# Projection Bands Dialog
class Bounced_PB(QDialog, Ui_Dialog_PB):
    def __init__(self):
        super(Bounced_PB, self).__init__()
        self.setupUi(self)


# DOS Dialog
class Bounced_DOS(QDialog, Ui_Dialog_DOS):
    def __init__(self):
        super(Bounced_DOS, self).__init__()
        self.setupUi(self)


# CHGCAR_2D Dialog
class Bounced_CHGCAR_2D(QDialog, Ui_Dialog_CHGCAR_2D):
    def __init__(self):
        super(Bounced_CHGCAR_2D, self).__init__()
        self.setupUi(self)


# CHGCAR_3D Dialog
class Bounced_CHGCAR_3D(QDialog, Ui_Dialog_CHGCAR_3D):
    def __init__(self):
        super(Bounced_CHGCAR_3D, self).__init__()
        self.setupUi(self)
