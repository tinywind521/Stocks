# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_20170809.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(872, 552)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(770, 10, 81, 31))
        self.pushButton.setObjectName("pushButton")
        self.gnWidget = QtWidgets.QListWidget(Form)
        self.gnWidget.setGeometry(QtCore.QRect(290, 310, 331, 221))
        self.gnWidget.setObjectName("gnWidget")
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setGeometry(QtCore.QRect(630, 50, 221, 481))
        self.tableWidget.setLineWidth(1)
        self.tableWidget.setMidLineWidth(1)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(0, 1, item)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.hyWidget = QtWidgets.QListWidget(Form)
        self.hyWidget.setGeometry(QtCore.QRect(290, 50, 331, 221))
        self.hyWidget.setObjectName("hyWidget")
        self.clWidget = QtWidgets.QListWidget(Form)
        self.clWidget.setGeometry(QtCore.QRect(20, 50, 261, 481))
        self.clWidget.setObjectName("clWidget")
        self.clLabel = QtWidgets.QLabel(Form)
        self.clLabel.setGeometry(QtCore.QRect(30, 20, 71, 16))
        self.clLabel.setObjectName("clLabel")
        self.hyLabel = QtWidgets.QLabel(Form)
        self.hyLabel.setGeometry(QtCore.QRect(300, 21, 71, 20))
        self.hyLabel.setObjectName("hyLabel")
        self.gnLabel = QtWidgets.QLabel(Form)
        self.gnLabel.setGeometry(QtCore.QRect(300, 281, 71, 20))
        self.gnLabel.setObjectName("gnLabel")
        self.tableWidget.raise_()
        self.pushButton.raise_()
        self.gnWidget.raise_()
        self.hyWidget.raise_()
        self.clWidget.raise_()
        self.clLabel.raise_()
        self.hyLabel.raise_()
        self.gnLabel.raise_()

        self.retranslateUi(Form)
        self.pushButton.clicked.connect(Form.reload)
        self.gnWidget.itemClicked['QListWidgetItem*'].connect(Form.selectGN)
        self.hyWidget.itemClicked['QListWidgetItem*'].connect(Form.selectHY)
        self.clWidget.itemSelectionChanged.connect(Form.selectCL)
        self.pushButton.clicked.connect(self.hyWidget.clear)
        self.pushButton.clicked.connect(self.gnWidget.clear)
        self.hyWidget.clicked['QModelIndex'].connect(self.gnWidget.clearSelection)
        self.gnWidget.clicked['QModelIndex'].connect(self.hyWidget.clearSelection)
        self.clWidget.clicked['QModelIndex'].connect(Form.clickCL)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "读取…"))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("Form", "0"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "代码"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "名称"))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.setSortingEnabled(__sortingEnabled)
        self.clLabel.setText(_translate("Form", "模版列表"))
        self.hyLabel.setText(_translate("Form", "行业列表"))
        self.gnLabel.setText(_translate("Form", "概念列表"))

