# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'VISA_builder.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QLineEdit,
    QSizePolicy, QWidget)

class Ui_VISA_Device_Builder(object):
    """ """
    def setupUi(self, VISA_Device_Builder):
        """

        Parameters
        ----------
        VISA_Device_Builder :
            

        Returns
        -------

        """
        if not VISA_Device_Builder.objectName():
            VISA_Device_Builder.setObjectName(u"VISA_Device_Builder")
        VISA_Device_Builder.resize(400, 300)
        self.gridLayout = QGridLayout(VISA_Device_Builder)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(VISA_Device_Builder)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.label_5 = QLabel(VISA_Device_Builder)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 5, 0, 1, 1)

        self.lineEdit_name = QLineEdit(VISA_Device_Builder)
        self.lineEdit_name.setObjectName(u"lineEdit_name")

        self.gridLayout.addWidget(self.lineEdit_name, 0, 1, 1, 3)

        self.label_6 = QLabel(VISA_Device_Builder)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 1, 0, 1, 1)

        self.lineEdit_search_tags = QLineEdit(VISA_Device_Builder)
        self.lineEdit_search_tags.setObjectName(u"lineEdit_search_tags")

        self.gridLayout.addWidget(self.lineEdit_search_tags, 5, 1, 1, 2)

        self.label_7 = QLabel(VISA_Device_Builder)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 5, 3, 1, 1)

        self.lineEdit_ophyd_name = QLineEdit(VISA_Device_Builder)
        self.lineEdit_ophyd_name.setObjectName(u"lineEdit_ophyd_name")

        self.gridLayout.addWidget(self.lineEdit_ophyd_name, 1, 1, 1, 3)

        self.label_3 = QLabel(VISA_Device_Builder)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)

        self.label_4 = QLabel(VISA_Device_Builder)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)

        self.lineEdit_baud_rate = QLineEdit(VISA_Device_Builder)
        self.lineEdit_baud_rate.setObjectName(u"lineEdit_baud_rate")

        self.gridLayout.addWidget(self.lineEdit_baud_rate, 4, 1, 1, 3)

        self.lineEdit_write_term = QLineEdit(VISA_Device_Builder)
        self.lineEdit_write_term.setObjectName(u"lineEdit_write_term")

        self.gridLayout.addWidget(self.lineEdit_write_term, 3, 1, 1, 3)

        self.lineEdit_read_term = QLineEdit(VISA_Device_Builder)
        self.lineEdit_read_term.setObjectName(u"lineEdit_read_term")

        self.gridLayout.addWidget(self.lineEdit_read_term, 2, 1, 1, 3)

        self.label_2 = QLabel(VISA_Device_Builder)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

        QWidget.setTabOrder(self.lineEdit_name, self.lineEdit_ophyd_name)
        QWidget.setTabOrder(self.lineEdit_ophyd_name, self.lineEdit_read_term)
        QWidget.setTabOrder(self.lineEdit_read_term, self.lineEdit_write_term)
        QWidget.setTabOrder(self.lineEdit_write_term, self.lineEdit_baud_rate)
        QWidget.setTabOrder(self.lineEdit_baud_rate, self.lineEdit_search_tags)

        self.retranslateUi(VISA_Device_Builder)

        QMetaObject.connectSlotsByName(VISA_Device_Builder)
    # setupUi

    def retranslateUi(self, VISA_Device_Builder):
        """

        Parameters
        ----------
        VISA_Device_Builder :
            

        Returns
        -------

        """
        VISA_Device_Builder.setWindowTitle(QCoreApplication.translate("VISA_Device_Builder", u"Form", None))
        self.label.setText(QCoreApplication.translate("VISA_Device_Builder", u"Name:", None))
        self.label_5.setText(QCoreApplication.translate("VISA_Device_Builder", u"Search-Tags:", None))
        self.label_6.setText(QCoreApplication.translate("VISA_Device_Builder", u"Ophyd-Class-Name:", None))
        self.label_7.setText(QCoreApplication.translate("VISA_Device_Builder", u"(space-separated)", None))
        self.label_3.setText(QCoreApplication.translate("VISA_Device_Builder", u"Default Write-Termination:", None))
        self.label_4.setText(QCoreApplication.translate("VISA_Device_Builder", u"Default Baud-Rate:", None))
        self.lineEdit_baud_rate.setText(QCoreApplication.translate("VISA_Device_Builder", u"9600", None))
        self.lineEdit_write_term.setText(QCoreApplication.translate("VISA_Device_Builder", u"\\r\\n", None))
        self.lineEdit_read_term.setText(QCoreApplication.translate("VISA_Device_Builder", u"\\r\\n", None))
        self.label_2.setText(QCoreApplication.translate("VISA_Device_Builder", u"Default Read-Termination:", None))
    # retranslateUi

