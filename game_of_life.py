#!/usr/bin/python2

import sys
from time import time, clock
from random import choice

from PySide.QtCore import *
from PySide.QtGui import *

from window import Ui_MainWindow
from pprint import pprint

class GameThread(QThread):

	def __init__(self, scene):
		QThread.__init__(self)
		self.scene = scene
		self.lastUpdate = clock()

	def run(self):
		alive, dead = self.scene.alive, self.scene.dead
		grid = self.scene.grid
		while not self.scene.finished:
			qApp.processEvents() #probably a hack
			if self.scene.running and (clock()-self.lastUpdate) > 0.05:
				for i in range(len(grid)):
					for j in range(len(grid)):
						cell = grid[i][j]
						cellState = cell.brush()
						crowd = self.scene.countNeighbors(i,j)
						if cellState == dead and crowd == 3 or \
						cellState == alive and crowd not in range(2,4):
							self.scene.toggle(cell)
				self.lastUpdate = clock()

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
		self.grid = []
		for x in range(40):
			row = []
			for y in range(40):
				xpos, ypos = [x*10, y*10]
				row.append(self.addRect(QRect(xpos, ypos, self.tileSize, self.tileSize), self.qpen, self.dead))
				#cell.setToolTip("coords: %d,%d"%(xpos,ypos,))
			self.grid.append(row)

	def cells(self):
		return [item for item in self.items() if isinstance(item, QGraphicsRectItem)]

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

	def countNeighbors(self, x, y):
		amt = 0
		for xOff in range(-1, 2):
			xpos = x + xOff
			if xpos not in range(len(self.grid)): continue
			for yOff in range(-1, 2):
				ypos = y + yOff
				if ypos not in range(len(self.grid)) or (x,y) == (xpos, ypos):
					continue
				if self.grid[xpos][ypos].brush() == self.alive:
					amt += 1
		return amt

	def restart(self):
		for c in self.cells():
			self.setCell(c, 0)
		self.running = False
		print "Game Restarted"

	def startGame(self):
		self.gameThread = GameThread(self)
		self.gameThread.start()
		self.started = True

	def toggleRun(self):
		state = {True: "Started", False: "Paused"}
		if not self.started:
			self.startGame()
		self.running = not self.running
		print "Game "+state[self.running]


	def quit(self):
		self.finished = True
		if self.started:
				self.gameThread.wait()

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
		self.scene.quit()
		qt_app.quit()

qt_app = QApplication(sys.argv)
window = Window(Ui_MainWindow())
window.center()
window.show()
sys.exit(qt_app.exec_())