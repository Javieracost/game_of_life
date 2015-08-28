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


class Grid(QGraphicsScene):
	def __init__(self, tileSize):
		super(Grid, self).__init__()
		self.started = False
		self.running = False
		self.tileSize = tileSize
		self.qpen = QPen()
		self.dead = QBrush(Qt.white)
		self.alive = QBrush(Qt.black)
		for pos in range(0, 410, self.tileSize):
			self.addLine(pos, 0, pos, 400, self.qpen)
			self.addLine(0, pos, 400, pos, self.qpen)
		for x in range(40):
			for y in range(40):
				last = self.addRect(QRect(x*self.tileSize, y*self.tileSize, self.tileSize, self.tileSize), self.qpen, self.dead)
		#test
		last.setBrush(self.alive)

	def cells(self):
		return [item for item in self.items() if isinstance(item, QGraphicsRectItem)]

	def mousePressEvent(self,e):
		clicked = self.itemAt(e.scenePos())
		self.toggle(clicked)

	def toggle(self, cell):
		newState = (1 if cell.brush() == self.dead else 0)
		self.setCell(cell, newState)


	def setCell(self, cell, alive):
		state = (self.alive if alive else self.dead)
		cell.setBrush(state)

	def restart(self):
		for c in self.cells():
			self.setCell(c, 0)
		self.running = False
		self.started = False
		print "--Game Restarted--"

	def startGame(self):
		self.threads = [ GameThread(self, q) for q in range(4) ]
		for t in self.threads:
			t.start()
		self.started = True
		print "Game Started!"

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
		
class Window(QMainWindow):
	def __init__(self,ui):
		super(Window, self).__init__()
		self.ui = ui
		self.ui.setupUi(self)
		self.setFixedSize(420,440)
		self.scene = Grid(10)
		self.ui.graphicsView.setScene(self.scene)
		self.ui.actionClose.setShortcut('q')
		self.ui.actionClose.triggered.connect(qApp.quit)
		self.ui.actionRestart.setShortcut('r')
		self.ui.actionRestart.triggered.connect(self.scene.restart)
		self.ui.actionToggle.setShortcut(' ')
		self.ui.actionToggle.triggered.connect(self.scene.toggleRun)

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