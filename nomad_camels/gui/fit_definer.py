# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'fit_definer.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
    QLabel, QLineEdit, QRadioButton, QSizePolicy,
    QSpacerItem, QWidget)

class Ui_Fit_Definer(object):
    def setupUi(self, Fit_Definer):
        if not Fit_Definer.objectName():
            Fit_Definer.setObjectName(u"Fit_Definer")
        Fit_Definer.resize(287, 243)
        self.gridLayout = QGridLayout(Fit_Definer)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.radioButton_custom_func = QRadioButton(Fit_Definer)
        self.radioButton_custom_func.setObjectName(u"radioButton_custom_func")

        self.gridLayout.addWidget(self.radioButton_custom_func, 1, 1, 1, 1)

        self.radioButton_predef_func = QRadioButton(Fit_Definer)
        self.radioButton_predef_func.setObjectName(u"radioButton_predef_func")
        self.radioButton_predef_func.setChecked(True)

        self.gridLayout.addWidget(self.radioButton_predef_func, 1, 0, 1, 1)

        self.lineEdit_custom_func = QLineEdit(Fit_Definer)
        self.lineEdit_custom_func.setObjectName(u"lineEdit_custom_func")

        self.gridLayout.addWidget(self.lineEdit_custom_func, 2, 1, 1, 1)

        self.comboBox_predef_func = QComboBox(Fit_Definer)
        self.comboBox_predef_func.setObjectName(u"comboBox_predef_func")

        self.gridLayout.addWidget(self.comboBox_predef_func, 2, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 3, 0, 1, 1)

        self.label = QLabel(Fit_Definer)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(9)
        font.setBold(True)
        self.label.setFont(font)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.checkBox_fit = QCheckBox(Fit_Definer)
        self.checkBox_fit.setObjectName(u"checkBox_fit")

        self.gridLayout.addWidget(self.checkBox_fit, 0, 1, 1, 1)

        self.checkBox_guess = QCheckBox(Fit_Definer)
        self.checkBox_guess.setObjectName(u"checkBox_guess")

        self.gridLayout.addWidget(self.checkBox_guess, 4, 0, 1, 1)

        self.checkBox_display_values = QCheckBox(Fit_Definer)
        self.checkBox_display_values.setObjectName(u"checkBox_display_values")

        self.gridLayout.addWidget(self.checkBox_display_values, 4, 1, 1, 1)


        self.retranslateUi(Fit_Definer)

        QMetaObject.connectSlotsByName(Fit_Definer)
    # setupUi

    def retranslateUi(self, Fit_Definer):
        Fit_Definer.setWindowTitle(QCoreApplication.translate("Fit_Definer", u"Form", None))
        self.radioButton_custom_func.setText(QCoreApplication.translate("Fit_Definer", u"Custom function", None))
        self.radioButton_predef_func.setText(QCoreApplication.translate("Fit_Definer", u"Predefined function", None))
        self.label.setText(QCoreApplication.translate("Fit_Definer", u"Fit to: all y-axes", None))
        self.checkBox_fit.setText(QCoreApplication.translate("Fit_Definer", u"fit?", None))
        self.checkBox_guess.setText(QCoreApplication.translate("Fit_Definer", u"guess initial parameters", None))
        self.checkBox_display_values.setText(QCoreApplication.translate("Fit_Definer", u"display fit values", None))
    # retranslateUi

