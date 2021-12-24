# GUI application main program entry
import sys
from PyQt5.QtWidgets import QApplication, QSplashScreen
from PyQt5 import QtGui, QtCore, QtWidgets

QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
app = QApplication(sys.argv)  # Create GUI application
splash = QSplashScreen(QtGui.QPixmap("images\startup.jpg"))
splash.showMessage("The program is loading, please wait...",
                   QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom,
                   QtCore.Qt.black)
splash.show()  # Display the startup interface
QtWidgets.qApp.processEvents()  # Handling main process events
from abinitostudio.myMainWindow import MainWindow

mainform = MainWindow()  # Create the main form
mainform.showMaximized()  # Maximize window
mainform.show()  # Display the main form
splash.finish(mainform)  # Hide the startup interface
sys.exit(app.exec_())
