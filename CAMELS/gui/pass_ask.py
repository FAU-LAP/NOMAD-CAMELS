# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pass_ask.ui'
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
    QGridLayout, QLabel, QLineEdit, QSizePolicy,
    QWidget)

class Ui_Pass_Ask(object):
    def setupUi(self, Pass_Ask):
        if not Pass_Ask.objectName():
            Pass_Ask.setObjectName(u"Pass_Ask")
        Pass_Ask.resize(400, 106)
        self.gridLayout = QGridLayout(Pass_Ask)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_2 = QLabel(Pass_Ask)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.lineEdit_password_1 = QLineEdit(Pass_Ask)
        self.lineEdit_password_1.setObjectName(u"lineEdit_password_1")
        self.lineEdit_password_1.setEchoMode(QLineEdit.Password)

        self.gridLayout.addWidget(self.lineEdit_password_1, 1, 1, 1, 1)

        self.buttonBox = QDialogButtonBox(Pass_Ask)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 2)

        self.label = QLabel(Pass_Ask)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)


        self.retranslateUi(Pass_Ask)
        self.buttonBox.accepted.connect(Pass_Ask.accept)
        self.buttonBox.rejected.connect(Pass_Ask.reject)

        QMetaObject.connectSlotsByName(Pass_Ask)
    # setupUi

    def retranslateUi(self, Pass_Ask):
        Pass_Ask.setWindowTitle(QCoreApplication.translate("Pass_Ask", u"Dialog", None))
        self.label_2.setText(QCoreApplication.translate("Pass_Ask", u"Password:", None))
        self.label.setText(QCoreApplication.translate("Pass_Ask", u"Enter sudo-password for the Ubuntu-user \"epics\":", None))
    # retranslateUi

