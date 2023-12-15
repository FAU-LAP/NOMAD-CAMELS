# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'device_installer.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHeaderView, QLabel,
    QLineEdit, QProgressBar, QPushButton, QSizePolicy,
    QTableWidget, QTableWidgetItem, QTextEdit, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(679, 481)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.textEdit_device_info = QTextEdit(Form)
        self.textEdit_device_info.setObjectName(u"textEdit_device_info")
        self.textEdit_device_info.setEnabled(True)
        self.textEdit_device_info.setTextInteractionFlags(Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)

        self.gridLayout.addWidget(self.textEdit_device_info, 1, 2, 5, 1)

        self.pushButton_update_drivers = QPushButton(Form)
        self.pushButton_update_drivers.setObjectName(u"pushButton_update_drivers")
        self.pushButton_update_drivers.setEnabled(True)
        self.pushButton_update_drivers.setStyleSheet(u"QPushButton {\n"
"                                background-color: #2a4cdf; \n"
"                                color: white; \n"
"                                border: none; \n"
"                                padding: 2px 10px; \n"
"                                text-align: center; \n"
"                                text-decoration: none; \n"
"                                font-size: 13px; \n"
"                                margin: 2px 2px; \n"
"                                border-radius: 6px;\n"
"								font-weight: bold;\n"
"                            }\n"
"\n"
"                            QPushButton:hover {\n"
"                                background-color: #1a3cbf;\n"
"                            }")

        self.gridLayout.addWidget(self.pushButton_update_drivers, 7, 0, 1, 1)

        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.pushButton_sel_none = QPushButton(Form)
        self.pushButton_sel_none.setObjectName(u"pushButton_sel_none")
        self.pushButton_sel_none.setStyleSheet(u"QPushButton {\n"
"        background-color: #bf8a36;\n"
"        color: white;\n"
"        border: none;\n"
"        padding: 2px 10px;\n"
"        text-align: center;\n"
"        text-decoration: none;\n"
"        font-size: 13px;\n"
"        margin: 2px 2px;\n"
"        border-radius: 6px;\n"
"        font-weight: bold;\n"
"    }\n"
"\n"
"    QPushButton:hover {\n"
"        background-color: #8a5a23;\n"
"    }")

        self.gridLayout.addWidget(self.pushButton_sel_none, 2, 1, 1, 1)

        self.pushButton_uninstall = QPushButton(Form)
        self.pushButton_uninstall.setObjectName(u"pushButton_uninstall")
        self.pushButton_uninstall.setEnabled(True)
        self.pushButton_uninstall.setStyleSheet(u"QPushButton {\n"
"                background-color: #E60000; \n"
"                color: white; \n"
"                                border: none; \n"
"                                padding: 2px 10px; \n"
"                                text-align: center; \n"
"                                text-decoration: none; \n"
"                                font-size: 13px; \n"
"                                margin: 2px 2px; \n"
"                                border-radius: 6px;\n"
"								font-weight: bold;\n"
"                            }\n"
"\n"
"            QPushButton:hover {\n"
"                background-color: #B22222;\n"
"            }")

        self.gridLayout.addWidget(self.pushButton_uninstall, 6, 1, 1, 1)

        self.pushButton_install_update_selected = QPushButton(Form)
        self.pushButton_install_update_selected.setObjectName(u"pushButton_install_update_selected")
        self.pushButton_install_update_selected.setEnabled(True)
        self.pushButton_install_update_selected.setStyleSheet(u"QPushButton {\n"
"                                background-color: #2a4cdf; \n"
"                                color: white; \n"
"                                border: none; \n"
"                                padding: 2px 10px; \n"
"                                text-align: center; \n"
"                                text-decoration: none; \n"
"                                font-size: 13px; \n"
"                                margin: 2px 2px; \n"
"                                border-radius: 6px;\n"
"								font-weight: bold;\n"
"                            }\n"
"\n"
"                            QPushButton:hover {\n"
"                                background-color: #1a3cbf;\n"
"                            }")

        self.gridLayout.addWidget(self.pushButton_install_update_selected, 6, 0, 1, 1)

        self.lineEdit_search_tags = QLineEdit(Form)
        self.lineEdit_search_tags.setObjectName(u"lineEdit_search_tags")
        self.lineEdit_search_tags.setMaximumSize(QSize(250, 16777215))

        self.gridLayout.addWidget(self.lineEdit_search_tags, 1, 1, 1, 1)

        self.pushButton_info = QPushButton(Form)
        self.pushButton_info.setObjectName(u"pushButton_info")
        self.pushButton_info.setStyleSheet(u"QPushButton {\n"
"        background-color: #bf8a36;\n"
"        color: white;\n"
"        border: none;\n"
"        padding: 2px 10px;\n"
"        text-align: center;\n"
"        text-decoration: none;\n"
"        font-size: 12px;\n"
"        margin: 2px 2px;\n"
"        border-radius: 6px;\n"
"        font-weight: bold;\n"
"    }\n"
"\n"
"    QPushButton:hover {\n"
"        background-color: #8a5a23;\n"
"    }")

        self.gridLayout.addWidget(self.pushButton_info, 6, 2, 1, 1)

        self.device_table = QTableWidget(Form)
        self.device_table.setObjectName(u"device_table")

        self.gridLayout.addWidget(self.device_table, 3, 0, 3, 2)

        self.pushButton_sel_all = QPushButton(Form)
        self.pushButton_sel_all.setObjectName(u"pushButton_sel_all")
        self.pushButton_sel_all.setStyleSheet(u"QPushButton {\n"
"    background-color: #2a4cdf; /* This is a lighter shade of blue */\n"
"    color: white;\n"
"    border: none;\n"
"    padding: 2px 10px;\n"
"    text-align: center;\n"
"    text-decoration: none;\n"
"    font-size: 13px;\n"
"    margin: 2px 2px;\n"
"    border-radius: 6px;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #1a3cbf; /* This is a darker shade of the lighter blue for hover effect */\n"
"}")

        self.gridLayout.addWidget(self.pushButton_sel_all, 2, 0, 1, 1)

        self.progressBar = QProgressBar(Form)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setEnabled(True)
        self.progressBar.setValue(0)
        self.progressBar.setInvertedAppearance(False)

        self.gridLayout.addWidget(self.progressBar, 0, 2, 1, 1)

        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.lineEdit_search_name = QLineEdit(Form)
        self.lineEdit_search_name.setObjectName(u"lineEdit_search_name")
        self.lineEdit_search_name.setMaximumSize(QSize(250, 16777215))

        self.gridLayout.addWidget(self.lineEdit_search_name, 0, 1, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.pushButton_update_drivers.setText(QCoreApplication.translate("Form", u"Update all installed drivers", None))
        self.label.setText(QCoreApplication.translate("Form", u"Search name:", None))
        self.pushButton_sel_none.setText(QCoreApplication.translate("Form", u"Select None", None))
        self.pushButton_uninstall.setText(QCoreApplication.translate("Form", u"Uninstall Selected", None))
        self.pushButton_install_update_selected.setText(QCoreApplication.translate("Form", u"Install / Update Selected", None))
        self.lineEdit_search_tags.setPlaceholderText(QCoreApplication.translate("Form", u"tags", None))
        self.pushButton_info.setText(QCoreApplication.translate("Form", u"hide info", None))
        self.pushButton_sel_all.setText(QCoreApplication.translate("Form", u"Select All", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Search tags:", None))
        self.lineEdit_search_name.setPlaceholderText(QCoreApplication.translate("Form", u"device name", None))
    # retranslateUi

