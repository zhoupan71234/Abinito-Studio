# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_vasp_supercell.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form_UI_supercell(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(253, 115)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/structure.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setStyleSheet("QPushButton{\n"
                             "color:rgb(255, 0, 0);\n"
                             "font: 12pt \"Times New Roman\";\n"
                             "}\n"
                             "\n"
                             "QLabel{\n"
                             "color:rgb(0, 85, 255);\n"
                             "font: 12pt \"Times New Roman\";\n"
                             "}\n"
                             "\n"
                             "QCheckBox{\n"
                             "color:rgb(0, 85, 255);\n"
                             "font: 12pt \"Times New Roman\";\n"
                             "}\n"
                             "\n"
                             "QGroupBox{\n"
                             "color:rgb(170, 85, 255);\n"
                             "font: 12pt \"Times New Roman\";\n"
                             "}\n"
                             "\n"
                             "QTextBrowser{\n"
                             "font: 12pt \"Times New Roman\";\n"
                             "}\n"
                             "\n"
                             "QLineEdit{\n"
                             "font: 12pt \"Times New Roman\";\n"
                             "}\n"
                             "\n"
                             "QTabWidget{\n"
                             "color:rgb(0, 85, 255);\n"
                             "font: 12pt \"Times New Roman\";\n"
                             "}\n"
                             "\n"
                             "QRadioButton{\n"
                             "color:rgb(0, 85, 255);\n"
                             "font: 12pt \"Times New Roman\";\n"
                             "}\n"
                             "\n"
                             "QSpinBox{\n"
                             "color:rgb(0, 85, 255);\n"
                             "font: 12pt \"Times New Roman\";\n"
                             "}")
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.spinBox = QtWidgets.QSpinBox(self.groupBox)
        self.spinBox.setProperty("value", 1)
        self.spinBox.setObjectName("spinBox")
        self.horizontalLayout.addWidget(self.spinBox)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.spinBox_2 = QtWidgets.QSpinBox(self.groupBox)
        self.spinBox_2.setProperty("value", 1)
        self.spinBox_2.setObjectName("spinBox_2")
        self.horizontalLayout.addWidget(self.spinBox_2)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.spinBox_3 = QtWidgets.QSpinBox(self.groupBox)
        self.spinBox_3.setProperty("value", 1)
        self.spinBox_3.setObjectName("spinBox_3")
        self.horizontalLayout.addWidget(self.spinBox_3)
        self.verticalLayout.addWidget(self.groupBox)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setMinimumSize(QtCore.QSize(90, 20))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_4.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.retranslateUi(Dialog)
        self.pushButton.clicked.connect(Dialog.close)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Supercell"))
        self.groupBox.setTitle(_translate("Dialog", "Size of supercell"))
        self.label.setText(_translate("Dialog", "<html><head/><body><p>a:</p></body></html>"))
        self.label_2.setText(_translate("Dialog", "<html><head/><body><p>  b:</p></body></html>"))
        self.label_3.setText(_translate("Dialog", "<html><head/><body><p>  c:</p></body></html>"))
        self.pushButton.setText(_translate("Dialog", "Enter"))
