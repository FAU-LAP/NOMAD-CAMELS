# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'enterTextDialog.ui'
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

class Ui_EnterTextDialog(object):
    """ """
    def setupUi(self, EnterTextDialog):
        """

        Parameters
        ----------
        EnterTextDialog :
            

        Returns
        -------

        """
        if not EnterTextDialog.objectName():
            EnterTextDialog.setObjectName(u"EnterTextDialog")
        EnterTextDialog.resize(278, 106)
        self.gridLayout_2 = QGridLayout(EnterTextDialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.lineEdit_text = QLineEdit(EnterTextDialog)
        self.lineEdit_text.setObjectName(u"lineEdit_text")

        self.gridLayout.addWidget(self.lineEdit_text, 0, 1, 1, 1)

        self.label = QLabel(EnterTextDialog)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(EnterTextDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout_2.addWidget(self.buttonBox, 1, 0, 1, 1)


        self.retranslateUi(EnterTextDialog)
        self.buttonBox.accepted.connect(EnterTextDialog.accept)
        self.buttonBox.rejected.connect(EnterTextDialog.reject)

        QMetaObject.connectSlotsByName(EnterTextDialog)
    # setupUi

    def retranslateUi(self, EnterTextDialog):
        """

        Parameters
        ----------
        EnterTextDialog :
            

        Returns
        -------

        """
        EnterTextDialog.setWindowTitle(QCoreApplication.translate("EnterTextDialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("EnterTextDialog", u"Task name:", None))
    # retranslateUi

