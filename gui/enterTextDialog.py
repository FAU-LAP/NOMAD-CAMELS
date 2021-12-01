# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'enterTextDialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_EnterTextDialog(object):
    def setupUi(self, EnterTextDialog):
        EnterTextDialog.setObjectName("EnterTextDialog")
        EnterTextDialog.resize(278, 106)
        self.gridLayout_2 = QtWidgets.QGridLayout(EnterTextDialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.lineEdit_text = QtWidgets.QLineEdit(EnterTextDialog)
        self.lineEdit_text.setObjectName("lineEdit_text")
        self.gridLayout.addWidget(self.lineEdit_text, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(EnterTextDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(EnterTextDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout_2.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(EnterTextDialog)
        self.buttonBox.accepted.connect(EnterTextDialog.accept)
        self.buttonBox.rejected.connect(EnterTextDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(EnterTextDialog)

    def retranslateUi(self, EnterTextDialog):
        _translate = QtCore.QCoreApplication.translate
        EnterTextDialog.setWindowTitle(_translate("EnterTextDialog", "Dialog"))
        self.label.setText(_translate("EnterTextDialog", "Task name:"))

