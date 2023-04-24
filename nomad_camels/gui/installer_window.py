# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'installer_window.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QGridLayout, QGroupBox,
    QLabel, QMainWindow, QMenuBar, QProgressBar,
    QPushButton, QRadioButton, QSizePolicy, QSpacerItem,
    QStatusBar, QWidget)

from CAMELS.ui_widgets.path_button_edit import Path_Button_Edit

class Ui_InstallerWindow(object):
    def setupUi(self, InstallerWindow):
        if not InstallerWindow.objectName():
            InstallerWindow.setObjectName(u"InstallerWindow")
        InstallerWindow.resize(800, 600)
        self.centralwidget = QWidget(InstallerWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.image_placeholder = QWidget(self.centralwidget)
        self.image_placeholder.setObjectName(u"image_placeholder")

        self.gridLayout.addWidget(self.image_placeholder, 0, 0, 4, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_2, 0, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 6, 0, 1, 1)

        self.pushButton_install = QPushButton(self.centralwidget)
        self.pushButton_install.setObjectName(u"pushButton_install")

        self.gridLayout.addWidget(self.pushButton_install, 6, 1, 1, 1)

        self.pushButton_cancel = QPushButton(self.centralwidget)
        self.pushButton_cancel.setObjectName(u"pushButton_cancel")

        self.gridLayout.addWidget(self.pushButton_cancel, 6, 2, 1, 1)

        self.groupBox_progress = QGroupBox(self.centralwidget)
        self.groupBox_progress.setObjectName(u"groupBox_progress")
        self.gridLayout_4 = QGridLayout(self.groupBox_progress)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.label_current_job = QLabel(self.groupBox_progress)
        self.label_current_job.setObjectName(u"label_current_job")

        self.gridLayout_4.addWidget(self.label_current_job, 0, 0, 1, 1)

        self.progressBar_installation = QProgressBar(self.groupBox_progress)
        self.progressBar_installation.setObjectName(u"progressBar_installation")
        self.progressBar_installation.setValue(0)

        self.gridLayout_4.addWidget(self.progressBar_installation, 1, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox_progress, 5, 0, 1, 3)

        self.groupBox_questions = QGroupBox(self.centralwidget)
        self.groupBox_questions.setObjectName(u"groupBox_questions")
        self.gridLayout_2 = QGridLayout(self.groupBox_questions)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.groupBox_custom_install = QGroupBox(self.groupBox_questions)
        self.groupBox_custom_install.setObjectName(u"groupBox_custom_install")
        self.gridLayout_3 = QGridLayout(self.groupBox_custom_install)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_3 = QLabel(self.groupBox_custom_install)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_3.addWidget(self.label_3, 5, 0, 1, 1)

        self.pathButton_CAMELS = Path_Button_Edit(self.groupBox_custom_install)
        self.pathButton_CAMELS.setObjectName(u"pathButton_CAMELS")

        self.gridLayout_3.addWidget(self.pathButton_CAMELS, 5, 1, 1, 1)

        self.checkBox_python = QCheckBox(self.groupBox_custom_install)
        self.checkBox_python.setObjectName(u"checkBox_python")
        self.checkBox_python.setChecked(True)

        self.gridLayout_3.addWidget(self.checkBox_python, 4, 0, 1, 2)

        self.checkBox_camels = QCheckBox(self.groupBox_custom_install)
        self.checkBox_camels.setObjectName(u"checkBox_camels")
        self.checkBox_camels.setChecked(True)

        self.gridLayout_3.addWidget(self.checkBox_camels, 3, 0, 1, 2)

        self.checkBox_epics = QCheckBox(self.groupBox_custom_install)
        self.checkBox_epics.setObjectName(u"checkBox_epics")
        self.checkBox_epics.setChecked(True)

        self.gridLayout_3.addWidget(self.checkBox_epics, 1, 0, 1, 2)

        self.checkBox_wsl = QCheckBox(self.groupBox_custom_install)
        self.checkBox_wsl.setObjectName(u"checkBox_wsl")
        self.checkBox_wsl.setChecked(True)

        self.gridLayout_3.addWidget(self.checkBox_wsl, 0, 0, 1, 2)


        self.gridLayout_2.addWidget(self.groupBox_custom_install, 3, 0, 1, 3)

        self.radioButton_full = QRadioButton(self.groupBox_questions)
        self.radioButton_full.setObjectName(u"radioButton_full")
        self.radioButton_full.setChecked(True)

        self.gridLayout_2.addWidget(self.radioButton_full, 0, 0, 1, 3)

        self.radioButton_custom = QRadioButton(self.groupBox_questions)
        self.radioButton_custom.setObjectName(u"radioButton_custom")

        self.gridLayout_2.addWidget(self.radioButton_custom, 1, 0, 1, 3)


        self.gridLayout.addWidget(self.groupBox_questions, 4, 0, 1, 3)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 3, 1, 1, 2)

        self.labela = QLabel(self.centralwidget)
        self.labela.setObjectName(u"labela")
        font = QFont()
        font.setFamilies([u"Calibri"])
        font.setPointSize(14)
        font.setBold(True)
        self.labela.setFont(font)

        self.gridLayout.addWidget(self.labela, 1, 1, 1, 2)

        self.label_2t = QLabel(self.centralwidget)
        self.label_2t.setObjectName(u"label_2t")

        self.gridLayout.addWidget(self.label_2t, 2, 1, 1, 2)

        InstallerWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(InstallerWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 21))
        InstallerWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(InstallerWindow)
        self.statusbar.setObjectName(u"statusbar")
        InstallerWindow.setStatusBar(self.statusbar)

        self.retranslateUi(InstallerWindow)

        QMetaObject.connectSlotsByName(InstallerWindow)
    # setupUi

    def retranslateUi(self, InstallerWindow):
        InstallerWindow.setWindowTitle(QCoreApplication.translate("InstallerWindow", u"MainWindow", None))
        self.pushButton_install.setText(QCoreApplication.translate("InstallerWindow", u"Install", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("InstallerWindow", u"Cancel", None))
        self.groupBox_progress.setTitle("")
        self.label_current_job.setText(QCoreApplication.translate("InstallerWindow", u"TextLabel", None))
        self.groupBox_questions.setTitle("")
        self.groupBox_custom_install.setTitle("")
        self.label_3.setText(QCoreApplication.translate("InstallerWindow", u"Path to CAMELS:", None))
        self.checkBox_python.setText(QCoreApplication.translate("InstallerWindow", u"Install Python Environment for CAMELS", None))
        self.checkBox_camels.setText(QCoreApplication.translate("InstallerWindow", u"Install CAMELS", None))
        self.checkBox_epics.setText(QCoreApplication.translate("InstallerWindow", u"Install EPICS in WSL", None))
        self.checkBox_wsl.setText(QCoreApplication.translate("InstallerWindow", u"Install WSL", None))
        self.radioButton_full.setText(QCoreApplication.translate("InstallerWindow", u"Full Install (recommended)", None))
        self.radioButton_custom.setText(QCoreApplication.translate("InstallerWindow", u"Custom Install", None))
        self.labela.setText(QCoreApplication.translate("InstallerWindow", u"CAMELS Installer", None))
        self.label_2t.setText(QCoreApplication.translate("InstallerWindow", u"Configurable Application for Measurements, Experiments and Laboratory-Systems", None))
    # retranslateUi

