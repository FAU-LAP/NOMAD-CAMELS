# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'instrument_config.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
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
    QGridLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QWidget,
)


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName("Form")
        Form.resize(483, 231)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setContentsMargins(9, 9, 9, 9)
        self.tableWidget_instruments = QTableWidget(Form)
        self.tableWidget_instruments.setObjectName("tableWidget_instruments")

        self.gridLayout.addWidget(self.tableWidget_instruments, 1, 0, 2, 2)

        self.label_config = QLabel(Form)
        self.label_config.setObjectName("label_config")
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.label_config.setFont(font)

        self.gridLayout.addWidget(self.label_config, 0, 3, 1, 1)

        self.pushButton_remove = QPushButton(Form)
        self.pushButton_remove.setObjectName("pushButton_remove")
        self.pushButton_remove.setEnabled(False)
        self.pushButton_remove.setMaximumSize(QSize(89999, 27))
        font1 = QFont()
        font1.setBold(True)
        font1.setUnderline(False)
        font1.setStrikeOut(False)
        self.pushButton_remove.setFont(font1)
        self.pushButton_remove.setStyleSheet(
            "QPushButton {\n"
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
            "        background-color:#808080;\n"
            "    }"
        )

        self.gridLayout.addWidget(self.pushButton_remove, 1, 4, 1, 1)

        self.pushButton_info = QPushButton(Form)
        self.pushButton_info.setObjectName("pushButton_info")
        self.pushButton_info.setStyleSheet(
            "QPushButton {\n"
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
            "}"
        )

        self.gridLayout.addWidget(self.pushButton_info, 0, 4, 1, 1)

        self.label = QLabel(Form)
        self.label.setObjectName("label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.lineEdit_search = QLineEdit(Form)
        self.lineEdit_search.setObjectName("lineEdit_search")

        self.gridLayout.addWidget(self.lineEdit_search, 0, 1, 1, 1)

        self.config_tabs = QTabWidget(Form)
        self.config_tabs.setObjectName("config_tabs")
        self.tab = QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_2 = QGridLayout(self.tab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.config_widge = QLabel(self.tab)
        self.config_widge.setObjectName("config_widge")

        self.gridLayout_2.addWidget(self.config_widge, 0, 0, 1, 1)

        self.config_tabs.addTab(self.tab, "")

        self.gridLayout.addWidget(self.config_tabs, 2, 3, 1, 2)

        self.pushButton_add = QPushButton(Form)
        self.pushButton_add.setObjectName("pushButton_add")
        self.pushButton_add.setEnabled(False)
        self.pushButton_add.setMaximumSize(QSize(99999, 27))
        self.pushButton_add.setFont(font1)
        self.pushButton_add.setStyleSheet(
            "QPushButton {\n"
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
            "                            QPushButton:hover {\n"
            "                                background-color: #45a049;\n"
            "                            }\n"
            "QPushButton:disabled {\n"
            "        background-color: #808080;\n"
            "    }"
        )

        self.gridLayout.addWidget(self.pushButton_add, 1, 3, 1, 1)

        self.retranslateUi(Form)

        self.config_tabs.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(Form)

    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", "Form", None))
        self.label_config.setText(
            QCoreApplication.translate("Form", "Configure:", None)
        )
        self.pushButton_remove.setText(QCoreApplication.translate("Form", "-", None))
        self.pushButton_info.setText(
            QCoreApplication.translate("Form", "hide info", None)
        )
        self.label.setText(QCoreApplication.translate("Form", "Search name:", None))
        self.lineEdit_search.setPlaceholderText(
            QCoreApplication.translate("Form", "Search", None)
        )
        self.config_widge.setText(
            QCoreApplication.translate(
                "Form",
                '<html><head/><body><p><span style=" font-size:10pt; font-weight:600;">Select an instrument</span></p></body></html>',
                None,
            )
        )
        self.config_tabs.setTabText(
            self.config_tabs.indexOf(self.tab),
            QCoreApplication.translate("Form", "Select an instrument", None),
        )
        self.pushButton_add.setText(QCoreApplication.translate("Form", "+", None))

    # retranslateUi
