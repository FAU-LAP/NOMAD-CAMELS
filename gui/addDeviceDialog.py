# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'addDeviceDialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog_Add_Device(object):
    def setupUi(self, Dialog_Add_Device):
        Dialog_Add_Device.setObjectName("Dialog_Add_Device")
        Dialog_Add_Device.resize(861, 544)
        self.gridLayout_2 = QtWidgets.QGridLayout(Dialog_Add_Device)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pushButton_update_drivers = QtWidgets.QPushButton(Dialog_Add_Device)
        self.pushButton_update_drivers.setEnabled(False)
        self.pushButton_update_drivers.setObjectName("pushButton_update_drivers")
        self.gridLayout_2.addWidget(self.pushButton_update_drivers, 6, 1, 1, 2)
        self.treeView_devices = QtWidgets.QTreeView(Dialog_Add_Device)
        self.treeView_devices.setObjectName("treeView_devices")
        self.gridLayout_2.addWidget(self.treeView_devices, 1, 0, 7, 1)
        self.progressBar = QtWidgets.QProgressBar(Dialog_Add_Device)
        self.progressBar.setEnabled(False)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout_2.addWidget(self.progressBar, 7, 1, 1, 2)
        self.pushButton_install_update_selected = QtWidgets.QPushButton(Dialog_Add_Device)
        self.pushButton_install_update_selected.setEnabled(False)
        self.pushButton_install_update_selected.setObjectName("pushButton_install_update_selected")
        self.gridLayout_2.addWidget(self.pushButton_install_update_selected, 5, 1, 1, 2)
        self.pushButton_update_driver_list = QtWidgets.QPushButton(Dialog_Add_Device)
        self.pushButton_update_driver_list.setObjectName("pushButton_update_driver_list")
        self.gridLayout_2.addWidget(self.pushButton_update_driver_list, 4, 1, 1, 2)
        self.label_2 = QtWidgets.QLabel(Dialog_Add_Device)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 2, 1, 1, 1)
        self.lineEdit_search_tags = QtWidgets.QLineEdit(Dialog_Add_Device)
        self.lineEdit_search_tags.setMaximumSize(QtCore.QSize(250, 16777215))
        self.lineEdit_search_tags.setObjectName("lineEdit_search_tags")
        self.gridLayout_2.addWidget(self.lineEdit_search_tags, 2, 2, 1, 1)
        self.label = QtWidgets.QLabel(Dialog_Add_Device)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 1, 1, 1, 1)
        self.pushButton_activate_selected = QtWidgets.QPushButton(Dialog_Add_Device)
        self.pushButton_activate_selected.setObjectName("pushButton_activate_selected")
        self.gridLayout_2.addWidget(self.pushButton_activate_selected, 3, 1, 1, 2)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog_Add_Device)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout_2.addWidget(self.buttonBox, 8, 0, 1, 3)
        self.lineEdit_search_name = QtWidgets.QLineEdit(Dialog_Add_Device)
        self.lineEdit_search_name.setMaximumSize(QtCore.QSize(250, 16777215))
        self.lineEdit_search_name.setObjectName("lineEdit_search_name")
        self.gridLayout_2.addWidget(self.lineEdit_search_name, 1, 2, 1, 1)

        self.retranslateUi(Dialog_Add_Device)
        self.buttonBox.rejected.connect(Dialog_Add_Device.reject)
        self.buttonBox.accepted.connect(Dialog_Add_Device.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog_Add_Device)

    def retranslateUi(self, Dialog_Add_Device):
        _translate = QtCore.QCoreApplication.translate
        Dialog_Add_Device.setWindowTitle(_translate("Dialog_Add_Device", "Dialog"))
        self.pushButton_update_drivers.setText(_translate("Dialog_Add_Device", "Update all installed drivers"))
        self.pushButton_install_update_selected.setText(_translate("Dialog_Add_Device", "Install / Update Selected"))
        self.pushButton_update_driver_list.setText(_translate("Dialog_Add_Device", "Update device-list"))
        self.label_2.setText(_translate("Dialog_Add_Device", "Search tags:"))
        self.lineEdit_search_tags.setPlaceholderText(_translate("Dialog_Add_Device", "tags"))
        self.label.setText(_translate("Dialog_Add_Device", "Search name:"))
        self.pushButton_activate_selected.setText(_translate("Dialog_Add_Device", "Add selected device"))
        self.lineEdit_search_name.setPlaceholderText(_translate("Dialog_Add_Device", "device name"))

