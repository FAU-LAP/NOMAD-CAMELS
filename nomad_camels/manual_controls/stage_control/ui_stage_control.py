# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_stage_control.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QGridLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(424, 279)
        self.gridLayout_2 = QGridLayout(Form)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.horizontalSpacer_4 = QSpacerItem(0, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_4, 3, 5, 1, 3)

        self.pushButton_right = QPushButton(Form)
        self.pushButton_right.setObjectName(u"pushButton_right")

        self.gridLayout_2.addWidget(self.pushButton_right, 3, 4, 1, 1)

        self.pushButton_up = QPushButton(Form)
        self.pushButton_up.setObjectName(u"pushButton_up")

        self.gridLayout_2.addWidget(self.pushButton_up, 2, 3, 1, 1)

        self.pushButton_down = QPushButton(Form)
        self.pushButton_down.setObjectName(u"pushButton_down")

        self.gridLayout_2.addWidget(self.pushButton_down, 4, 3, 1, 1)

        self.pushButton_stop = QPushButton(Form)
        self.pushButton_stop.setObjectName(u"pushButton_stop")

        self.gridLayout_2.addWidget(self.pushButton_stop, 3, 3, 1, 1)

        self.pushButton_left = QPushButton(Form)
        self.pushButton_left.setObjectName(u"pushButton_left")

        self.gridLayout_2.addWidget(self.pushButton_left, 3, 2, 1, 1)

        self.lineEdit_stepZ = QLineEdit(Form)
        self.lineEdit_stepZ.setObjectName(u"lineEdit_stepZ")

        self.gridLayout_2.addWidget(self.lineEdit_stepZ, 4, 10, 1, 1)

        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setLayoutDirection(Qt.LeftToRight)
        self.label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label, 2, 8, 1, 1)

        self.lineEdit_stepY = QLineEdit(Form)
        self.lineEdit_stepY.setObjectName(u"lineEdit_stepY")

        self.gridLayout_2.addWidget(self.lineEdit_stepY, 3, 10, 1, 1)

        self.pushButton_zDown = QPushButton(Form)
        self.pushButton_zDown.setObjectName(u"pushButton_zDown")

        self.gridLayout_2.addWidget(self.pushButton_zDown, 4, 6, 1, 1)

        self.pushButton_zUp = QPushButton(Form)
        self.pushButton_zUp.setObjectName(u"pushButton_zUp")

        self.gridLayout_2.addWidget(self.pushButton_zUp, 2, 6, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_2, 3, 0, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_3, 2, 7, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 2, 0, 1, 3)

        self.lineEdit_goZ = QLineEdit(Form)
        self.lineEdit_goZ.setObjectName(u"lineEdit_goZ")

        self.gridLayout_2.addWidget(self.lineEdit_goZ, 10, 8, 1, 3)

        self.pushButton_go_to = QPushButton(Form)
        self.pushButton_go_to.setObjectName(u"pushButton_go_to")

        self.gridLayout_2.addWidget(self.pushButton_go_to, 7, 8, 1, 3)

        self.lineEdit_goX = QLineEdit(Form)
        self.lineEdit_goX.setObjectName(u"lineEdit_goX")

        self.gridLayout_2.addWidget(self.lineEdit_goX, 8, 8, 1, 3)

        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_2, 3, 8, 1, 1)

        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_3, 4, 8, 1, 1)

        self.lineEdit_goY = QLineEdit(Form)
        self.lineEdit_goY.setObjectName(u"lineEdit_goY")

        self.gridLayout_2.addWidget(self.lineEdit_goY, 9, 8, 1, 3)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer, 0, 10, 1, 1)

        self.line = QFrame(Form)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.gridLayout_2.addWidget(self.line, 1, 11, 4, 1)

        self.lineEdit_currentX = QLineEdit(Form)
        self.lineEdit_currentX.setObjectName(u"lineEdit_currentX")
        self.lineEdit_currentX.setEnabled(False)

        self.gridLayout_2.addWidget(self.lineEdit_currentX, 8, 13, 1, 2)

        self.lineEdit_currentZ = QLineEdit(Form)
        self.lineEdit_currentZ.setObjectName(u"lineEdit_currentZ")
        self.lineEdit_currentZ.setEnabled(False)

        self.gridLayout_2.addWidget(self.lineEdit_currentZ, 10, 13, 1, 2)

        self.lineEdit_stepX = QLineEdit(Form)
        self.lineEdit_stepX.setObjectName(u"lineEdit_stepX")

        self.gridLayout_2.addWidget(self.lineEdit_stepX, 2, 10, 1, 1)

        self.label_6 = QLabel(Form)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_2.addWidget(self.label_6, 7, 13, 1, 2)

        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")
        font = QFont()
        font.setBold(True)
        self.label_4.setFont(font)

        self.gridLayout_2.addWidget(self.label_4, 1, 10, 1, 1)

        self.lineEdit_currentY = QLineEdit(Form)
        self.lineEdit_currentY.setObjectName(u"lineEdit_currentY")
        self.lineEdit_currentY.setEnabled(False)

        self.gridLayout_2.addWidget(self.lineEdit_currentY, 9, 13, 1, 2)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_7, 4, 0, 1, 3)

        self.checkBox_manualActive = QCheckBox(Form)
        self.checkBox_manualActive.setObjectName(u"checkBox_manualActive")

        self.gridLayout_2.addWidget(self.checkBox_manualActive, 11, 2, 1, 5)

        self.label_5 = QLabel(Form)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font)

        self.gridLayout_2.addWidget(self.label_5, 7, 2, 1, 5)

        self.lineEdit_manualY = QLineEdit(Form)
        self.lineEdit_manualY.setObjectName(u"lineEdit_manualY")

        self.gridLayout_2.addWidget(self.lineEdit_manualY, 9, 2, 1, 5)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_6, 3, 1, 1, 1)

        self.lineEdit_manualZ = QLineEdit(Form)
        self.lineEdit_manualZ.setObjectName(u"lineEdit_manualZ")

        self.gridLayout_2.addWidget(self.lineEdit_manualZ, 10, 2, 1, 5)

        self.line_3 = QFrame(Form)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.VLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.gridLayout_2.addWidget(self.line_3, 7, 7, 5, 1)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_5, 2, 4, 1, 2)

        self.lineEdit_manualX = QLineEdit(Form)
        self.lineEdit_manualX.setObjectName(u"lineEdit_manualX")

        self.gridLayout_2.addWidget(self.lineEdit_manualX, 8, 2, 1, 5)

        self.checkBox_refY = QCheckBox(Form)
        self.checkBox_refY.setObjectName(u"checkBox_refY")
        self.checkBox_refY.setChecked(True)

        self.gridLayout_2.addWidget(self.checkBox_refY, 3, 12, 1, 1)

        self.checkBox_refZ = QCheckBox(Form)
        self.checkBox_refZ.setObjectName(u"checkBox_refZ")
        self.checkBox_refZ.setChecked(True)

        self.gridLayout_2.addWidget(self.checkBox_refZ, 4, 12, 1, 1)

        self.checkBox_refX = QCheckBox(Form)
        self.checkBox_refX.setObjectName(u"checkBox_refX")
        self.checkBox_refX.setChecked(True)

        self.gridLayout_2.addWidget(self.checkBox_refX, 2, 12, 1, 1)

        self.pushButton_ref = QPushButton(Form)
        self.pushButton_ref.setObjectName(u"pushButton_ref")

        self.gridLayout_2.addWidget(self.pushButton_ref, 1, 12, 1, 3)

        self.pushButton_position = QPushButton(Form)
        self.pushButton_position.setObjectName(u"pushButton_position")

        self.gridLayout_2.addWidget(self.pushButton_position, 9, 11, 1, 2)

        self.lineEdit_read_frequ = QLineEdit(Form)
        self.lineEdit_read_frequ.setObjectName(u"lineEdit_read_frequ")

        self.gridLayout_2.addWidget(self.lineEdit_read_frequ, 11, 13, 1, 2)

        self.label_7 = QLabel(Form)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_7, 11, 8, 1, 5)

        self.line_2 = QFrame(Form)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.gridLayout_2.addWidget(self.line_2, 5, 0, 1, 15)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.pushButton_right.setText("")
        self.pushButton_up.setText("")
        self.pushButton_down.setText("")
        self.pushButton_stop.setText("")
        self.pushButton_left.setText("")
        self.label.setText(QCoreApplication.translate("Form", u"x", None))
        self.pushButton_zDown.setText(QCoreApplication.translate("Form", u"z", None))
        self.pushButton_zUp.setText(QCoreApplication.translate("Form", u"z", None))
        self.pushButton_go_to.setText(QCoreApplication.translate("Form", u"Go To", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"y", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"z", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"current pos.", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Step Size", None))
        self.checkBox_manualActive.setText(QCoreApplication.translate("Form", u"active", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Manual Movement Speeds", None))
        self.checkBox_refY.setText(QCoreApplication.translate("Form", u"y", None))
        self.checkBox_refZ.setText(QCoreApplication.translate("Form", u"z", None))
        self.checkBox_refX.setText(QCoreApplication.translate("Form", u"x", None))
        self.pushButton_ref.setText(QCoreApplication.translate("Form", u"Find Reference", None))
        self.pushButton_position.setText("")
        self.label_7.setText(QCoreApplication.translate("Form", u"Time between readings (s)", None))
    # retranslateUi

