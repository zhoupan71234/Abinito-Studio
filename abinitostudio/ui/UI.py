from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(520, 494)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/structure.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("QPushButton{\ncolor:rgb(255, 0, 0);\nfont: 12pt \"Times New Roman\";\n}\n\n"
                                 "QLabel{\ncolor:rgb(0, 0, 0);\nfont: 12pt \"Times New Roman\";\n}\n\n"
                                 "QCheckBox{\ncolor:rgb(0, 85, 255);\nfont: 12pt \"Times New Roman\";\n}\n\n"
                                 "QGroupBox{\ncolor:rgb(170, 85, 255);\nfont: 12pt \"Times New Roman\";\n}\n\n"
                                 "QTextBrowser{\nfont: 12pt \"Times New Roman\";\n}\n\n"
                                 "QLineEdit{\nfont: 12pt \"Times New Roman\";\n}\n\n"
                                 "QDoubleSpinBox{\nfont: 12pt \"Times New Roman\";\n}\n\n"
                                 "")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.splitter_2 = QtWidgets.QSplitter(self.centralwidget)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.splitter_2)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.splitter = QtWidgets.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.layoutWidget = QtWidgets.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textBrowser = QtWidgets.QTextBrowser(self.splitter)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout_3.addWidget(self.splitter_2)
        self.verticalLayout_3.setStretch(0, 20)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 520, 23))
        self.menubar.setObjectName("menubar")
        
        
        self.actionvisual = QtWidgets.QAction(MainWindow)
        self.actionvisual.setObjectName("actionvisual")
        
        self.actionbuild = QtWidgets.QAction(MainWindow)
        self.actionvisual.setObjectName("actionbuild")
        
        self.actionclose = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("images/close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionclose.setIcon(icon2)
        self.actionclose.setObjectName("actionclose") 

        
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuFile.addAction(self.actionvisual)
        self.menuFile.addAction(self.actionbuild)
        self.menuFile.addAction(self.actionclose)
        self.menubar.addAction(self.menuFile.menuAction())
        
        
        
        self.menuOperation = QtWidgets.QMenu(self.menubar)
        self.menuOperation.setObjectName("menuOperation")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menuVASP = QtWidgets.QMenu(self.menu)

        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("images/vasp.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.menuVASP.setIcon(icon1)
        self.menuVASP.setObjectName("menuVASP")

        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        self.menu_4 = QtWidgets.QMenu(self.menubar)
        self.menu_4.setObjectName("menu_4")
        MainWindow.setMenuBar(self.menubar)

        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        # Toolbar close button

        self.toolBar.addAction(self.actionclose)

        self.actionband = QtWidgets.QAction(MainWindow)
        self.actionband.setObjectName("actionband")

        self.actionprojectionband = QtWidgets.QAction(MainWindow)
        self.actionprojectionband.setObjectName("actionprojectionband")

        self.actiondos = QtWidgets.QAction(MainWindow)
        self.actiondos.setObjectName("actiondos")

        self.actioninstruction = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("images/illustration.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actioninstruction.setIcon(icon3)
        self.actioninstruction.setObjectName("actioninstruction")

        self.actionabout = QtWidgets.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("images/about.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionabout.setIcon(icon4)
        self.actionabout.setObjectName("actionabout")

        self.actionsupercell = QtWidgets.QAction(MainWindow)
        self.actionsupercell.setObjectName("actionsupercell")

        self.actiondownload = QtWidgets.QAction(MainWindow)
        self.actiondownload.setObjectName("actiondownload")

        self.actionsetting = QtWidgets.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("images/setting.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionsetting.setIcon(icon5)
        self.actionsetting.setObjectName("actionsetting")

        self.actiontest = QtWidgets.QAction(MainWindow)
        self.actiontest.setObjectName("actiontest")


        self.actionbands = QtWidgets.QAction(MainWindow)
        self.actionbands.setObjectName("actionbands")

        self.actionscf = QtWidgets.QAction(MainWindow)
        self.actionscf.setObjectName("actionscf")

        self.actionscf_noncal = QtWidgets.QAction(MainWindow)
        self.actionscf_noncal.setObjectName("actionscf_noncal")

        self.actionband_noncal = QtWidgets.QAction(MainWindow)
        self.actionband_noncal.setObjectName("actionband_noncal")

        self.actionDOS = QtWidgets.QAction(MainWindow)
        self.actionDOS.setObjectName("actionDOS")

        self.actionphonon = QtWidgets.QAction(MainWindow)
        self.actionphonon.setObjectName("actionphonon")

        self.actionwannier = QtWidgets.QAction(MainWindow)
        self.actionwannier.setObjectName("actionwannier")

        self.actiontype_of_cell = QtWidgets.QAction(MainWindow)
        self.actiontype_of_cell.setObjectName("actiontype_of_cell")

        self.actionchgcar2D = QtWidgets.QAction(MainWindow)
        self.actionchgcar2D.setObjectName("actionchgcar2D")

        self.actionchgcar3D = QtWidgets.QAction(MainWindow)
        self.actionchgcar3D.setObjectName("actionchgcar3D")
        # Toolbar move up button
        self.actionup = QtWidgets.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("images/up.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionup.setIcon(icon6)
        self.actionup.setObjectName("actionup")
        self.toolBar.addAction(self.actionup)
        # Toolbar move down button
        self.actiondown = QtWidgets.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("images/down.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actiondown.setIcon(icon7)
        self.actiondown.setObjectName("actiondown")
        self.toolBar.addAction(self.actiondown)
        # Toolbar move left button
        self.actionleft = QtWidgets.QAction(MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("images/left.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionleft.setIcon(icon8)
        self.actionleft.setObjectName("actionleft")
        self.toolBar.addAction(self.actionleft)
        # Toolbar move right button
        self.actionright = QtWidgets.QAction(MainWindow)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("images/right.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionright.setIcon(icon9)
        self.actionright.setObjectName("actionright")
        self.toolBar.addAction(self.actionright)
        # Toolbar lineEdit input
        self.lineEdit = QtWidgets.QLineEdit(MainWindow)
        self.lineEdit.setFixedWidth(50)
        self.lineEdit.setText("0.01")
        self.lineEdit.setObjectName("lineEdit")
        self.toolBar.addWidget(self.lineEdit)
        # Toolbar doubleSpinBox input
#        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(MainWindow)
#        self.doubleSpinBox.setFixedWidth(55)
#        self.doubleSpinBox.setFixedHeight(25)
#        self.doubleSpinBox.setMinimum(-100.0)
#        self.doubleSpinBox.setMaximum(100.0)
#        self.doubleSpinBox.setSingleStep(1.0)
#        self.doubleSpinBox.setProperty("value", 1.0)
#        self.doubleSpinBox.setObjectName("doubleSpinBox")
#        self.toolBar.addWidget(self.doubleSpinBox)
        # Toolbar label unit
        self.label = QtWidgets.QLabel(MainWindow)
        self.label.setFixedWidth(50)
        self.label.setFixedHeight(20)
        self.label.setObjectName("label")
        
        #label_text = u'\u212B\u00B3'
        #d = label_text.decode('utf-8')
        self.label.setText(" Å")
        self.toolBar.addWidget(self.label)
        
        
        
        


        self.menuVASP.addAction(self.actionscf)
        self.menuVASP.addAction(self.actionscf_noncal)
        self.menuVASP.addAction(self.actionbands)
        self.menuVASP.addAction(self.actionband_noncal)
        self.menuVASP.addAction(self.actionDOS)
        self.menuVASP.addAction(self.actionphonon)
        self.menuVASP.addAction(self.actionwannier)
        
        self.menu.addAction(self.menuVASP.menuAction())
        self.menu.addAction(self.actiontest)

        self.menuOperation.addAction(self.actionband)
        self.menuOperation.addAction(self.actionprojectionband)
        self.menuOperation.addAction(self.actiondos)
        self.menuOperation.addAction(self.actionchgcar2D)
        self.menuOperation.addAction(self.actionchgcar3D)

        self.menu_4.addAction(self.actionsupercell)
        self.menu_4.addAction(self.actiontype_of_cell)
        self.menu_4.addAction(self.actiondownload)

        self.menu_2.addAction(self.actionsetting)

        self.menuHelp.addAction(self.actioninstruction)
        self.menuHelp.addAction(self.actionabout)

       
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menuOperation.menuAction())
        self.menubar.addAction(self.menu_4.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.actionclose.triggered.connect(MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Abinito Studio"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuOperation.setTitle(_translate("MainWindow", "Plot"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.menu.setTitle(_translate("MainWindow", "Calculation"))
        self.menuVASP.setTitle(_translate("MainWindow", "VASP"))
        self.menu_2.setTitle(_translate("MainWindow", "Settings"))
        self.menu_4.setTitle(_translate("MainWindow", "Tools"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        
        self.actionbuild.setText(_translate("MainWindow", "Build structure"))
        self.actionclose.setText(_translate("MainWindow", "Close"))
        self.actionband.setText(_translate("MainWindow", "Bands"))
        self.actionprojectionband.setText(_translate("MainWindow", "Projected Band"))
        self.actiondos.setText(_translate("MainWindow", "DOS"))
        self.actioninstruction.setText(_translate("MainWindow", "Instruction"))
        self.actionabout.setText(_translate("MainWindow", "About"))
        self.actionsupercell.setText(_translate("MainWindow", "Supercell"))
        self.actiondownload.setText(_translate("MainWindow", "Download"))
        self.actionsetting.setText(_translate("MainWindow", "Node Connection"))
        self.actiontest.setText(_translate("MainWindow", "Pyxtal"))
        self.actionvisual.setText(_translate("MainWindow", "Open POSCAR"))
        self.actionbands.setText(_translate("MainWindow", "band"))
        self.actionscf.setText(_translate("MainWindow", "scf"))
        self.actionscf_noncal.setText(_translate("MainWindow", "scf_noncal"))
        self.actionband_noncal.setText(_translate("MainWindow", "band_noncal"))
        self.actionDOS.setText(_translate("MainWindow", "DOS"))
        self.actionphonon.setText(_translate("MainWindow", "phonon"))
        self.actionwannier.setText(_translate("MainWindow", "wannier"))
        self.actiontype_of_cell.setText(_translate("MainWindow", "Type of cell"))
        self.actionchgcar2D.setText(_translate("MainWindow", "CHGCAR 2D"))
        self.actionchgcar3D.setText(_translate("MainWindow", "CHGCAR 3D"))
        self.actionup.setText(_translate("MainWindow", "up"))
        self.actiondown.setText(_translate("MainWindow", "down"))
        self.actionleft.setText(_translate("MainWindow", "left"))
        self.actionright.setText(_translate("MainWindow", "right"))
