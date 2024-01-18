# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'protocol_view.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHeaderView,
    QLabel, QPushButton, QSizePolicy, QSplitter,
    QToolButton, QTreeView, QWidget)

class Ui_Protocol_View(object):
    def setupUi(self, Protocol_View):
        if not Protocol_View.objectName():
            Protocol_View.setObjectName(u"Protocol_View")
        Protocol_View.resize(617, 522)
        self.gridLayout = QGridLayout(Protocol_View)
        self.gridLayout.setObjectName(u"gridLayout")
        self.meas_splitter = QSplitter(Protocol_View)
        self.meas_splitter.setObjectName(u"meas_splitter")
        self.meas_splitter.setFrameShape(QFrame.NoFrame)
        self.meas_splitter.setLineWidth(10)
        self.meas_splitter.setMidLineWidth(10)
        self.meas_splitter.setOrientation(Qt.Horizontal)
        self.sequence_main_widget = QWidget(self.meas_splitter)
        self.sequence_main_widget.setObjectName(u"sequence_main_widget")
        self.gridLayout_8 = QGridLayout(self.sequence_main_widget)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(-1, 0, -1, 0)
        self.pushButton_remove_step = QPushButton(self.sequence_main_widget)
        self.pushButton_remove_step.setObjectName(u"pushButton_remove_step")
        self.pushButton_remove_step.setMinimumSize(QSize(30, 23))
        self.pushButton_remove_step.setMaximumSize(QSize(30, 30))
        self.pushButton_remove_step.setStyleSheet(u"QPushButton {\n"
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
"            }")

        self.gridLayout_8.addWidget(self.pushButton_remove_step, 3, 2, 1, 1)

        self.toolButton_add_step = QToolButton(self.sequence_main_widget)
        self.toolButton_add_step.setObjectName(u"toolButton_add_step")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButton_add_step.sizePolicy().hasHeightForWidth())
        self.toolButton_add_step.setSizePolicy(sizePolicy)
        self.toolButton_add_step.setMinimumSize(QSize(30, 23))
        self.toolButton_add_step.setMaximumSize(QSize(30, 30))
        self.toolButton_add_step.setStyleSheet(u"QToolButton {\n"
"                                background-color: #4CAF50; \n"
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
"                            QToolButton:hover {\n"
"                                background-color: #45a049;\n"
"                            }")

        self.gridLayout_8.addWidget(self.toolButton_add_step, 2, 2, 1, 1)

        self.label_sequence = QLabel(self.sequence_main_widget)
        self.label_sequence.setObjectName(u"label_sequence")
        self.label_sequence.setMaximumSize(QSize(16777215, 19))
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_sequence.setFont(font)

        self.gridLayout_8.addWidget(self.label_sequence, 0, 0, 1, 1)

        self.pushButton_move_step_up = QPushButton(self.sequence_main_widget)
        self.pushButton_move_step_up.setObjectName(u"pushButton_move_step_up")
        self.pushButton_move_step_up.setStyleSheet(u"QPushButton {\n"
"    background-color: #2a4cdf; /* This is a lighter shade of blue */\n"
"    color: white;\n"
"    border: none;\n"
"    padding: 2px 10px;\n"
"    text-align: center;\n"
"    text-decoration: none;\n"
"    font-size: 13px;\n"
"    margin: 2px 2px;\n"
"    border-radius: 6px;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #1a3cbf; /* This is a darker shade of the lighter blue for hover effect */\n"
"}")

        self.gridLayout_8.addWidget(self.pushButton_move_step_up, 2, 0, 1, 1)

        self.treeView_protocol_sequence = QTreeView(self.sequence_main_widget)
        self.treeView_protocol_sequence.setObjectName(u"treeView_protocol_sequence")

        self.gridLayout_8.addWidget(self.treeView_protocol_sequence, 5, 0, 1, 3)

        self.pushButton_move_step_down = QPushButton(self.sequence_main_widget)
        self.pushButton_move_step_down.setObjectName(u"pushButton_move_step_down")
        self.pushButton_move_step_down.setStyleSheet(u"QPushButton {\n"
"    background-color: #2a4cdf; /* This is a lighter shade of blue */\n"
"    color: white;\n"
"    border: none;\n"
"    padding: 2px 10px;\n"
"    text-align: center;\n"
"    text-decoration: none;\n"
"    font-size: 13px;\n"
"    margin: 2px 2px;\n"
"    border-radius: 6px;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #1a3cbf; /* This is a darker shade of the lighter blue for hover effect */\n"
"}")

        self.gridLayout_8.addWidget(self.pushButton_move_step_down, 3, 0, 1, 1)

        self.pushButton_move_step_out = QPushButton(self.sequence_main_widget)
        self.pushButton_move_step_out.setObjectName(u"pushButton_move_step_out")
        self.pushButton_move_step_out.setStyleSheet(u"QPushButton {\n"
"    background-color: #2a4cdf; /* This is a lighter shade of blue */\n"
"    color: white;\n"
"    border: none;\n"
"    padding: 2px 10px;\n"
"    text-align: center;\n"
"    text-decoration: none;\n"
"    font-size: 13px;\n"
"    margin: 2px 2px;\n"
"    border-radius: 6px;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #1a3cbf; /* This is a darker shade of the lighter blue for hover effect */\n"
"}")

        self.gridLayout_8.addWidget(self.pushButton_move_step_out, 3, 1, 1, 1)

        self.pushButton_move_step_in = QPushButton(self.sequence_main_widget)
        self.pushButton_move_step_in.setObjectName(u"pushButton_move_step_in")
        self.pushButton_move_step_in.setStyleSheet(u"QPushButton {\n"
"    background-color: #2a4cdf; /* This is a lighter shade of blue */\n"
"    color: white;\n"
"    border: none;\n"
"    padding: 2px 10px;\n"
"    text-align: center;\n"
"    text-decoration: none;\n"
"    font-size: 13px;\n"
"    margin: 2px 2px;\n"
"    border-radius: 6px;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #1a3cbf; /* This is a darker shade of the lighter blue for hover effect */\n"
"}")

        self.gridLayout_8.addWidget(self.pushButton_move_step_in, 2, 1, 1, 1)

        self.meas_splitter.addWidget(self.sequence_main_widget)
        self.configuration_main_widget = QWidget(self.meas_splitter)
        self.configuration_main_widget.setObjectName(u"configuration_main_widget")
        self.gridLayout_9 = QGridLayout(self.configuration_main_widget)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(-1, 0, 0, 0)
        self.label_configuration = QLabel(self.configuration_main_widget)
        self.label_configuration.setObjectName(u"label_configuration")
        self.label_configuration.setMaximumSize(QSize(16777215, 19))
        self.label_configuration.setFont(font)

        self.gridLayout_9.addWidget(self.label_configuration, 0, 0, 1, 1)

        self.loopstep_configuration_widget = QWidget(self.configuration_main_widget)
        self.loopstep_configuration_widget.setObjectName(u"loopstep_configuration_widget")
        self.gridLayout_10 = QGridLayout(self.loopstep_configuration_widget)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setContentsMargins(0, 0, 0, 0)

        self.gridLayout_9.addWidget(self.loopstep_configuration_widget, 1, 0, 1, 1)

        self.meas_splitter.addWidget(self.configuration_main_widget)

        self.gridLayout.addWidget(self.meas_splitter, 0, 0, 1, 1)


        self.retranslateUi(Protocol_View)

        QMetaObject.connectSlotsByName(Protocol_View)
    # setupUi

    def retranslateUi(self, Protocol_View):
        Protocol_View.setWindowTitle(QCoreApplication.translate("Protocol_View", u"Form", None))
        self.pushButton_remove_step.setText(QCoreApplication.translate("Protocol_View", u"-", None))
        self.toolButton_add_step.setText(QCoreApplication.translate("Protocol_View", u"+", None))
        self.label_sequence.setText(QCoreApplication.translate("Protocol_View", u"Sequence", None))
        self.pushButton_move_step_up.setText(QCoreApplication.translate("Protocol_View", u"move up \u2191", None))
        self.pushButton_move_step_down.setText(QCoreApplication.translate("Protocol_View", u"move down \u2193", None))
        self.pushButton_move_step_out.setText(QCoreApplication.translate("Protocol_View", u"move out \u2190", None))
        self.pushButton_move_step_in.setText(QCoreApplication.translate("Protocol_View", u"move in \u2192", None))
        self.label_configuration.setText(QCoreApplication.translate("Protocol_View", u"Configuration", None))
    # retranslateUi

