#!/usr/bin/python2

import sys

from PySide.QtCore import *
from PySide.QtGui import *
from window import Ui_MainWindow

class Window(QMainWindow):
	def __init__(self,ui):
		super(Window, self).__init__()
		self.ui = ui
		self.ui.setupUi(self)
	
	def center(self):
		frameGm = self.frameGeometry()
		screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
		centerPoint = QApplication.desktop().screenGeometry(screen).center()
		frameGm.moveCenter(centerPoint)
		self.move(frameGm.topLeft())


qt_app = QApplication(sys.argv)
window = Window(Ui_MainWindow())
window.center()
window.show()
 
# Run the application's event loop
sys.exit(qt_app.exec_())