# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'plot_options.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Plot_Options(object):
    def setupUi(self, Plot_Options):
        Plot_Options.setObjectName("Plot_Options")
        Plot_Options.resize(400, 283)
        self.gridLayout = QtWidgets.QGridLayout(Plot_Options)
        self.gridLayout.setObjectName("gridLayout")
        self.checkBox_log_y2 = QtWidgets.QCheckBox(Plot_Options)
        self.checkBox_log_y2.setObjectName("checkBox_log_y2")
        self.gridLayout.addWidget(self.checkBox_log_y2, 2, 0, 1, 1)
        self.checkBox_use_abs_x = QtWidgets.QCheckBox(Plot_Options)
        self.checkBox_use_abs_x.setEnabled(False)
        self.checkBox_use_abs_x.setObjectName("checkBox_use_abs_x")
        self.gridLayout.addWidget(self.checkBox_use_abs_x, 0, 1, 1, 1)
        self.checkBox_log_x = QtWidgets.QCheckBox(Plot_Options)
        self.checkBox_log_x.setObjectName("checkBox_log_x")
        self.gridLayout.addWidget(self.checkBox_log_x, 0, 0, 1, 1)
        self.checkBox_use_abs_y = QtWidgets.QCheckBox(Plot_Options)
        self.checkBox_use_abs_y.setEnabled(False)
        self.checkBox_use_abs_y.setObjectName("checkBox_use_abs_y")
        self.gridLayout.addWidget(self.checkBox_use_abs_y, 1, 1, 1, 1)
        self.checkBox_log_y = QtWidgets.QCheckBox(Plot_Options)
        self.checkBox_log_y.setObjectName("checkBox_log_y")
        self.gridLayout.addWidget(self.checkBox_log_y, 1, 0, 1, 1)
        self.checkBox_use_abs_y2 = QtWidgets.QCheckBox(Plot_Options)
        self.checkBox_use_abs_y2.setEnabled(False)
        self.checkBox_use_abs_y2.setObjectName("checkBox_use_abs_y2")
        self.gridLayout.addWidget(self.checkBox_use_abs_y2, 2, 1, 1, 1)
        self.tableWidget = QtWidgets.QTableWidget(Plot_Options)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.gridLayout.addWidget(self.tableWidget, 3, 0, 1, 2)

        self.retranslateUi(Plot_Options)
        QtCore.QMetaObject.connectSlotsByName(Plot_Options)

    def retranslateUi(self, Plot_Options):
        _translate = QtCore.QCoreApplication.translate
        Plot_Options.setWindowTitle(_translate("Plot_Options", "Form"))
        self.checkBox_log_y2.setText(_translate("Plot_Options", "Y-Axis 2 logarithmic"))
        self.checkBox_use_abs_x.setText(_translate("Plot_Options", "Use Absolute"))
        self.checkBox_log_x.setText(_translate("Plot_Options", "X-Axis logarithmic"))
        self.checkBox_use_abs_y.setText(_translate("Plot_Options", "Use Absolute"))
        self.checkBox_log_y.setText(_translate("Plot_Options", "Y-Axis logarithmic"))
        self.checkBox_use_abs_y2.setText(_translate("Plot_Options", "Use Absolute"))

