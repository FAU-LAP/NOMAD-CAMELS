# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(375, 186)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_save_state = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_save_state.setObjectName("pushButton_save_state")
        self.gridLayout.addWidget(self.pushButton_save_state, 0, 1, 1, 1)
        self.pushButton_load_state = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_load_state.setObjectName("pushButton_load_state")
        self.gridLayout.addWidget(self.pushButton_load_state, 0, 2, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 375, 21))
        self.menubar.setObjectName("menubar")
        self.menuTask = QtWidgets.QMenu(self.menubar)
        self.menuTask.setObjectName("menuTask")
        self.menuAdd_Ons = QtWidgets.QMenu(self.menubar)
        self.menuAdd_Ons.setObjectName("menuAdd_Ons")
        self.menuDevices = QtWidgets.QMenu(self.menubar)
        self.menuDevices.setObjectName("menuDevices")
        self.menuPreferences = QtWidgets.QMenu(self.menubar)
        self.menuPreferences.setObjectName("menuPreferences")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actiontest = QtWidgets.QAction(MainWindow)
        self.actiontest.setObjectName("actiontest")
        self.menubar.addAction(self.menuTask.menuAction())
        self.menubar.addAction(self.menuAdd_Ons.menuAction())
        self.menubar.addAction(self.menuDevices.menuAction())
        self.menubar.addAction(self.menuPreferences.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_save_state.setText(_translate("MainWindow", "Save Current State"))
        self.pushButton_load_state.setText(_translate("MainWindow", "Load State"))
        self.menuTask.setTitle(_translate("MainWindow", "Task"))
        self.menuAdd_Ons.setTitle(_translate("MainWindow", "Add-Ons"))
        self.menuDevices.setTitle(_translate("MainWindow", "Devices"))
        self.menuPreferences.setTitle(_translate("MainWindow", "Preferences"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actiontest.setText(_translate("MainWindow", "test"))