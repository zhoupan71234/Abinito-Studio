# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_introduction.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import webbrowser


class Ui_Form_UI_introduction(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(282, 137)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/structure.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        Form.setStyleSheet("QPushButton{\n"
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
"QRadioButton{\n"
"color:rgb(0, 85, 255);\n"
"font: 12pt \"Times New Roman\";\n"
"}\n"
"")
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setMinimumSize(QtCore.QSize(110, 0))
        self.label.setMaximumSize(QtCore.QSize(110, 16777215))
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setMinimumSize(QtCore.QSize(110, 0))
        self.label_2.setMaximumSize(QtCore.QSize(110, 16777215))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(True)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("QLabel{\n"
"color:rgb(170, 85, 255);\n"
"font: 12pt \"Times New Roman\";\n"
"}")
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setMinimumSize(QtCore.QSize(110, 0))
        self.label_3.setMaximumSize(QtCore.QSize(110, 16777215))
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setMinimumSize(QtCore.QSize(110, 0))
        self.label_4.setMaximumSize(QtCore.QSize(110, 16777215))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(True)
        font.setWeight(50)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("QLabel{\n"
"color:rgb(170, 85, 255);\n"
"font: 12pt \"Times New Roman\";\n"
"}")
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)

        self.retranslateUi(Form)
        self.label_2.linkActivated['QString'].connect(self.manual_url) # type: ignore
        self.label_4.linkActivated['QString'].connect(self.open_source_url) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "introduction"))
        self.label.setText(_translate("Form", "Manual link："))
        self.label_2.setText(_translate("Form", u'<a href="https://pypi.org/">https://pypi.org/</a>'))
        self.label_3.setText(_translate("Form", "Open source link："))
        self.label_4.setText(_translate("Form", u'<a href="https://github.com/">https://github.com/</a>'))

    def manual_url(self):
        webbrowser.open("https://pypi.org/")

    def open_source_url(self):
        webbrowser.open("https://github.com/")
