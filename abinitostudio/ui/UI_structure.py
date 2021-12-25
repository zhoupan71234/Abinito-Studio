from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QHeaderView


class Ui_structure(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(456, 200)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/structure.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        Form.setStyleSheet("QPushButton{\ncolor:rgb(0, 85, 255);\nfont: 12pt \"Times New Roman\";\n}\n\n"
                           "QLabel{\ncolor:rgb(0, 85, 255);\nfont: 12pt \"Times New Roman\";\n}\n\n"
                           "QCheckBox{\ncolor:rgb(0, 85, 255);\nfont: 12pt \"Times New Roman\";\n}\n\n"
                           "QGroupBox{\ncolor:rgb(0, 85, 255);\nfont: 12pt \"Times New Roman\";\n}\n\n"
                           "QTextBrowser{\nfont: 12pt \"Times New Roman\";\n}\n\n"
                           "QLineEdit{\nfont: 12pt \"Times New Roman\";\n}\n\n"
                           "QTabWidget{\ncolor:rgb(0, 85, 255);\nfont: 12pt \"Times New Roman\";\n}\n\n"
                           "QRadioButton{\ncolor:rgb(0, 85, 255);\nfont: 12pt \"Times New Roman\";\n}\n\n"
                           "QTabWidget{\ncolor:rgb(0, 85, 255);\nfont: 12pt \"Times New Roman\";\n}\n"
                           "")

        
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_11 = QtWidgets.QLabel()
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_8.addWidget(self.label_11)
        
        self.radioButton = QtWidgets.QRadioButton()
        self.radioButton.setChecked(True)
        self.radioButton.setObjectName("radioButton")
        self.horizontalLayout_8.addWidget(self.radioButton)
        self.radioButton_2 = QtWidgets.QRadioButton()
        self.radioButton_2.setObjectName("radioButton_2")
        self.horizontalLayout_8.addWidget(self.radioButton_2)
        
        self.verticalLayout.addLayout(self.horizontalLayout_8)
        
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        
        
        self.pushButton = QtWidgets.QPushButton()
        self.pushButton.setObjectName("pushButton")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem1)
        
        self.horizontalLayout_10.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout_10)
        
        self.retranslateUi(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Adjust lattice parameters"))
        self.label_11.setText(_translate("Form", "Choose crystal type: "))
        
        self.radioButton.setText(_translate("Form", "Conventional"))
        self.radioButton_2.setText(_translate("Form", "Primitive"))
        
        self.pushButton.setText(_translate("Form", "Ok"))