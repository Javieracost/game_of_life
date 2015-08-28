#!/usr/bin/python2

import sys
from time import sleep,time
from random import choice

from PySide.QtCore import *
from PySide.QtGui import *

from window import Ui_MainWindow

class GameThread(QThread):
	def __init__(self, scene, quad):
		QThread.__init__(self)
		self.scene = scene
		self.quad = quad
		self.setWorkingArea()
		self.i = 0
		self.j = 0

	def setWorkingArea(self):
		qTopLeft = { 0 : (0,0) , 1 : (201,0) , 2 : (0,201), 3: (201,201) }
		topLeft = qTopLeft[self.quad]
		quadArea = QRect(topLeft[0], topLeft[1], 400/2, 400/2)
		#print "from a rect with topLeft in %d, %d that is %dx%d" % (topLeft[0], topLeft[1], 400/2, 400/2,)
		self.cells = [item for item in self.scene.items(quadArea) if isinstance(item, QGraphicsRectItem)]

	def run(self):
		while not self.scene.finished:
			if self.scene.running:
				for c in self.cells:
					self.scene.setCell(c, choice([0,1]))
				sleep(3)
				self.i +=1
				#print "thread running..."+str(self.i)
				continue
			#self.j +=1
			#print "thread paused..."+str(self.j)
		print "thread finished"



class Grid(QGraphicsScene):
	def __init__(self, tileSize):
		super(Grid, self).__init__()
		self.started = False
		self.finished = False
		self.running = False
		self.tileSize = tileSize
		self.qpen = QPen()
		self.dead = QBrush(Qt.white)
		self.alive = QBrush(Qt.black)
		self.previousCell = None
		for pos in range(0, 410, self.tileSize):
			self.addLine(pos, 0, pos, 400, self.qpen)
			self.addLine(0, pos, 400, pos, self.qpen)
		for x in range(40):
			for y in range(40):
				last = self.addRect(QRect(x*self.tileSize, y*self.tileSize, self.tileSize, self.tileSize), self.qpen, self.dead)

	def cells(self):
		return [item for item in self.items() if isinstance(item, QGraphicsRectItem)]

	def mousePressEvent(self,e):
		clicked = self.itemAt(e.scenePos())
		if isinstance(clicked, QGraphicsRectItem):
			self.toggle(clicked)

	def mouseMoveEvent(self,e):
		selected = self.itemAt(e.scenePos())
		if selected != self.previousCell and isinstance(selected, QGraphicsRectItem):
			self.previousCell = selected
			self.toggle(selected)

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
		print "--Game Restarted--"

	def startGame(self):
		self.threads = [ GameThread(self, q) for q in range(1) ]
		for t in self.threads:
			t.start()
		self.started = True
		print "Game Started!"

	def toggleRun(self):
		print "Running status switched"
		if not self.started:
			self.startGame()
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
		self.ui.actionClose.triggered.connect(lambda: self.closeEvent(None))
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

	def closeEvent(self, e):
		self.scene.finished = True
		if self.scene.started:
			for t in self.scene.threads:
				t.wait()
		qt_app.quit()


qt_app = QApplication(sys.argv)
window = Window(Ui_MainWindow())
window.center()
window.show()
# Run the application's event loop
sys.exit(qt_app.exec_())