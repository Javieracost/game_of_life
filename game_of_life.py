#!/usr/bin/python2

import sys

from PySide.QtCore import *
from PySide.QtGui import *

from window import Ui_MainWindow

class GameThread(QThread):
	def __init__(self, scene, quad):
		QThread.__init__(self)
		self.scene = scene
		self.quad = quad

	def run(self):
		print "created thread to work quadrant: "+str(self.quad)
		return

class Window(QMainWindow):
	def __init__(self,ui):
		super(Window, self).__init__()
		self.ui = ui
		self.ui.setupUi(self)
		self.setFixedSize(420,440)
		self.ui.actionClose.setShortcut('q')
		self.ui.actionClose.triggered.connect(qApp.quit)
		self.ui.actionRestart.setShortcut('r')
		self.ui.actionRestart.triggered.connect(self.restart)
		self.ui.actionToggle.setShortcut(' ')
		self.ui.actionToggle.triggered.connect(self.toggleRun)
		self.tileSize = 10
		self.scene = QGraphicsScene(QRectF(0, 0, 400, 400))
		self.ui.graphicsView.setScene(self.scene)
		self.qpen = QPen()
		for i in range(0, 410, self.tileSize):
			self.scene.addLine(i, 0, i, 400, self.qpen)
			self.scene.addLine(0, i, 400, i, self.qpen)
		self.started = False
		self.running = False
		
		#some test code
		for i in range(10):
			self.setCell(1, i, i)
		self.setCell(0,1,1)
		self.setCell(0,2,2)
		#for i in range(10):
		#	self.setCell(1, i, i)

	def center(self):
		frameGm = self.frameGeometry()
		screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
		centerPoint = QApplication.desktop().screenGeometry(screen).center()
		frameGm.moveCenter(centerPoint)
		self.move(frameGm.topLeft())

	def setCell(self, alive, x, y):
		"""Sets the cell at x,y to the given state's color"""
		xpos = x*self.tileSize
		ypos = y*self.tileSize
		brush = QBrush(Qt.SolidPattern)
		if not alive:
			brush.setColor(Qt.white)
		self.scene.addRect(QRect(xpos, ypos, self.tileSize, self.tileSize), self.qpen, brush)

	def getCell(self, x, y):
		"""Returns the state of the cell at x,y"""
		return ()

	def restart(self):
		for i in range(40):
			for j in range(40):
				self.setCell(0, i, j)
		self.running = False
		self.started = False
		print "--Game Restarted--"

	def toggleRun(self):
		print "Running status switched"
		if not self.started:
			self.startGame()
		if self.running:
			#pause code
			print "off!"
		else:
			print "on!"
			#start/resume code
		self.running = not self.running

	def startGame(self):
		self.threads = [ GameThread(self.scene, q) for q in range(4) ]
		for t in self.threads:
			t.start()
		self.started = True
		print "Game Started!"


qt_app = QApplication(sys.argv)
window = Window(Ui_MainWindow())
window.center()
window.show()
# Run the application's event loop
sys.exit(qt_app.exec_())