# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'read_channels.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QGridLayout, QSizePolicy,
    QWidget)

class Ui_read_channels_config(object):
    def setupUi(self, read_channels_config):
        if not read_channels_config.objectName():
            read_channels_config.setObjectName(u"read_channels_config")
        read_channels_config.resize(372, 230)
        self.gridLayout = QGridLayout(read_channels_config)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.checkBox_read_all = QCheckBox(read_channels_config)
        self.checkBox_read_all.setObjectName(u"checkBox_read_all")

        self.gridLayout.addWidget(self.checkBox_read_all, 0, 0, 1, 1)

        self.checkBox_split_trigger = QCheckBox(read_channels_config)
        self.checkBox_split_trigger.setObjectName(u"checkBox_split_trigger")

        self.gridLayout.addWidget(self.checkBox_split_trigger, 0, 1, 1, 1)

        self.checkBox_read_variables = QCheckBox(read_channels_config)
        self.checkBox_read_variables.setObjectName(u"checkBox_read_variables")

        self.gridLayout.addWidget(self.checkBox_read_variables, 0, 2, 1, 1)


        self.retranslateUi(read_channels_config)

        QMetaObject.connectSlotsByName(read_channels_config)
    # setupUi

    def retranslateUi(self, read_channels_config):
        read_channels_config.setWindowTitle(QCoreApplication.translate("read_channels_config", u"Form", None))
        self.checkBox_read_all.setText(QCoreApplication.translate("read_channels_config", u"Read All", None))
        self.checkBox_split_trigger.setText(QCoreApplication.translate("read_channels_config", u"Split trigger and read", None))
        self.checkBox_read_variables.setText(QCoreApplication.translate("read_channels_config", u"read/save variables", None))
    # retranslateUi

