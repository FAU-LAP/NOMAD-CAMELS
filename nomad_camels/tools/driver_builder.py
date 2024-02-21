# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'driver_builder.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QFrame,
    QGridLayout,
    QLabel,
    QLineEdit,
    QSizePolicy,
    QWidget,
)


class Ui_VISA_Device_Builder(object):
    def setupUi(self, VISA_Device_Builder):
        if not VISA_Device_Builder.objectName():
            VISA_Device_Builder.setObjectName("VISA_Device_Builder")
        VISA_Device_Builder.resize(1141, 310)
        self.gridLayout = QGridLayout(VISA_Device_Builder)
        self.gridLayout.setObjectName("gridLayout")
        self.lineEdit_name = QLineEdit(VISA_Device_Builder)
        self.lineEdit_name.setObjectName("lineEdit_name")
        self.lineEdit_name.setMaximumSize(QSize(350, 16777215))

        self.gridLayout.addWidget(self.lineEdit_name, 0, 1, 1, 2)

        self.lineEdit_search_tags = QLineEdit(VISA_Device_Builder)
        self.lineEdit_search_tags.setObjectName("lineEdit_search_tags")
        self.lineEdit_search_tags.setMaximumSize(QSize(250, 16777215))

        self.gridLayout.addWidget(self.lineEdit_search_tags, 2, 1, 1, 1)

        self.label_baud_rate = QLabel(VISA_Device_Builder)
        self.label_baud_rate.setObjectName("label_baud_rate")

        self.gridLayout.addWidget(self.label_baud_rate, 3, 4, 1, 1)

        self.label = QLabel(VISA_Device_Builder)
        self.label.setObjectName("label")
        self.label.setMaximumSize(QSize(100, 16777215))

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.label_write_term = QLabel(VISA_Device_Builder)
        self.label_write_term.setObjectName("label_write_term")
        self.label_write_term.setMaximumSize(QSize(140, 16777215))

        self.gridLayout.addWidget(self.label_write_term, 2, 4, 1, 1)

        self.label_5 = QLabel(VISA_Device_Builder)
        self.label_5.setObjectName("label_5")
        self.label_5.setMaximumSize(QSize(100, 16777215))

        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)

        self.label_read_term = QLabel(VISA_Device_Builder)
        self.label_read_term.setObjectName("label_read_term")
        self.label_read_term.setMaximumSize(QSize(140, 16777215))

        self.gridLayout.addWidget(self.label_read_term, 1, 4, 1, 1)

        self.lineEdit_write_term = QLineEdit(VISA_Device_Builder)
        self.lineEdit_write_term.setObjectName("lineEdit_write_term")

        self.gridLayout.addWidget(self.lineEdit_write_term, 2, 5, 1, 3)

        self.label_7 = QLabel(VISA_Device_Builder)
        self.label_7.setObjectName("label_7")
        self.label_7.setMaximumSize(QSize(100, 16777215))

        self.gridLayout.addWidget(self.label_7, 2, 2, 1, 1)

        self.lineEdit_baud_rate = QLineEdit(VISA_Device_Builder)
        self.lineEdit_baud_rate.setObjectName("lineEdit_baud_rate")

        self.gridLayout.addWidget(self.lineEdit_baud_rate, 3, 5, 1, 3)

        self.checkBox_VISA = QCheckBox(VISA_Device_Builder)
        self.checkBox_VISA.setObjectName("checkBox_VISA")

        self.gridLayout.addWidget(self.checkBox_VISA, 0, 4, 1, 4)

        self.lineEdit_read_term = QLineEdit(VISA_Device_Builder)
        self.lineEdit_read_term.setObjectName("lineEdit_read_term")

        self.gridLayout.addWidget(self.lineEdit_read_term, 1, 5, 1, 3)

        self.line = QFrame(VISA_Device_Builder)
        self.line.setObjectName("line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line, 0, 3, 4, 1)

        self.retranslateUi(VISA_Device_Builder)

        QMetaObject.connectSlotsByName(VISA_Device_Builder)

    # setupUi

    def retranslateUi(self, VISA_Device_Builder):
        VISA_Device_Builder.setWindowTitle(
            QCoreApplication.translate("VISA_Device_Builder", "Form", None)
        )
        self.label_baud_rate.setText(
            QCoreApplication.translate(
                "VISA_Device_Builder", "Default Baud-Rate:", None
            )
        )
        self.label.setText(
            QCoreApplication.translate("VISA_Device_Builder", "Name:", None)
        )
        self.label_write_term.setText(
            QCoreApplication.translate(
                "VISA_Device_Builder", "Default Write-Termination:", None
            )
        )
        self.label_5.setText(
            QCoreApplication.translate("VISA_Device_Builder", "Search-Tags:", None)
        )
        self.label_read_term.setText(
            QCoreApplication.translate(
                "VISA_Device_Builder", "Default Read-Termination:", None
            )
        )
        self.lineEdit_write_term.setText(
            QCoreApplication.translate("VISA_Device_Builder", "\\r\\n", None)
        )
        self.label_7.setText(
            QCoreApplication.translate("VISA_Device_Builder", "(space-separated)", None)
        )
        self.lineEdit_baud_rate.setText(
            QCoreApplication.translate("VISA_Device_Builder", "9600", None)
        )
        self.checkBox_VISA.setText(
            QCoreApplication.translate("VISA_Device_Builder", "VISA connection", None)
        )
        self.lineEdit_read_term.setText(
            QCoreApplication.translate("VISA_Device_Builder", "\\r\\n", None)
        )

    # retranslateUi
