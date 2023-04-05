# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainWindow_v2.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QLabel, QLineEdit, QMainWindow, QMenu,
    QMenuBar, QProgressBar, QPushButton, QSizePolicy,
    QSpacerItem, QSplitter, QStatusBar, QWidget)

from CAMELS.ui_widgets.console_redirect import Console_TextEdit

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1021, 490)
        self.actionPresets = QAction(MainWindow)
        self.actionPresets.setObjectName(u"actionPresets")
        self.actionOptions = QAction(MainWindow)
        self.actionOptions.setObjectName(u"actionOptions")
        self.actionSave_Device_Preset_As = QAction(MainWindow)
        self.actionSave_Device_Preset_As.setObjectName(u"actionSave_Device_Preset_As")
        self.actionLoad = QAction(MainWindow)
        self.actionLoad.setObjectName(u"actionLoad")
        self.actionMeasurement_Presets = QAction(MainWindow)
        self.actionMeasurement_Presets.setObjectName(u"actionMeasurement_Presets")
        self.actionSave_Preset = QAction(MainWindow)
        self.actionSave_Preset.setObjectName(u"actionSave_Preset")
        self.actionOpen_Backup_Device_Preset = QAction(MainWindow)
        self.actionOpen_Backup_Device_Preset.setObjectName(u"actionOpen_Backup_Device_Preset")
        self.actionLoad_Backup_Preset = QAction(MainWindow)
        self.actionLoad_Backup_Preset.setObjectName(u"actionLoad_Backup_Preset")
        self.actionAutosave_on_closing = QAction(MainWindow)
        self.actionAutosave_on_closing.setObjectName(u"actionAutosave_on_closing")
        self.actionAutosave_on_closing.setCheckable(True)
        self.actionDevice_Driver_Builder = QAction(MainWindow)
        self.actionDevice_Driver_Builder.setObjectName(u"actionDevice_Driver_Builder")
        self.actionDark_Mode = QAction(MainWindow)
        self.actionDark_Mode.setObjectName(u"actionDark_Mode")
        self.actionDark_Mode.setCheckable(True)
        self.actionUndo = QAction(MainWindow)
        self.actionUndo.setObjectName(u"actionUndo")
        self.actionRedo = QAction(MainWindow)
        self.actionRedo.setObjectName(u"actionRedo")
        self.actionSettings = QAction(MainWindow)
        self.actionSettings.setObjectName(u"actionSettings")
        self.actionIOC_Builder = QAction(MainWindow)
        self.actionIOC_Builder.setObjectName(u"actionIOC_Builder")
        self.actionNew_Device_Preset_2 = QAction(MainWindow)
        self.actionNew_Device_Preset_2.setObjectName(u"actionNew_Device_Preset_2")
        self.actionSave_Device_Preset = QAction(MainWindow)
        self.actionSave_Device_Preset.setObjectName(u"actionSave_Device_Preset")
        self.actionSave_Preset_As = QAction(MainWindow)
        self.actionSave_Preset_As.setObjectName(u"actionSave_Preset_As")
        self.actionNew_Preset = QAction(MainWindow)
        self.actionNew_Preset.setObjectName(u"actionNew_Preset")
        self.actionNew_Device_Preset = QAction(MainWindow)
        self.actionNew_Device_Preset.setObjectName(u"actionNew_Device_Preset")
        self.actionDocumentation = QAction(MainWindow)
        self.actionDocumentation.setObjectName(u"actionDocumentation")
        self.actionReport_Bug = QAction(MainWindow)
        self.actionReport_Bug.setObjectName(u"actionReport_Bug")
        self.actionVISA_device_builder = QAction(MainWindow)
        self.actionVISA_device_builder.setObjectName(u"actionVISA_device_builder")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_5 = QGridLayout(self.centralwidget)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.label_arrow = QLabel(self.centralwidget)
        self.label_arrow.setObjectName(u"label_arrow")
        self.label_arrow.setAlignment(Qt.AlignCenter)

        self.gridLayout_5.addWidget(self.label_arrow, 2, 2, 1, 1)

        self.pushButton_stop = QPushButton(self.centralwidget)
        self.pushButton_stop.setObjectName(u"pushButton_stop")
        self.pushButton_stop.setEnabled(False)
        self.pushButton_stop.setMaximumSize(QSize(130, 16777215))

        self.gridLayout_5.addWidget(self.pushButton_stop, 4, 11, 1, 1)

        self.pushButton_resume = QPushButton(self.centralwidget)
        self.pushButton_resume.setObjectName(u"pushButton_resume")
        self.pushButton_resume.setEnabled(False)
        self.pushButton_resume.setMaximumSize(QSize(130, 16777215))

        self.gridLayout_5.addWidget(self.pushButton_resume, 4, 9, 1, 1)

        self.pushButton_pause = QPushButton(self.centralwidget)
        self.pushButton_pause.setObjectName(u"pushButton_pause")
        self.pushButton_pause.setEnabled(False)
        self.pushButton_pause.setMaximumSize(QSize(130, 16777215))

        self.gridLayout_5.addWidget(self.pushButton_pause, 4, 10, 1, 1)

        self.progressBar_protocols = QProgressBar(self.centralwidget)
        self.progressBar_protocols.setObjectName(u"progressBar_protocols")
        self.progressBar_protocols.setMaximumSize(QSize(400, 16777215))
        self.progressBar_protocols.setValue(0)

        self.gridLayout_5.addWidget(self.progressBar_protocols, 5, 9, 1, 3)

        self.textEdit_console_output = Console_TextEdit(self.centralwidget)
        self.textEdit_console_output.setObjectName(u"textEdit_console_output")
        self.textEdit_console_output.setMaximumSize(QSize(400, 16777215))
        self.textEdit_console_output.setTextInteractionFlags(Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)

        self.gridLayout_5.addWidget(self.textEdit_console_output, 6, 9, 2, 3)

        self.label_no_instruments = QLabel(self.centralwidget)
        self.label_no_instruments.setObjectName(u"label_no_instruments")

        self.gridLayout_5.addWidget(self.label_no_instruments, 2, 3, 1, 9)

        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setMaximumSize(QSize(16777215, 50))
        self.gridLayout_6 = QGridLayout(self.widget)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.comboBox_user = QComboBox(self.widget)
        self.comboBox_user.setObjectName(u"comboBox_user")
        font = QFont()
        font.setPointSize(10)
        self.comboBox_user.setFont(font)

        self.gridLayout_6.addWidget(self.comboBox_user, 0, 2, 1, 1)

        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMaximumSize(QSize(70, 16777215))
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(True)
        self.label.setFont(font1)
        self.label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_6.addWidget(self.label, 0, 1, 1, 1)

        self.pushButton_manage_instr = QPushButton(self.widget)
        self.pushButton_manage_instr.setObjectName(u"pushButton_manage_instr")
        font2 = QFont()
        font2.setPointSize(12)
        font2.setBold(True)
        self.pushButton_manage_instr.setFont(font2)

        self.gridLayout_6.addWidget(self.pushButton_manage_instr, 0, 0, 1, 1)

        self.label_8 = QLabel(self.widget)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMaximumSize(QSize(70, 16777215))
        self.label_8.setFont(font1)
        self.label_8.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_8, 0, 5, 1, 1)

        self.pushButton_editSampleInfo = QPushButton(self.widget)
        self.pushButton_editSampleInfo.setObjectName(u"pushButton_editSampleInfo")
        self.pushButton_editSampleInfo.setFont(font)

        self.gridLayout_6.addWidget(self.pushButton_editSampleInfo, 0, 8, 1, 1)

        self.pushButton_editUserInfo = QPushButton(self.widget)
        self.pushButton_editUserInfo.setObjectName(u"pushButton_editUserInfo")
        self.pushButton_editUserInfo.setFont(font)

        self.gridLayout_6.addWidget(self.pushButton_editUserInfo, 0, 3, 1, 1)

        self.comboBox_sample = QComboBox(self.widget)
        self.comboBox_sample.setObjectName(u"comboBox_sample")
        self.comboBox_sample.setFont(font)

        self.gridLayout_6.addWidget(self.comboBox_sample, 0, 7, 1, 1)

        self.line = QFrame(self.widget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.gridLayout_6.addWidget(self.line, 0, 4, 1, 1)

        self.line_2 = QFrame(self.widget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.gridLayout_6.addWidget(self.line_2, 0, 9, 1, 1)

        self.label_4 = QLabel(self.widget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMaximumSize(QSize(70, 16777215))
        self.label_4.setFont(font1)
        self.label_4.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_4, 0, 10, 1, 1)

        self.lineEdit_session = QLineEdit(self.widget)
        self.lineEdit_session.setObjectName(u"lineEdit_session")

        self.gridLayout_6.addWidget(self.lineEdit_session, 0, 11, 1, 1)


        self.gridLayout_5.addWidget(self.widget, 1, 2, 1, 10)

        self.label_logo = QLabel(self.centralwidget)
        self.label_logo.setObjectName(u"label_logo")
        self.label_logo.setMaximumSize(QSize(16777215, 70))
        self.label_logo.setPixmap(QPixmap(u"../graphics/camels_horizontal.png"))
        self.label_logo.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_logo, 8, 9, 1, 3)

        self.main_splitter = QSplitter(self.centralwidget)
        self.main_splitter.setObjectName(u"main_splitter")
        self.main_splitter.setOrientation(Qt.Vertical)
        self.manual_widget = QWidget(self.main_splitter)
        self.manual_widget.setObjectName(u"manual_widget")
        self.gridLayout = QGridLayout(self.manual_widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 1, 2, 1, 1)

        self.pushButton_add_manual = QPushButton(self.manual_widget)
        self.pushButton_add_manual.setObjectName(u"pushButton_add_manual")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton_add_manual.sizePolicy().hasHeightForWidth())
        self.pushButton_add_manual.setSizePolicy(sizePolicy1)
        self.pushButton_add_manual.setMinimumSize(QSize(70, 70))
        self.pushButton_add_manual.setMaximumSize(QSize(70, 70))
        font3 = QFont()
        font3.setFamilies([u"Calibri"])
        font3.setPointSize(75)
        font3.setBold(True)
        self.pushButton_add_manual.setFont(font3)
        self.pushButton_add_manual.setStyleSheet(u"QPushButton {\n"
"	font-family: Calibri;\n"
"	font-size: 75pt;\n"
"	font-weight: bold;\n"
"	padding: 0px;\n"
"	padding-bottom: 10px;\n"
"}")

        self.gridLayout.addWidget(self.pushButton_add_manual, 1, 1, 1, 1)

        self.label_2 = QLabel(self.manual_widget)
        self.label_2.setObjectName(u"label_2")
        font4 = QFont()
        font4.setFamilies([u"Calibri"])
        font4.setPointSize(20)
        font4.setBold(True)
        self.label_2.setFont(font4)
        self.label_2.setStyleSheet(u"QLabel {\n"
"	font-family: Calibri;\n"
"	font-size: 20pt;\n"
"	font-weight: bold;\n"
"}")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.main_splitter.addWidget(self.manual_widget)
        self.meas_widget = QWidget(self.main_splitter)
        self.meas_widget.setObjectName(u"meas_widget")
        self.gridLayout_2 = QGridLayout(self.meas_widget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_2, 1, 2, 1, 1)

        self.label_3 = QLabel(self.meas_widget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font4)
        self.label_3.setStyleSheet(u"QLabel {\n"
"	font-family: Calibri;\n"
"	font-size: 20pt;\n"
"	font-weight: bold;\n"
"}")

        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 1)

        self.pushButton_add_meas = QPushButton(self.meas_widget)
        self.pushButton_add_meas.setObjectName(u"pushButton_add_meas")
        sizePolicy1.setHeightForWidth(self.pushButton_add_meas.sizePolicy().hasHeightForWidth())
        self.pushButton_add_meas.setSizePolicy(sizePolicy1)
        self.pushButton_add_meas.setMinimumSize(QSize(70, 70))
        self.pushButton_add_meas.setMaximumSize(QSize(70, 70))
        font5 = QFont()
        font5.setFamilies([u"Calibri"])
        font5.setPointSize(75)
        font5.setBold(True)
        font5.setKerning(True)
        self.pushButton_add_meas.setFont(font5)
        self.pushButton_add_meas.setStyleSheet(u"QPushButton {\n"
"	font-family: Calibri;\n"
"	font-size: 75pt;\n"
"	font-weight: bold;\n"
"	padding: 0px;\n"
"	padding-bottom: 10px;\n"
"}")

        self.gridLayout_2.addWidget(self.pushButton_add_meas, 1, 1, 1, 1)

        self.main_splitter.addWidget(self.meas_widget)

        self.gridLayout_5.addWidget(self.main_splitter, 4, 2, 5, 7)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1021, 21))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        self.menuTools = QMenu(self.menubar)
        self.menuTools.setObjectName(u"menuTools")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionNew_Preset)
        self.menuFile.addAction(self.actionSave_Preset)
        self.menuFile.addAction(self.actionSave_Preset_As)
        self.menuFile.addAction(self.actionLoad_Backup_Preset)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSettings)
        self.menuHelp.addAction(self.actionDocumentation)
        self.menuHelp.addAction(self.actionReport_Bug)
        self.menuTools.addAction(self.actionDevice_Driver_Builder)
        self.menuTools.addAction(self.actionVISA_device_builder)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionPresets.setText(QCoreApplication.translate("MainWindow", u"Device-Presets", None))
        self.actionOptions.setText(QCoreApplication.translate("MainWindow", u"Options", None))
        self.actionSave_Device_Preset_As.setText(QCoreApplication.translate("MainWindow", u"Save Device Preset As", None))
        self.actionLoad.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.actionMeasurement_Presets.setText(QCoreApplication.translate("MainWindow", u"Measurement-Presets", None))
        self.actionSave_Preset.setText(QCoreApplication.translate("MainWindow", u"Save Preset", None))
        self.actionOpen_Backup_Device_Preset.setText(QCoreApplication.translate("MainWindow", u"Load Backup Device Preset", None))
        self.actionLoad_Backup_Preset.setText(QCoreApplication.translate("MainWindow", u"Load Preset", None))
        self.actionAutosave_on_closing.setText(QCoreApplication.translate("MainWindow", u"Autosave on closing", None))
        self.actionDevice_Driver_Builder.setText(QCoreApplication.translate("MainWindow", u"Update CAMELS", None))
        self.actionDark_Mode.setText(QCoreApplication.translate("MainWindow", u"Dark Mode", None))
        self.actionUndo.setText(QCoreApplication.translate("MainWindow", u"Undo (ctrl + z)", None))
        self.actionRedo.setText(QCoreApplication.translate("MainWindow", u"Redo (ctrl + y)", None))
        self.actionSettings.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.actionIOC_Builder.setText(QCoreApplication.translate("MainWindow", u"IOC-Builder", None))
        self.actionNew_Device_Preset_2.setText(QCoreApplication.translate("MainWindow", u"New Device Preset", None))
        self.actionSave_Device_Preset.setText(QCoreApplication.translate("MainWindow", u"Save Device Preset", None))
        self.actionSave_Preset_As.setText(QCoreApplication.translate("MainWindow", u"Save Preset As", None))
        self.actionNew_Preset.setText(QCoreApplication.translate("MainWindow", u"New Preset", None))
        self.actionNew_Device_Preset.setText(QCoreApplication.translate("MainWindow", u"New Device Preset", None))
        self.actionDocumentation.setText(QCoreApplication.translate("MainWindow", u"Documentation", None))
        self.actionReport_Bug.setText(QCoreApplication.translate("MainWindow", u"Report Bug", None))
        self.actionVISA_device_builder.setText(QCoreApplication.translate("MainWindow", u"VISA-device builder", None))
        self.label_arrow.setText("")
        self.pushButton_stop.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.pushButton_resume.setText(QCoreApplication.translate("MainWindow", u"Resume", None))
        self.pushButton_pause.setText(QCoreApplication.translate("MainWindow", u"Pause", None))
        self.label_no_instruments.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">You are currently using no instruments.</span></p><p><span style=\" font-size:12pt; font-weight:600;\">Click &quot;Manage Instruments&quot; to configure your</span></p><p><span style=\" font-size:12pt; font-weight:600;\">first instrument and start with CAMELS!</span></p></body></html>", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"User:", None))
        self.pushButton_manage_instr.setText(QCoreApplication.translate("MainWindow", u"Mangage\n"
"Instruments", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Sample:", None))
        self.pushButton_editSampleInfo.setText(QCoreApplication.translate("MainWindow", u"Edit Sample-Information", None))
        self.pushButton_editUserInfo.setText(QCoreApplication.translate("MainWindow", u"Edit User-Information", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Session:", None))
        self.label_logo.setText("")
        self.pushButton_add_manual.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Manual Control", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Measurement Protocols", None))
        self.pushButton_add_meas.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.menuTools.setTitle(QCoreApplication.translate("MainWindow", u"Tools", None))
    # retranslateUi

