# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'addDeviceDialog.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QGridLayout, QHeaderView, QLabel, QLineEdit,
    QProgressBar, QPushButton, QSizePolicy, QTextEdit,
    QTreeView, QWidget)

class Ui_Dialog_Add_Device(object):
    """ """
    def setupUi(self, Dialog_Add_Device):
        """

        Parameters
        ----------
        Dialog_Add_Device :
            

        Returns
        -------

        """
        if not Dialog_Add_Device.objectName():
            Dialog_Add_Device.setObjectName(u"Dialog_Add_Device")
        Dialog_Add_Device.resize(861, 544)
        self.gridLayout_2 = QGridLayout(Dialog_Add_Device)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.progressBar = QProgressBar(Dialog_Add_Device)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setEnabled(False)
        self.progressBar.setValue(0)
        self.progressBar.setInvertedAppearance(False)

        self.gridLayout_2.addWidget(self.progressBar, 7, 1, 1, 2)

        self.pushButton_update_drivers = QPushButton(Dialog_Add_Device)
        self.pushButton_update_drivers.setObjectName(u"pushButton_update_drivers")
        self.pushButton_update_drivers.setEnabled(False)

        self.gridLayout_2.addWidget(self.pushButton_update_drivers, 6, 1, 1, 2)

        self.pushButton_install_update_selected = QPushButton(Dialog_Add_Device)
        self.pushButton_install_update_selected.setObjectName(u"pushButton_install_update_selected")
        self.pushButton_install_update_selected.setEnabled(False)

        self.gridLayout_2.addWidget(self.pushButton_install_update_selected, 5, 1, 1, 2)

        self.pushButton_update_driver_list = QPushButton(Dialog_Add_Device)
        self.pushButton_update_driver_list.setObjectName(u"pushButton_update_driver_list")

        self.gridLayout_2.addWidget(self.pushButton_update_driver_list, 4, 1, 1, 2)

        self.lineEdit_search_tags = QLineEdit(Dialog_Add_Device)
        self.lineEdit_search_tags.setObjectName(u"lineEdit_search_tags")
        self.lineEdit_search_tags.setMaximumSize(QSize(250, 16777215))

        self.gridLayout_2.addWidget(self.lineEdit_search_tags, 2, 2, 1, 1)

        self.label = QLabel(Dialog_Add_Device)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 1, 1, 1, 1)

        self.pushButton_activate_selected = QPushButton(Dialog_Add_Device)
        self.pushButton_activate_selected.setObjectName(u"pushButton_activate_selected")

        self.gridLayout_2.addWidget(self.pushButton_activate_selected, 3, 1, 1, 2)

        self.label_2 = QLabel(Dialog_Add_Device)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 2, 1, 1, 1)

        self.lineEdit_search_name = QLineEdit(Dialog_Add_Device)
        self.lineEdit_search_name.setObjectName(u"lineEdit_search_name")
        self.lineEdit_search_name.setMaximumSize(QSize(250, 16777215))

        self.gridLayout_2.addWidget(self.lineEdit_search_name, 1, 2, 1, 1)

        self.buttonBox = QDialogButtonBox(Dialog_Add_Device)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout_2.addWidget(self.buttonBox, 9, 0, 1, 3)

        self.textEdit_device_info = QTextEdit(Dialog_Add_Device)
        self.textEdit_device_info.setObjectName(u"textEdit_device_info")
        self.textEdit_device_info.setEnabled(True)

        self.gridLayout_2.addWidget(self.textEdit_device_info, 8, 1, 1, 2)

        self.treeView_devices = QTreeView(Dialog_Add_Device)
        self.treeView_devices.setObjectName(u"treeView_devices")

        self.gridLayout_2.addWidget(self.treeView_devices, 1, 0, 8, 1)


        self.retranslateUi(Dialog_Add_Device)
        self.buttonBox.rejected.connect(Dialog_Add_Device.reject)
        self.buttonBox.accepted.connect(Dialog_Add_Device.accept)

        QMetaObject.connectSlotsByName(Dialog_Add_Device)
    # setupUi

    def retranslateUi(self, Dialog_Add_Device):
        """

        Parameters
        ----------
        Dialog_Add_Device :
            

        Returns
        -------

        """
        Dialog_Add_Device.setWindowTitle(QCoreApplication.translate("Dialog_Add_Device", u"Dialog", None))
        self.pushButton_update_drivers.setText(QCoreApplication.translate("Dialog_Add_Device", u"Update all installed drivers", None))
        self.pushButton_install_update_selected.setText(QCoreApplication.translate("Dialog_Add_Device", u"Install / Update Selected", None))
        self.pushButton_update_driver_list.setText(QCoreApplication.translate("Dialog_Add_Device", u"Update device-list", None))
        self.lineEdit_search_tags.setPlaceholderText(QCoreApplication.translate("Dialog_Add_Device", u"tags", None))
        self.label.setText(QCoreApplication.translate("Dialog_Add_Device", u"Search name:", None))
        self.pushButton_activate_selected.setText(QCoreApplication.translate("Dialog_Add_Device", u"Add selected device", None))
        self.label_2.setText(QCoreApplication.translate("Dialog_Add_Device", u"Search tags:", None))
        self.lineEdit_search_name.setPlaceholderText(QCoreApplication.translate("Dialog_Add_Device", u"device name", None))
    # retranslateUi

