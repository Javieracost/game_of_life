#!/usr/bin/python2

import sys

from PySide.QtCore import *
from PySide.QtGui import *
from window import Ui_MainWindow

from time import sleep


#!TODO: Add an abstraction layer between the graphicscene and the game grid

class Window(QMainWindow, QWidget):
	def __init__(self,ui):
		super(Window, self).__init__()
		self.ui = ui
		self.ui.setupUi(self)
		self.setFixedSize(420,440)
		self.tileSize = 10
		self.scene = QGraphicsScene(QRectF(0, 0, 400, 400))
		self.ui.graphicsView.setScene(self.scene)
		self.colorPen = QPen(Qt.black)
		self.whitePen = QPen(Qt.white)
		for i in xrange(0, 410, self.tileSize):
			self.scene.addLine(i, 0, i, 400, self.colorPen)
			self.scene.addLine(0, i, 400, i, self.colorPen)
		for i in xrange(20):
			self.turn(1, i, i)

	def center(self):
		frameGm = self.frameGeometry()
		screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
		centerPoint = QApplication.desktop().screenGeometry(screen).center()
		frameGm.moveCenter(centerPoint)
		self.move(frameGm.topLeft())

	def turn(self, alive, x, y):
		"""Sets the tile at x,y coordinates to the given state's color"""
		if alive:
			pen = self.colorPen
		else:
			pen = self.whitePen
		self.scene.addRect(QRect(x*self.tileSize, y*self.tileSize, self.tileSize, self.tileSize), pen, QBrush(Qt.SolidPattern))

	def restart(self):
		#!TODO Update relevant menu buttons 
		for i in xrange(40):
			for j in xrange(40):
				self.turn(0, i, j)

	def keyPressEvent(self, e):
		if e.key() == Qt.Key_Q:
			self.close()
		elif e.key() == Qt.Key_R:
			self.restart()

qt_app = QApplication(sys.argv)
window = Window(Ui_MainWindow())
window.center()
window.show()
# Run the application's event loop
sys.exit(qt_app.exec_())