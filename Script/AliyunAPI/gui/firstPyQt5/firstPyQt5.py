# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'firstPyQt5.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_mainWindow(object):
    def __init__(self):
        mainWindow = None
        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.menubar = QtWidgets.QMenuBar(mainWindow)
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)

    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(631, 600)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton.setGeometry(QtCore.QRect(250, 130, 131, 61))
        font = QtGui.QFont()
        font.setPointSize(22)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        mainWindow.setCentralWidget(self.centralwidget)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 631, 22))
        self.menubar.setObjectName("menubar")
        mainWindow.setMenuBar(self.menubar)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(mainWindow)
        self.pushButton.clicked.connect(self.firstPyQt5_button_click)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "第一个PyQt5程序"))
        self.pushButton.setText(_translate("mainWindow", "点我弹框"))


    def firstPyQt5_button_click(self):
        QtWidgets.QMessageBox.information(self.pushButton, "标题", "这是第一个PyQt5 GUI程序")