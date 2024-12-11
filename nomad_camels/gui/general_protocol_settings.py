# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'general_protocol_settings.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QGridLayout, QHeaderView,
    QLabel, QLineEdit, QPushButton, QRadioButton,
    QSizePolicy, QWidget)

from nomad_camels.ui_widgets.variable_table import VariableTable

class Ui_Protocol_Settings(object):
    def setupUi(self, Protocol_Settings):
        if not Protocol_Settings.objectName():
            Protocol_Settings.setObjectName(u"Protocol_Settings")
        Protocol_Settings.resize(374, 463)
        self.gridLayout = QGridLayout(Protocol_Settings)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.pushButton_add_variable = QPushButton(Protocol_Settings)
        self.pushButton_add_variable.setObjectName(u"pushButton_add_variable")
        self.pushButton_add_variable.setMaximumSize(QSize(27, 27))
        self.pushButton_add_variable.setStyleSheet(u"QPushButton {\n"
"                                background-color:  #4CAF50; \n"
"                                color: white; \n"
"                                border: none; \n"
"                                padding: 0px; \n"
"                                padding-bottom: 5px;\n"
"                                text-align: center; \n"
"                                text-decoration: none; \n"
"                                font-size: 18px; \n"
"                                margin: 2px 2px; \n"
"                                border-radius: 6px;\n"
"								font-weight: bold;\n"
"                            }\n"
"\n"
"            QPushButton:hover {\n"
"                background-color: #45a049;\n"
"            }")

        self.gridLayout.addWidget(self.pushButton_add_variable, 8, 1, 1, 1)

        self.lineEdit_filename = QLineEdit(Protocol_Settings)
        self.lineEdit_filename.setObjectName(u"lineEdit_filename")

        self.gridLayout.addWidget(self.lineEdit_filename, 2, 1, 1, 5)

        self.label = QLabel(Protocol_Settings)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(60, 16777215))
        font = QFont()
        font.setBold(True)
        self.label.setFont(font)

        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)

        self.lineEdit_protocol_name = QLineEdit(Protocol_Settings)
        self.lineEdit_protocol_name.setObjectName(u"lineEdit_protocol_name")

        self.gridLayout.addWidget(self.lineEdit_protocol_name, 1, 1, 1, 5)

        self.pushButton_remove_variable = QPushButton(Protocol_Settings)
        self.pushButton_remove_variable.setObjectName(u"pushButton_remove_variable")
        self.pushButton_remove_variable.setMaximumSize(QSize(27, 27))
        self.pushButton_remove_variable.setStyleSheet(u"QPushButton {\n"
"                                background-color:  #FF3333; \n"
"                                color: white; \n"
"                                border: none; \n"
"                                padding: 0px; \n"
"                                padding-bottom: 5px;\n"
"                                text-align: center; \n"
"                                text-decoration: none; \n"
"                                font-size: 18px; \n"
"                                margin: 2px 2px; \n"
"                                border-radius: 6px;\n"
"								font-weight: bold;\n"
"                            }\n"
"\n"
"            QPushButton:hover {\n"
"                background-color: #B22222;\n"
"            }\n"
"QPushButton:disabled {\n"
"        background-color: #808080;\n"
"    }")

        self.gridLayout.addWidget(self.pushButton_remove_variable, 8, 2, 1, 1)

        self.widget_2 = QWidget(Protocol_Settings)
        self.widget_2.setObjectName(u"widget_2")
        self.gridLayout_2 = QGridLayout(self.widget_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.radioButton_h5_after = QRadioButton(self.widget_2)
        self.radioButton_h5_after.setObjectName(u"radioButton_h5_after")

        self.gridLayout_2.addWidget(self.radioButton_h5_after, 0, 1, 1, 1)

        self.checkBox_json_exp = QCheckBox(self.widget_2)
        self.checkBox_json_exp.setObjectName(u"checkBox_json_exp")

        self.gridLayout_2.addWidget(self.checkBox_json_exp, 1, 1, 1, 1)

        self.checkBox_no_config = QCheckBox(self.widget_2)
        self.checkBox_no_config.setObjectName(u"checkBox_no_config")

        self.gridLayout_2.addWidget(self.checkBox_no_config, 4, 0, 1, 2)

        self.checkBox_csv_exp = QCheckBox(self.widget_2)
        self.checkBox_csv_exp.setObjectName(u"checkBox_csv_exp")

        self.gridLayout_2.addWidget(self.checkBox_csv_exp, 1, 0, 1, 1)

        self.checkBox_NeXus = QCheckBox(self.widget_2)
        self.checkBox_NeXus.setObjectName(u"checkBox_NeXus")
        self.checkBox_NeXus.setChecked(True)

        self.gridLayout_2.addWidget(self.checkBox_NeXus, 3, 0, 1, 2)

        self.radioButton_h5_during = QRadioButton(self.widget_2)
        self.radioButton_h5_during.setObjectName(u"radioButton_h5_during")
        self.radioButton_h5_during.setChecked(True)

        self.gridLayout_2.addWidget(self.radioButton_h5_during, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.widget_2, 4, 0, 1, 6)

        self.variable_table = VariableTable(Protocol_Settings)
        self.variable_table.setObjectName(u"variable_table")
        self.variable_table.verticalHeader().setVisible(False)

        self.gridLayout.addWidget(self.variable_table, 9, 0, 1, 6)

        self.label_title = QLabel(Protocol_Settings)
        self.label_title.setObjectName(u"label_title")
        font1 = QFont()
        font1.setPointSize(12)
        font1.setBold(True)
        self.label_title.setFont(font1)

        self.gridLayout.addWidget(self.label_title, 0, 0, 1, 4)

        self.widget_3 = QWidget(Protocol_Settings)
        self.widget_3.setObjectName(u"widget_3")

        self.gridLayout.addWidget(self.widget_3, 5, 0, 1, 1)

        self.label_4 = QLabel(Protocol_Settings)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMaximumSize(QSize(85, 16777215))
        self.label_4.setFont(font)

        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)

        self.widget_4 = QWidget(Protocol_Settings)
        self.widget_4.setObjectName(u"widget_4")

        self.gridLayout.addWidget(self.widget_4, 7, 0, 1, 1)

        self.label_2 = QLabel(Protocol_Settings)
        self.label_2.setObjectName(u"label_2")
        font2 = QFont()
        font2.setPointSize(9)
        font2.setBold(True)
        self.label_2.setFont(font2)

        self.gridLayout.addWidget(self.label_2, 8, 0, 1, 1)

        self.checkBox_live_variables = QCheckBox(Protocol_Settings)
        self.checkBox_live_variables.setObjectName(u"checkBox_live_variables")

        self.gridLayout.addWidget(self.checkBox_live_variables, 10, 0, 1, 6)

        self.checkBox_live_comments = QCheckBox(Protocol_Settings)
        self.checkBox_live_comments.setObjectName(u"checkBox_live_comments")

        self.gridLayout.addWidget(self.checkBox_live_comments, 11, 0, 1, 6)


        self.retranslateUi(Protocol_Settings)

        QMetaObject.connectSlotsByName(Protocol_Settings)
    # setupUi

    def retranslateUi(self, Protocol_Settings):
        Protocol_Settings.setWindowTitle(QCoreApplication.translate("Protocol_Settings", u"Form", None))
        self.pushButton_add_variable.setText(QCoreApplication.translate("Protocol_Settings", u"+", None))
        self.lineEdit_filename.setText(QCoreApplication.translate("Protocol_Settings", u"Datafile", None))
        self.lineEdit_filename.setPlaceholderText(QCoreApplication.translate("Protocol_Settings", u"Filename", None))
        self.label.setText(QCoreApplication.translate("Protocol_Settings", u"Filename:", None))
        self.pushButton_remove_variable.setText(QCoreApplication.translate("Protocol_Settings", u"-", None))
        self.radioButton_h5_after.setText(QCoreApplication.translate("Protocol_Settings", u"write hdf5 after run", None))
        self.checkBox_json_exp.setText(QCoreApplication.translate("Protocol_Settings", u"Export metadata to json", None))
        self.checkBox_no_config.setText(QCoreApplication.translate("Protocol_Settings", u"do not reconfigure instruments at start", None))
        self.checkBox_csv_exp.setText(QCoreApplication.translate("Protocol_Settings", u"Export data to csv", None))
        self.checkBox_NeXus.setText(QCoreApplication.translate("Protocol_Settings", u"also write NeXus entry to data", None))
        self.radioButton_h5_during.setText(QCoreApplication.translate("Protocol_Settings", u"write hdf5 during run", None))
        self.label_title.setText(QCoreApplication.translate("Protocol_Settings", u"General Configuration", None))
        self.label_4.setText(QCoreApplication.translate("Protocol_Settings", u"Protocol Name:", None))
        self.label_2.setText(QCoreApplication.translate("Protocol_Settings", u"Variables", None))
        self.checkBox_live_variables.setText(QCoreApplication.translate("Protocol_Settings", u"allow for live resetting of variables", None))
        self.checkBox_live_comments.setText(QCoreApplication.translate("Protocol_Settings", u"allow live comments to protocol", None))
    # retranslateUi

