# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'graphic.ui'
#
# Created: Tue Aug 25 01:00:26 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(420, 420)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtGui.QWidget(MainWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.graphicsView = QtGui.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(0, 0, 420, 420))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsView.sizePolicy().hasHeightForWidth())
        self.graphicsView.setSizePolicy(sizePolicy)
        self.graphicsView.setSceneRect(QtCore.QRectF(0.0, 0.0, 400.0, 400.0))
        self.graphicsView.setObjectName("graphicsView")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 420, 20))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.actionRestart = QtGui.QAction(MainWindow)
        self.actionRestart.setObjectName("actionRestart")
        self.actionPause = QtGui.QAction(MainWindow)
        self.actionPause.setObjectName("actionPause")
        self.actionResume = QtGui.QAction(MainWindow)
        self.actionResume.setEnabled(False)
        self.actionResume.setObjectName("actionResume")
        self.actionClose = QtGui.QAction(MainWindow)
        self.actionClose.setObjectName("actionClose")
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionStart = QtGui.QAction(MainWindow)
        self.actionStart.setObjectName("actionStart")
        self.menuFile.addAction(self.actionStart)
        self.menuFile.addAction(self.actionRestart)
        self.menuFile.addAction(self.actionPause)
        self.menuFile.addAction(self.actionResume)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionClose)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Conway\'s Game of Life", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("MainWindow", "&Help", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRestart.setText(QtGui.QApplication.translate("MainWindow", "Restart", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRestart.setToolTip(QtGui.QApplication.translate("MainWindow", "Clear all tiles", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPause.setText(QtGui.QApplication.translate("MainWindow", "Pause", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPause.setToolTip(QtGui.QApplication.translate("MainWindow", "Pause game", None, QtGui.QApplication.UnicodeUTF8))
        self.actionResume.setText(QtGui.QApplication.translate("MainWindow", "Resume", None, QtGui.QApplication.UnicodeUTF8))
        self.actionResume.setToolTip(QtGui.QApplication.translate("MainWindow", "Resume paused game", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClose.setText(QtGui.QApplication.translate("MainWindow", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setText(QtGui.QApplication.translate("MainWindow", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.actionStart.setText(QtGui.QApplication.translate("MainWindow", "Start", None, QtGui.QApplication.UnicodeUTF8))
        self.actionStart.setToolTip(QtGui.QApplication.translate("MainWindow", "Start Game", None, QtGui.QApplication.UnicodeUTF8))

