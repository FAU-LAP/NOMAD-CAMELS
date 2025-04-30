# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'general_protocol_settings.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QGridLayout, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QTabWidget, QTextEdit, QWidget)

from nomad_camels.frontpanels.flyer_window import FlyerButton
from nomad_camels.ui_widgets.path_button_edit import Path_Button_Edit
from nomad_camels.ui_widgets.variable_table import VariableTable
from nomad_camels.ui_widgets.variable_tool_tip_box import Variable_Box

class Ui_Protocol_Settings(object):
    def setupUi(self, Protocol_Settings):
        if not Protocol_Settings.objectName():
            Protocol_Settings.setObjectName(u"Protocol_Settings")
        Protocol_Settings.resize(446, 550)
        self.gridLayout = QGridLayout(Protocol_Settings)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 9, 0)
        self.tabWidget = QTabWidget(Protocol_Settings)
        self.tabWidget.setObjectName(u"tabWidget")
        self.general = QWidget()
        self.general.setObjectName(u"general")
        self.gridLayout_3 = QGridLayout(self.general)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_3 = QLabel(self.general)
        self.label_3.setObjectName(u"label_3")
        font = QFont()
        font.setBold(True)
        self.label_3.setFont(font)

        self.gridLayout_3.addWidget(self.label_3, 1, 0, 1, 2)

        self.textEdit_desc_protocol = QTextEdit(self.general)
        self.textEdit_desc_protocol.setObjectName(u"textEdit_desc_protocol")

        self.gridLayout_3.addWidget(self.textEdit_desc_protocol, 10, 0, 1, 2)

        self.checkBox_csv_exp = QCheckBox(self.general)
        self.checkBox_csv_exp.setObjectName(u"checkBox_csv_exp")

        self.gridLayout_3.addWidget(self.checkBox_csv_exp, 5, 0, 1, 1)

        self.checkBox_json_exp = QCheckBox(self.general)
        self.checkBox_json_exp.setObjectName(u"checkBox_json_exp")

        self.gridLayout_3.addWidget(self.checkBox_json_exp, 5, 1, 1, 1)

        self.label_5 = QLabel(self.general)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font)

        self.gridLayout_3.addWidget(self.label_5, 8, 0, 1, 2)

        self.line_2 = QFrame(self.general)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_3.addWidget(self.line_2, 7, 0, 1, 2)

        self.checkBox_NeXus = QCheckBox(self.general)
        self.checkBox_NeXus.setObjectName(u"checkBox_NeXus")
        self.checkBox_NeXus.setChecked(False)

        self.gridLayout_3.addWidget(self.checkBox_NeXus, 6, 0, 1, 2)

        self.comboBox_h5 = QComboBox(self.general)
        self.comboBox_h5.addItem("")
        self.comboBox_h5.addItem("")
        self.comboBox_h5.setObjectName(u"comboBox_h5")

        self.gridLayout_3.addWidget(self.comboBox_h5, 3, 0, 1, 2)

        self.checkBox_live_comments = QCheckBox(self.general)
        self.checkBox_live_comments.setObjectName(u"checkBox_live_comments")

        self.gridLayout_3.addWidget(self.checkBox_live_comments, 9, 0, 1, 2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label = QLabel(self.general)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(60, 16777215))
        font1 = QFont()
        font1.setBold(False)
        self.label.setFont(font1)

        self.horizontalLayout_3.addWidget(self.label)

        self.lineEdit_filename = Variable_Box(self.general)
        self.lineEdit_filename.setObjectName(u"lineEdit_filename")

        self.horizontalLayout_3.addWidget(self.lineEdit_filename)


        self.gridLayout_3.addLayout(self.horizontalLayout_3, 2, 0, 1, 2)

        self.tabWidget.addTab(self.general, "")
        self.plot_widge = QWidget()
        self.plot_widge.setObjectName(u"plot_widge")
        self.tabWidget.addTab(self.plot_widge, "")
        self.variables = QWidget()
        self.variables.setObjectName(u"variables")
        self.gridLayout_4 = QGridLayout(self.variables)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.variable_table = VariableTable(self.variables)
        self.variable_table.setObjectName(u"variable_table")
        self.variable_table.verticalHeader().setVisible(False)

        self.gridLayout_4.addWidget(self.variable_table, 2, 0, 1, 3)

        self.pushButton_add_variable = QPushButton(self.variables)
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

        self.gridLayout_4.addWidget(self.pushButton_add_variable, 1, 1, 1, 1)

        self.checkBox_live_variables = QCheckBox(self.variables)
        self.checkBox_live_variables.setObjectName(u"checkBox_live_variables")

        self.gridLayout_4.addWidget(self.checkBox_live_variables, 0, 0, 1, 1)

        self.label_2 = QLabel(self.variables)
        self.label_2.setObjectName(u"label_2")
        font2 = QFont()
        font2.setPointSize(9)
        font2.setBold(True)
        self.label_2.setFont(font2)

        self.gridLayout_4.addWidget(self.label_2, 1, 0, 1, 1)

        self.pushButton_remove_variable = QPushButton(self.variables)
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

        self.gridLayout_4.addWidget(self.pushButton_remove_variable, 1, 2, 1, 1)

        self.tabWidget.addTab(self.variables, "")
        self.advanced = QWidget()
        self.advanced.setObjectName(u"advanced")
        self.gridLayout_2 = QGridLayout(self.advanced)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_7 = QLabel(self.advanced)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font)

        self.gridLayout_2.addWidget(self.label_7, 4, 0, 1, 1)

        self.line = QFrame(self.advanced)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_2.addWidget(self.line, 3, 0, 1, 1)

        self.line_3 = QFrame(self.advanced)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_2.addWidget(self.line_3, 6, 0, 1, 1)

        self.checkBox_no_config = QCheckBox(self.advanced)
        self.checkBox_no_config.setObjectName(u"checkBox_no_config")

        self.gridLayout_2.addWidget(self.checkBox_no_config, 5, 0, 1, 1)

        self.label_6 = QLabel(self.advanced)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font)

        self.gridLayout_2.addWidget(self.label_6, 0, 0, 1, 1)

        self.pushButton_instrument_aliases = QPushButton(self.advanced)
        self.pushButton_instrument_aliases.setObjectName(u"pushButton_instrument_aliases")

        self.gridLayout_2.addWidget(self.pushButton_instrument_aliases, 1, 0, 1, 1)

        self.line_4 = QFrame(self.advanced)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.Shape.HLine)
        self.line_4.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_2.addWidget(self.line_4, 9, 0, 1, 1)

        self.checkBox_perform_at_end = QCheckBox(self.advanced)
        self.checkBox_perform_at_end.setObjectName(u"checkBox_perform_at_end")

        self.gridLayout_2.addWidget(self.checkBox_perform_at_end, 12, 0, 1, 1)

        self.label_9 = QLabel(self.advanced)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setFont(font)

        self.gridLayout_2.addWidget(self.label_9, 7, 0, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer_3, 15, 0, 1, 1)

        self.label_8 = QLabel(self.advanced)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setFont(font)

        self.gridLayout_2.addWidget(self.label_8, 11, 0, 1, 1)

        self.ending_protocol_selection = Path_Button_Edit(self.advanced)
        self.ending_protocol_selection.setObjectName(u"ending_protocol_selection")

        self.gridLayout_2.addWidget(self.ending_protocol_selection, 14, 0, 1, 1)

        self.flyer_button = FlyerButton(self.advanced)
        self.flyer_button.setObjectName(u"flyer_button")

        self.gridLayout_2.addWidget(self.flyer_button, 8, 0, 1, 1)

        self.tabWidget.addTab(self.advanced, "")

        self.gridLayout.addWidget(self.tabWidget, 2, 0, 1, 3)

        self.label_title = QLabel(Protocol_Settings)
        self.label_title.setObjectName(u"label_title")
        font3 = QFont()
        font3.setPointSize(12)
        font3.setBold(True)
        self.label_title.setFont(font3)

        self.gridLayout.addWidget(self.label_title, 0, 0, 1, 3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_4 = QLabel(Protocol_Settings)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMaximumSize(QSize(90, 16777215))
        self.label_4.setFont(font)

        self.horizontalLayout_2.addWidget(self.label_4)

        self.lineEdit_protocol_name = QLineEdit(Protocol_Settings)
        self.lineEdit_protocol_name.setObjectName(u"lineEdit_protocol_name")

        self.horizontalLayout_2.addWidget(self.lineEdit_protocol_name)


        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)


        self.retranslateUi(Protocol_Settings)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Protocol_Settings)
    # setupUi

    def retranslateUi(self, Protocol_Settings):
        Protocol_Settings.setWindowTitle(QCoreApplication.translate("Protocol_Settings", u"Form", None))
        self.label_3.setText(QCoreApplication.translate("Protocol_Settings", u"Saving:", None))
        self.checkBox_csv_exp.setText(QCoreApplication.translate("Protocol_Settings", u"Export data to csv", None))
        self.checkBox_json_exp.setText(QCoreApplication.translate("Protocol_Settings", u"Export metadata to json", None))
        self.label_5.setText(QCoreApplication.translate("Protocol_Settings", u"Descriptions:", None))
        self.checkBox_NeXus.setText(QCoreApplication.translate("Protocol_Settings", u"also write NeXus entry to data", None))
        self.comboBox_h5.setItemText(0, QCoreApplication.translate("Protocol_Settings", u"write hdf5 during run", None))
        self.comboBox_h5.setItemText(1, QCoreApplication.translate("Protocol_Settings", u"write hdf5 after run", None))

        self.checkBox_live_comments.setText(QCoreApplication.translate("Protocol_Settings", u"allow live comments to protocol", None))
        self.label.setText(QCoreApplication.translate("Protocol_Settings", u"Filename:", None))
        self.lineEdit_filename.setText(QCoreApplication.translate("Protocol_Settings", u"Datafile", None))
        self.lineEdit_filename.setPlaceholderText(QCoreApplication.translate("Protocol_Settings", u"Filename", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.general), QCoreApplication.translate("Protocol_Settings", u"General Settings", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.plot_widge), QCoreApplication.translate("Protocol_Settings", u"Plots", None))
        self.pushButton_add_variable.setText(QCoreApplication.translate("Protocol_Settings", u"+", None))
        self.checkBox_live_variables.setText(QCoreApplication.translate("Protocol_Settings", u"allow for live resetting of variables", None))
        self.label_2.setText(QCoreApplication.translate("Protocol_Settings", u"Variables", None))
        self.pushButton_remove_variable.setText(QCoreApplication.translate("Protocol_Settings", u"-", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.variables), QCoreApplication.translate("Protocol_Settings", u"Variables", None))
        self.label_7.setText(QCoreApplication.translate("Protocol_Settings", u"Instrument Configuration:", None))
        self.checkBox_no_config.setText(QCoreApplication.translate("Protocol_Settings", u"do not reconfigure instruments at start", None))
        self.label_6.setText(QCoreApplication.translate("Protocol_Settings", u"Protocol Sharing:", None))
        self.pushButton_instrument_aliases.setText(QCoreApplication.translate("Protocol_Settings", u"Instrument Aliases", None))
        self.checkBox_perform_at_end.setText(QCoreApplication.translate("Protocol_Settings", u"Perform steps at end of protocol", None))
        self.label_9.setText(QCoreApplication.translate("Protocol_Settings", u"Data Acquisition:", None))
        self.label_8.setText(QCoreApplication.translate("Protocol_Settings", u"Protocol Cleanup:", None))
        self.flyer_button.setText(QCoreApplication.translate("Protocol_Settings", u"Asynchronous measurement during protocol", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.advanced), QCoreApplication.translate("Protocol_Settings", u"Advanced", None))
        self.label_title.setText(QCoreApplication.translate("Protocol_Settings", u"General Configuration", None))
        self.label_4.setText(QCoreApplication.translate("Protocol_Settings", u"Protocol Name:", None))
    # retranslateUi

