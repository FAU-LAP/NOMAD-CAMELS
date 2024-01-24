# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'add_on_manager.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHeaderView, QLabel,
    QLineEdit, QProgressBar, QPushButton, QSizePolicy,
    QTableWidget, QTableWidgetItem, QTextEdit, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(400, 300)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.lineEdit_search_name = QLineEdit(Form)
        self.lineEdit_search_name.setObjectName(u"lineEdit_search_name")
        self.lineEdit_search_name.setMaximumSize(QSize(250, 16777215))

        self.gridLayout.addWidget(self.lineEdit_search_name, 0, 1, 1, 1)

        self.pushButton_install_update_selected = QPushButton(Form)
        self.pushButton_install_update_selected.setObjectName(u"pushButton_install_update_selected")
        self.pushButton_install_update_selected.setEnabled(True)

        self.gridLayout.addWidget(self.pushButton_install_update_selected, 0, 2, 1, 1)

        self.pushButton_uninstall = QPushButton(Form)
        self.pushButton_uninstall.setObjectName(u"pushButton_uninstall")
        self.pushButton_uninstall.setEnabled(True)

        self.gridLayout.addWidget(self.pushButton_uninstall, 1, 2, 1, 1)

        self.progressBar = QProgressBar(Form)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setEnabled(True)
        self.progressBar.setValue(0)
        self.progressBar.setInvertedAppearance(False)

        self.gridLayout.addWidget(self.progressBar, 2, 2, 1, 1)

        self.textEdit_info = QTextEdit(Form)
        self.textEdit_info.setObjectName(u"textEdit_info")
        self.textEdit_info.setEnabled(True)
        self.textEdit_info.setTextInteractionFlags(Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)

        self.gridLayout.addWidget(self.textEdit_info, 3, 2, 1, 1)

        self.pushButton_info = QPushButton(Form)
        self.pushButton_info.setObjectName(u"pushButton_info")

        self.gridLayout.addWidget(self.pushButton_info, 4, 2, 1, 1)

        self.extension_table = QTableWidget(Form)
        self.extension_table.setObjectName(u"extension_table")

        self.gridLayout.addWidget(self.extension_table, 1, 0, 4, 2)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"Search name:", None))
        self.lineEdit_search_name.setPlaceholderText(QCoreApplication.translate("Form", u"name", None))
        self.pushButton_install_update_selected.setText(QCoreApplication.translate("Form", u"Install / Update Selected", None))
        self.pushButton_uninstall.setText(QCoreApplication.translate("Form", u"Uninstall Selected", None))
        self.pushButton_info.setText(QCoreApplication.translate("Form", u"hide info", None))
    # retranslateUi

