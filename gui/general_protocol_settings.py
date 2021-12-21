# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'general_protocol_settings.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Protocol_Settings(object):
    def setupUi(self, Protocol_Settings):
        Protocol_Settings.setObjectName("Protocol_Settings")
        Protocol_Settings.resize(397, 674)
        self.gridLayout = QtWidgets.QGridLayout(Protocol_Settings)
        self.gridLayout.setObjectName("gridLayout")
        self.tableView_variables = QtWidgets.QTableView(Protocol_Settings)
        self.tableView_variables.setObjectName("tableView_variables")
        self.tableView_variables.verticalHeader().setVisible(False)
        self.gridLayout.addWidget(self.tableView_variables, 3, 0, 1, 4)
        self.pushButton_plot_setup = QtWidgets.QPushButton(Protocol_Settings)
        self.pushButton_plot_setup.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_plot_setup.setFont(font)
        self.pushButton_plot_setup.setObjectName("pushButton_plot_setup")
        self.gridLayout.addWidget(self.pushButton_plot_setup, 1, 0, 1, 4)
        self.label = QtWidgets.QLabel(Protocol_Settings)
        self.label.setMaximumSize(QtCore.QSize(60, 16777215))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.pushButton_add_variable = QtWidgets.QPushButton(Protocol_Settings)
        self.pushButton_add_variable.setMaximumSize(QtCore.QSize(30, 16777215))
        self.pushButton_add_variable.setObjectName("pushButton_add_variable")
        self.gridLayout.addWidget(self.pushButton_add_variable, 2, 2, 1, 1)
        self.pushButton_remove_variable = QtWidgets.QPushButton(Protocol_Settings)
        self.pushButton_remove_variable.setMaximumSize(QtCore.QSize(30, 16777215))
        self.pushButton_remove_variable.setObjectName("pushButton_remove_variable")
        self.gridLayout.addWidget(self.pushButton_remove_variable, 2, 3, 1, 1)
        self.label_2 = QtWidgets.QLabel(Protocol_Settings)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.lineEdit_filename = QtWidgets.QLineEdit(Protocol_Settings)
        self.lineEdit_filename.setObjectName("lineEdit_filename")
        self.gridLayout.addWidget(self.lineEdit_filename, 0, 1, 1, 3)

        self.retranslateUi(Protocol_Settings)
        QtCore.QMetaObject.connectSlotsByName(Protocol_Settings)

    def retranslateUi(self, Protocol_Settings):
        _translate = QtCore.QCoreApplication.translate
        Protocol_Settings.setWindowTitle(_translate("Protocol_Settings", "Form"))
        self.pushButton_plot_setup.setText(_translate("Protocol_Settings", "Plot Setup"))
        self.label.setText(_translate("Protocol_Settings", "Filename:"))
        self.pushButton_add_variable.setText(_translate("Protocol_Settings", "+"))
        self.pushButton_remove_variable.setText(_translate("Protocol_Settings", "-"))
        self.label_2.setText(_translate("Protocol_Settings", "Variables"))
        self.lineEdit_filename.setText(_translate("Protocol_Settings", "Datafile"))
        self.lineEdit_filename.setPlaceholderText(_translate("Protocol_Settings", "Filename"))

