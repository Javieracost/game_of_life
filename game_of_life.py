#!/usr/bin/python2

import sys

from PySide.QtCore import *
from PySide.QtGui import *

from window import Ui_MainWindow
from about import Ui_Dialog

class GameThread(QThread):

	def __init__(self, scene):
		QThread.__init__(self)
		self.scene = scene
		self.status = StatusObj()

	def run(self):
		alive, dead = self.scene.alive, self.scene.dead
		grid = self.scene.grid
		pending = [] #cells to be updated on the next gen
		generation = 0
		statMsgs = {True : "Running...", False : "Paused"}
		lastMsg = ""
		while not self.scene.finished:
			qApp.processEvents() #probably a hack
			if self.scene.running:
				generation += 1
				for i in range(len(grid)):
					for j in range(len(grid)):
						cell = grid[i][j]
						cellState = cell.brush()
						crowd = self.scene.countNeighbors(i,j)
						if cellState == dead and crowd == 3 or \
						cellState == alive and crowd not in range(2,4):
							#actual update should be done only after checking every cell
							pending.append(grid[i][j])
				while pending and self.scene.running:
					self.scene.toggle(pending.pop(0))
				self.status.updateG(generation)
			if self.scene.started and lastMsg != statMsgs[self.scene.running]:
				lastMsg = statMsgs[self.scene.running]
				self.status.updateS(lastMsg)
			if self.scene.restarted:
				pending = []
				generation = 0
				self.status.updateS("Ready!")
				self.status.updateG(generation)
				self.scene.restarted = False

class StatusObj(QObject):

	updateGen = Signal(int)
	updateStat = Signal(str)

	def __init__(self):
		QObject.__init__(self)

	def updateG(self, gen):
		self.updateGen.emit(gen)

	def updateS(self, newState):
		self.updateStat.emit(newState)

class Grid(QGraphicsScene):

	def __init__(self, tileSize):
		super(Grid, self).__init__()
		self.started = False
		self.finished = False
		self.running = False
		self.restarted = False
		self.tileSize = tileSize
		self.qpen = QPen()
		self.dead = QBrush(Qt.white)
		self.alive = QBrush(Qt.black)
		self.previousCell = None
		self.grid = []
		self.gameThread = GameThread(self)
		for x in range(40):
			row = []
			for y in range(40):
				xpos, ypos = [x*10, y*10]
				row.append(self.addRect(QRect(xpos, ypos, self.tileSize, self.tileSize), self.qpen, self.dead))
			self.grid.append(row)

	def cells(self):
		return [item for item in self.items() if isinstance(item, QGraphicsRectItem)]

	def mouseDoubleClickEvent(self,e):
		selected = self.itemAt(e.scenePos())
		self.toggle(selected)

	def mouseReleaseEvent(self,e):
		self.previousCell = None

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
		self.running = False
		self.restarted = True
		for c in self.cells():
			self.setCell(c, 0)

	def startGame(self):
		self.gameThread.start()
		self.started = True

	def toggleRun(self):
		if not self.started:
			self.startGame()
		self.running = not self.running

	def quit(self):
		self.finished = True
		if self.started:
			self.gameThread.wait()

class Window(QMainWindow):

	def __init__(self,ui):
		super(Window, self).__init__()
		self.ui = ui
		self.ui.setupUi(self)
		self.setFixedSize(420,460)
		self.scene = Grid(10)
		self.statusLabel = QLabel()
		self.statusLabel.setText("Ready!")
		self.generationLabel = QLabel()
		self.ui.statusBar.addPermanentWidget(self.statusLabel, 1)
		self.ui.statusBar.addPermanentWidget(self.generationLabel, 1)
		self.ui.graphicsView.setScene(self.scene)
		self.ui.actionClose.setShortcut('q')
		self.ui.actionClose.triggered.connect(lambda: self.closeEvent(None))
		self.ui.actionRestart.setShortcut('r')
		self.ui.actionRestart.triggered.connect(self.scene.restart)
		self.ui.actionToggle.setShortcut(' ')
		self.ui.actionToggle.triggered.connect(self.scene.toggleRun)
		self.ui.actionAbout.triggered.connect(self.aboutDiag)
		self.scene.gameThread.status.updateGen.connect(self.generationUpdate)
		self.scene.gameThread.status.updateStat.connect(self.statusUpdate)

	def aboutDiag(self):
		dialog = QDialog()
		dialog.ui = Ui_Dialog()
		dialog.ui.setupUi(dialog)
		dialog.setAttribute(Qt.WA_DeleteOnClose)
		dialog.exec_()



	def center(self):
		frameGm = self.frameGeometry()
		screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
		centerPoint = QApplication.desktop().screenGeometry(screen).center()
		frameGm.moveCenter(centerPoint)
		self.move(frameGm.topLeft())

	@Slot(str)
	def statusUpdate(self,newState):
		self.statusLabel.setText(newState)

	@Slot(int)
	def generationUpdate(self,gen):
		txt = "Generation: " + str(gen)
		if not gen:
			txt = ""
		self.generationLabel.setText(txt)


	def closeEvent(self, e):
		self.scene.quit()
		qt_app.quit()

qt_app = QApplication(sys.argv)
window = Window(Ui_MainWindow())
window.center()
window.show()
sys.exit(qt_app.exec_())