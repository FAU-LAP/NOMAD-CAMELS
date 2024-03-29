# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainWindow_v2.ui'
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
    QAction,
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
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMenu,
    QMenuBar,
    QProgressBar,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QSplitter,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)

from nomad_camels.ui_widgets.console_redirect import Console_TextEdit


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1059, 345)
        self.actionPresets = QAction(MainWindow)
        self.actionPresets.setObjectName("actionPresets")
        self.actionOptions = QAction(MainWindow)
        self.actionOptions.setObjectName("actionOptions")
        self.actionSave_Device_Preset_As = QAction(MainWindow)
        self.actionSave_Device_Preset_As.setObjectName("actionSave_Device_Preset_As")
        self.actionLoad = QAction(MainWindow)
        self.actionLoad.setObjectName("actionLoad")
        self.actionMeasurement_Presets = QAction(MainWindow)
        self.actionMeasurement_Presets.setObjectName("actionMeasurement_Presets")
        self.actionSave_Preset = QAction(MainWindow)
        self.actionSave_Preset.setObjectName("actionSave_Preset")
        self.actionOpen_Backup_Device_Preset = QAction(MainWindow)
        self.actionOpen_Backup_Device_Preset.setObjectName(
            "actionOpen_Backup_Device_Preset"
        )
        self.actionLoad_Backup_Preset = QAction(MainWindow)
        self.actionLoad_Backup_Preset.setObjectName("actionLoad_Backup_Preset")
        self.actionAutosave_on_closing = QAction(MainWindow)
        self.actionAutosave_on_closing.setObjectName("actionAutosave_on_closing")
        self.actionAutosave_on_closing.setCheckable(True)
        self.actionUpdate_CAMELS = QAction(MainWindow)
        self.actionUpdate_CAMELS.setObjectName("actionUpdate_CAMELS")
        self.actionDark_Mode = QAction(MainWindow)
        self.actionDark_Mode.setObjectName("actionDark_Mode")
        self.actionDark_Mode.setCheckable(True)
        self.actionUndo = QAction(MainWindow)
        self.actionUndo.setObjectName("actionUndo")
        self.actionRedo = QAction(MainWindow)
        self.actionRedo.setObjectName("actionRedo")
        self.actionSettings = QAction(MainWindow)
        self.actionSettings.setObjectName("actionSettings")
        self.actionIOC_Builder = QAction(MainWindow)
        self.actionIOC_Builder.setObjectName("actionIOC_Builder")
        self.actionNew_Device_Preset_2 = QAction(MainWindow)
        self.actionNew_Device_Preset_2.setObjectName("actionNew_Device_Preset_2")
        self.actionSave_Device_Preset = QAction(MainWindow)
        self.actionSave_Device_Preset.setObjectName("actionSave_Device_Preset")
        self.actionSave_Preset_As = QAction(MainWindow)
        self.actionSave_Preset_As.setObjectName("actionSave_Preset_As")
        self.actionNew_Preset = QAction(MainWindow)
        self.actionNew_Preset.setObjectName("actionNew_Preset")
        self.actionNew_Device_Preset = QAction(MainWindow)
        self.actionNew_Device_Preset.setObjectName("actionNew_Device_Preset")
        self.actionDocumentation = QAction(MainWindow)
        self.actionDocumentation.setObjectName("actionDocumentation")
        self.actionReport_Bug = QAction(MainWindow)
        self.actionReport_Bug.setObjectName("actionReport_Bug")
        self.action_driver_builder = QAction(MainWindow)
        self.action_driver_builder.setObjectName("action_driver_builder")
        self.actionEPICS_driver_builder = QAction(MainWindow)
        self.actionEPICS_driver_builder.setObjectName("actionEPICS_driver_builder")
        self.actionExport_from_databroker = QAction(MainWindow)
        self.actionExport_from_databroker.setObjectName("actionExport_from_databroker")
        self.actionManage_Extensions = QAction(MainWindow)
        self.actionManage_Extensions.setObjectName("actionManage_Extensions")
        self.actionExport_CAMELS_hdf5_to_csv_json = QAction(MainWindow)
        self.actionExport_CAMELS_hdf5_to_csv_json.setObjectName(
            "actionExport_CAMELS_hdf5_to_csv_json"
        )
        self.actionQuit = QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_5 = QGridLayout(self.centralwidget)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.textEdit_console_output = Console_TextEdit(self.centralwidget)
        self.textEdit_console_output.setObjectName("textEdit_console_output")
        self.textEdit_console_output.setMaximumSize(QSize(400, 16777215))
        self.textEdit_console_output.setTextInteractionFlags(
            Qt.TextSelectableByKeyboard | Qt.TextSelectableByMouse
        )

        self.gridLayout_5.addWidget(self.textEdit_console_output, 6, 9, 2, 3)

        self.pushButton_clear_log = QPushButton(self.centralwidget)
        self.pushButton_clear_log.setObjectName("pushButton_clear_log")
        self.pushButton_clear_log.setStyleSheet("")

        self.gridLayout_5.addWidget(self.pushButton_clear_log, 8, 9, 1, 2)

        self.pushButton_stop = QPushButton(self.centralwidget)
        self.pushButton_stop.setObjectName("pushButton_stop")
        self.pushButton_stop.setEnabled(False)
        self.pushButton_stop.setMaximumSize(QSize(130, 16777215))
        self.pushButton_stop.setStyleSheet(
            "QPushButton {\n"
            "                background-color: #E60000; \n"
            "                color: white; \n"
            "                                border: none; \n"
            "                                padding: 2px 10px; \n"
            "                                text-align: center; \n"
            "                                text-decoration: none; \n"
            "                                font-size: 13px; \n"
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
            "    }"
        )

        self.gridLayout_5.addWidget(self.pushButton_stop, 4, 11, 1, 1)

        self.progressBar_protocols = QProgressBar(self.centralwidget)
        self.progressBar_protocols.setObjectName("progressBar_protocols")
        self.progressBar_protocols.setMaximumSize(QSize(400, 16777215))
        self.progressBar_protocols.setValue(0)

        self.gridLayout_5.addWidget(self.progressBar_protocols, 5, 9, 1, 3)

        self.label_logo = QLabel(self.centralwidget)
        self.label_logo.setObjectName("label_logo")
        self.label_logo.setMaximumSize(QSize(16777215, 70))
        self.label_logo.setPixmap(QPixmap("../graphics/camels_horizontal.png"))
        self.label_logo.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_logo, 9, 9, 1, 3)

        self.menu_widget = QWidget(self.centralwidget)
        self.menu_widget.setObjectName("menu_widget")
        self.menu_widget.setMaximumSize(QSize(16777215, 60))
        self.gridLayout_6 = QGridLayout(self.menu_widget)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.pushButton_manage_instr = QPushButton(self.menu_widget)
        self.pushButton_manage_instr.setObjectName("pushButton_manage_instr")
        self.pushButton_manage_instr.setMaximumSize(QSize(150, 16777215))
        font = QFont()
        font.setBold(True)
        font.setUnderline(False)
        font.setStrikeOut(False)
        self.pushButton_manage_instr.setFont(font)
        self.pushButton_manage_instr.setStyleSheet(
            "QPushButton {\n"
            "        background-color: #2a4cdf;\n"
            "        color: white;\n"
            "        border: none;\n"
            "        padding: 2px 10px;\n"
            "        text-align: center;\n"
            "        text-decoration: none;\n"
            "        font-size: 15px;\n"
            "        margin: 2px 2px;\n"
            "        border-radius: 6px;\n"
            "        font-weight: bold;\n"
            "    }\n"
            "\n"
            "    QPushButton:hover {\n"
            "        background-color: #1a3cbf;\n"
            "    }"
        )

        self.gridLayout_6.addWidget(self.pushButton_manage_instr, 0, 0, 1, 1)

        self.line_2 = QFrame(self.menu_widget)
        self.line_2.setObjectName("line_2")
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.gridLayout_6.addWidget(self.line_2, 0, 13, 1, 1)

        self.line = QFrame(self.menu_widget)
        self.line.setObjectName("line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.gridLayout_6.addWidget(self.line, 0, 8, 1, 1)

        self.comboBox_user_type = QComboBox(self.menu_widget)
        self.comboBox_user_type.setObjectName("comboBox_user_type")
        self.comboBox_user_type.setMaximumSize(QSize(110, 16777215))

        self.gridLayout_6.addWidget(self.comboBox_user_type, 0, 1, 1, 1)

        self.sample_widget = QWidget(self.menu_widget)
        self.sample_widget.setObjectName("sample_widget")
        self.verticalLayout_2 = QVBoxLayout(self.sample_widget)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.sample_widget_default = QWidget(self.sample_widget)
        self.sample_widget_default.setObjectName("sample_widget_default")
        self.horizontalLayout_4 = QHBoxLayout(self.sample_widget_default)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 3, 0, 3)
        self.comboBox_sample = QComboBox(self.sample_widget_default)
        self.comboBox_sample.setObjectName("comboBox_sample")
        font1 = QFont()
        font1.setPointSize(10)
        self.comboBox_sample.setFont(font1)

        self.horizontalLayout_4.addWidget(self.comboBox_sample)

        self.pushButton_editSampleInfo = QPushButton(self.sample_widget_default)
        self.pushButton_editSampleInfo.setObjectName("pushButton_editSampleInfo")
        self.pushButton_editSampleInfo.setFont(font)
        self.pushButton_editSampleInfo.setStyleSheet(
            "QPushButton {\n"
            "        background-color: #2a4cdf;\n"
            "        color: white;\n"
            "        border: none;\n"
            "        padding: 2px 10px;\n"
            "        text-align: center;\n"
            "        text-decoration: none;\n"
            "        font-size: 12px;\n"
            "        margin: 2px 2px;\n"
            "        border-radius: 6px;\n"
            "        font-weight: bold;\n"
            "    }\n"
            "\n"
            "    QPushButton:hover {\n"
            "        background-color: #1a3cbf;\n"
            "    }"
        )

        self.horizontalLayout_4.addWidget(self.pushButton_editSampleInfo)

        self.verticalLayout_2.addWidget(self.sample_widget_default)

        self.sample_widget_nomad = QWidget(self.sample_widget)
        self.sample_widget_nomad.setObjectName("sample_widget_nomad")
        self.horizontalLayout_3 = QHBoxLayout(self.sample_widget_nomad)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 3, 0, 3)
        self.checkBox_use_nomad_sample = QCheckBox(self.sample_widget_nomad)
        self.checkBox_use_nomad_sample.setObjectName("checkBox_use_nomad_sample")

        self.horizontalLayout_3.addWidget(self.checkBox_use_nomad_sample)

        self.pushButton_nomad_sample = QPushButton(self.sample_widget_nomad)
        self.pushButton_nomad_sample.setObjectName("pushButton_nomad_sample")
        self.pushButton_nomad_sample.setFont(font)
        self.pushButton_nomad_sample.setStyleSheet(
            "QPushButton {\n"
            "        background-color: #2a4cdf;\n"
            "        color: white;\n"
            "        border: none;\n"
            "        padding: 2px 10px;\n"
            "        text-align: center;\n"
            "        text-decoration: none;\n"
            "        font-size: 12px;\n"
            "        margin: 2px 2px;\n"
            "        border-radius: 6px;\n"
            "        font-weight: bold;\n"
            "    }\n"
            "\n"
            "    QPushButton:hover {\n"
            "        background-color: #1a3cbf;\n"
            "    }"
        )

        self.horizontalLayout_3.addWidget(self.pushButton_nomad_sample)

        self.verticalLayout_2.addWidget(self.sample_widget_nomad)

        self.gridLayout_6.addWidget(self.sample_widget, 0, 10, 1, 1)

        self.session_upload_widget = QWidget(self.menu_widget)
        self.session_upload_widget.setObjectName("session_upload_widget")
        self.verticalLayout_3 = QVBoxLayout(self.session_upload_widget)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.nomad_upload_widget = QWidget(self.session_upload_widget)
        self.nomad_upload_widget.setObjectName("nomad_upload_widget")
        self.horizontalLayout_6 = QHBoxLayout(self.nomad_upload_widget)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 3, 0, 3)
        self.label_nomad_upload = QLabel(self.nomad_upload_widget)
        self.label_nomad_upload.setObjectName("label_nomad_upload")
        font2 = QFont()
        font2.setPointSize(10)
        font2.setBold(True)
        self.label_nomad_upload.setFont(font2)

        self.horizontalLayout_6.addWidget(self.label_nomad_upload)

        self.comboBox_upload_type = QComboBox(self.nomad_upload_widget)
        self.comboBox_upload_type.setObjectName("comboBox_upload_type")

        self.horizontalLayout_6.addWidget(self.comboBox_upload_type)

        self.comboBox_upload_choice = QComboBox(self.nomad_upload_widget)
        self.comboBox_upload_choice.setObjectName("comboBox_upload_choice")

        self.horizontalLayout_6.addWidget(self.comboBox_upload_choice)

        self.verticalLayout_3.addWidget(self.nomad_upload_widget)

        self.session_widget = QWidget(self.session_upload_widget)
        self.session_widget.setObjectName("session_widget")
        self.horizontalLayout_5 = QHBoxLayout(self.session_widget)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 3, 0, 3)
        self.label_4 = QLabel(self.session_widget)
        self.label_4.setObjectName("label_4")
        self.label_4.setMaximumSize(QSize(1500000, 16777215))
        self.label_4.setFont(font2)
        self.label_4.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.label_4)

        self.lineEdit_session = QLineEdit(self.session_widget)
        self.lineEdit_session.setObjectName("lineEdit_session")

        self.horizontalLayout_5.addWidget(self.lineEdit_session)

        self.verticalLayout_3.addWidget(self.session_widget)

        self.gridLayout_6.addWidget(self.session_upload_widget, 0, 15, 1, 1)

        self.user_widget = QWidget(self.menu_widget)
        self.user_widget.setObjectName("user_widget")
        self.verticalLayout = QVBoxLayout(self.user_widget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.user_widget_default = QWidget(self.user_widget)
        self.user_widget_default.setObjectName("user_widget_default")
        self.horizontalLayout = QHBoxLayout(self.user_widget_default)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 3, 0, 3)
        self.comboBox_user = QComboBox(self.user_widget_default)
        self.comboBox_user.setObjectName("comboBox_user")
        self.comboBox_user.setFont(font1)

        self.horizontalLayout.addWidget(self.comboBox_user)

        self.pushButton_editUserInfo = QPushButton(self.user_widget_default)
        self.pushButton_editUserInfo.setObjectName("pushButton_editUserInfo")
        self.pushButton_editUserInfo.setFont(font)
        self.pushButton_editUserInfo.setStyleSheet(
            "QPushButton {\n"
            "        background-color: #2a4cdf;\n"
            "        color: white;\n"
            "        border: none;\n"
            "        padding: 2px 10px;\n"
            "        text-align: center;\n"
            "        text-decoration: none;\n"
            "        font-size: 12px;\n"
            "        margin: 2px 2px;\n"
            "        border-radius: 6px;\n"
            "        font-weight: bold;\n"
            "    }\n"
            "\n"
            "    QPushButton:hover {\n"
            "        background-color: #1a3cbf;\n"
            "    }"
        )

        self.horizontalLayout.addWidget(self.pushButton_editUserInfo)

        self.verticalLayout.addWidget(self.user_widget_default)

        self.user_widget_nomad = QWidget(self.user_widget)
        self.user_widget_nomad.setObjectName("user_widget_nomad")
        self.horizontalLayout_2 = QHBoxLayout(self.user_widget_nomad)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 3, 0, 3)
        self.label_nomad_user = QLabel(self.user_widget_nomad)
        self.label_nomad_user.setObjectName("label_nomad_user")
        self.label_nomad_user.setFont(font1)

        self.horizontalLayout_2.addWidget(self.label_nomad_user)

        self.pushButton_login_nomad = QPushButton(self.user_widget_nomad)
        self.pushButton_login_nomad.setObjectName("pushButton_login_nomad")
        self.pushButton_login_nomad.setFont(font)
        self.pushButton_login_nomad.setStyleSheet(
            "QPushButton {\n"
            "        background-color: #2a4cdf;\n"
            "        color: white;\n"
            "        border: none;\n"
            "        padding: 2px 10px;\n"
            "        text-align: center;\n"
            "        text-decoration: none;\n"
            "        font-size: 12px;\n"
            "        margin: 2px 2px;\n"
            "        border-radius: 6px;\n"
            "        font-weight: bold;\n"
            "    }\n"
            "\n"
            "    QPushButton:hover {\n"
            "        background-color: #1a3cbf;\n"
            "    }"
        )

        self.horizontalLayout_2.addWidget(self.pushButton_login_nomad)

        self.verticalLayout.addWidget(self.user_widget_nomad)

        self.gridLayout_6.addWidget(self.user_widget, 0, 2, 1, 1)

        self.label_8 = QLabel(self.menu_widget)
        self.label_8.setObjectName("label_8")
        self.label_8.setMaximumSize(QSize(70, 16777215))
        self.label_8.setFont(font2)
        self.label_8.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_8, 0, 9, 1, 1)

        self.gridLayout_5.addWidget(self.menu_widget, 1, 2, 1, 10)

        self.widget_2 = QWidget(self.centralwidget)
        self.widget_2.setObjectName("widget_2")
        self.gridLayout_3 = QGridLayout(self.widget_2)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_no_instruments = QLabel(self.widget_2)
        self.label_no_instruments.setObjectName("label_no_instruments")

        self.gridLayout_3.addWidget(self.label_no_instruments, 0, 1, 1, 1)

        self.label_arrow = QLabel(self.widget_2)
        self.label_arrow.setObjectName("label_arrow")
        self.label_arrow.setMaximumSize(QSize(120, 16777215))
        self.label_arrow.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.label_arrow, 0, 0, 1, 1)

        self.main_splitter = QSplitter(self.widget_2)
        self.main_splitter.setObjectName("main_splitter")
        self.main_splitter.setOrientation(Qt.Vertical)
        self.manual_widget = QWidget(self.main_splitter)
        self.manual_widget.setObjectName("manual_widget")
        self.gridLayout = QGridLayout(self.manual_widget)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.gridLayout.addItem(self.horizontalSpacer, 1, 2, 1, 1)

        self.pushButton_add_manual = QPushButton(self.manual_widget)
        self.pushButton_add_manual.setObjectName("pushButton_add_manual")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButton_add_manual.sizePolicy().hasHeightForWidth()
        )
        self.pushButton_add_manual.setSizePolicy(sizePolicy)
        self.pushButton_add_manual.setMinimumSize(QSize(32, 32))
        self.pushButton_add_manual.setMaximumSize(QSize(32, 32))
        self.pushButton_add_manual.setFont(font)
        self.pushButton_add_manual.setStyleSheet(
            "QPushButton {\n"
            "                                background-color: #4CAF50; \n"
            "                                color: white; \n"
            "                                border: none; \n"
            "                                padding: 0px; \n"
            "                                padding-bottom: 5px;\n"
            "                                text-align: center; \n"
            "                                text-decoration: none; \n"
            "                                font-size: 30px; \n"
            "                                margin: 2px 2px; \n"
            "                                border-radius: 6px;\n"
            "								font-weight: bold;\n"
            "                            }\n"
            "\n"
            "                            QPushButton:hover {\n"
            "                                background-color: #45a049;\n"
            "                            }"
        )

        self.gridLayout.addWidget(self.pushButton_add_manual, 1, 1, 1, 1)

        self.label_2 = QLabel(self.manual_widget)
        self.label_2.setObjectName("label_2")
        font3 = QFont()
        font3.setFamilies(["Calibri"])
        font3.setPointSize(20)
        font3.setBold(True)
        self.label_2.setFont(font3)
        self.label_2.setStyleSheet(
            "QLabel {\n"
            "	font-family: Calibri;\n"
            "	font-size: 20pt;\n"
            "	font-weight: bold;\n"
            "}"
        )

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.main_splitter.addWidget(self.manual_widget)
        self.meas_widget = QWidget(self.main_splitter)
        self.meas_widget.setObjectName("meas_widget")
        self.gridLayout_2 = QGridLayout(self.meas_widget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalSpacer_2 = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.gridLayout_2.addItem(self.horizontalSpacer_2, 1, 3, 1, 1)

        self.label_3 = QLabel(self.meas_widget)
        self.label_3.setObjectName("label_3")
        self.label_3.setFont(font3)
        self.label_3.setStyleSheet(
            "QLabel {\n"
            "	font-family: Calibri;\n"
            "	font-size: 20pt;\n"
            "	font-weight: bold;\n"
            "}"
        )

        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 1)

        self.pushButton_add_meas = QPushButton(self.meas_widget)
        self.pushButton_add_meas.setObjectName("pushButton_add_meas")
        sizePolicy.setHeightForWidth(
            self.pushButton_add_meas.sizePolicy().hasHeightForWidth()
        )
        self.pushButton_add_meas.setSizePolicy(sizePolicy)
        self.pushButton_add_meas.setMinimumSize(QSize(32, 32))
        self.pushButton_add_meas.setMaximumSize(QSize(32, 32))
        self.pushButton_add_meas.setFont(font)
        self.pushButton_add_meas.setStyleSheet(
            "QPushButton {\n"
            "                                background-color: #4CAF50; \n"
            "                                color: white; \n"
            "                                border: none; \n"
            "                                padding: 0px; \n"
            "                                padding-bottom: 5px;\n"
            "                                text-align: center; \n"
            "                                text-decoration: none; \n"
            "                                font-size: 30px; \n"
            "                                margin: 2px 2px; \n"
            "                                border-radius: 6px;\n"
            "								font-weight: bold;\n"
            "                            }\n"
            "\n"
            "                            QPushButton:hover {\n"
            "                                background-color: #45a049;\n"
            "                            }"
        )

        self.gridLayout_2.addWidget(self.pushButton_add_meas, 1, 1, 1, 1)

        self.pushButton_import_protocol = QPushButton(self.meas_widget)
        self.pushButton_import_protocol.setObjectName("pushButton_import_protocol")
        sizePolicy.setHeightForWidth(
            self.pushButton_import_protocol.sizePolicy().hasHeightForWidth()
        )
        self.pushButton_import_protocol.setSizePolicy(sizePolicy)
        self.pushButton_import_protocol.setMinimumSize(QSize(32, 32))
        self.pushButton_import_protocol.setMaximumSize(QSize(60, 32))
        self.pushButton_import_protocol.setStyleSheet(
            "QPushButton {\n"
            "        background-color: #2a4cdf;\n"
            "        color: white;\n"
            "        border: none;\n"
            "        padding: 2px 10px;\n"
            "        text-align: center;\n"
            "        text-decoration: none;\n"
            "        font-size: 12px;\n"
            "        margin: 2px 2px;\n"
            "        border-radius: 6px;\n"
            "        font-weight: bold;\n"
            "    }\n"
            "\n"
            "    QPushButton:hover {\n"
            "        background-color: #1a3cbf;\n"
            "    }"
        )

        self.gridLayout_2.addWidget(self.pushButton_import_protocol, 1, 2, 1, 1)

        self.main_splitter.addWidget(self.meas_widget)

        self.gridLayout_3.addWidget(self.main_splitter, 1, 0, 1, 2)

        self.gridLayout_5.addWidget(self.widget_2, 4, 2, 6, 7)

        self.pushButton_pause = QPushButton(self.centralwidget)
        self.pushButton_pause.setObjectName("pushButton_pause")
        self.pushButton_pause.setEnabled(False)
        self.pushButton_pause.setMaximumSize(QSize(130, 16777215))
        self.pushButton_pause.setStyleSheet(
            "QPushButton {\n"
            "        background-color: #FFA500;\n"
            "        color: white;\n"
            "        border: none;\n"
            "        padding: 2px 10px;\n"
            "        text-align: center;\n"
            "        text-decoration: none;\n"
            "        font-size: 13px;\n"
            "        margin: 2px 2px;\n"
            "        border-radius: 6px;\n"
            "        font-weight: bold;\n"
            "    }\n"
            "\n"
            "    QPushButton:hover {\n"
            "        background-color: #FF8C00;\n"
            "    }\n"
            "QPushButton:disabled {\n"
            "        background-color: #808080;\n"
            "    }"
        )

        self.gridLayout_5.addWidget(self.pushButton_pause, 4, 10, 1, 1)

        self.pushButton_resume = QPushButton(self.centralwidget)
        self.pushButton_resume.setObjectName("pushButton_resume")
        self.pushButton_resume.setEnabled(False)
        self.pushButton_resume.setMaximumSize(QSize(130, 16777215))
        self.pushButton_resume.setStyleSheet(
            "QPushButton {\n"
            "                                background-color: #4CAF50; \n"
            "                                color: white; \n"
            "                                border: none; \n"
            "                                padding: 2px 10px; \n"
            "                                text-align: center; \n"
            "                                text-decoration: none; \n"
            "                                font-size: 13px; \n"
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

        self.gridLayout_5.addWidget(self.pushButton_resume, 4, 9, 1, 1)

        self.pushButton_close_plots = QPushButton(self.centralwidget)
        self.pushButton_close_plots.setObjectName("pushButton_close_plots")
        self.pushButton_close_plots.setStyleSheet("")

        self.gridLayout_5.addWidget(self.pushButton_close_plots, 8, 11, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QRect(0, 0, 1059, 21))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuTools = QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
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
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuHelp.addAction(self.actionDocumentation)
        self.menuHelp.addAction(self.actionReport_Bug)
        self.menuTools.addAction(self.actionUpdate_CAMELS)
        self.menuTools.addSeparator()
        self.menuTools.addAction(self.actionExport_from_databroker)
        self.menuTools.addAction(self.actionExport_CAMELS_hdf5_to_csv_json)
        self.menuTools.addSeparator()
        self.menuTools.addAction(self.action_driver_builder)
        self.menuTools.addAction(self.actionEPICS_driver_builder)
        self.menuTools.addSeparator()
        self.menuTools.addAction(self.actionManage_Extensions)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", "MainWindow", None)
        )
        self.actionPresets.setText(
            QCoreApplication.translate("MainWindow", "Device-Presets", None)
        )
        self.actionOptions.setText(
            QCoreApplication.translate("MainWindow", "Options", None)
        )
        self.actionSave_Device_Preset_As.setText(
            QCoreApplication.translate("MainWindow", "Save Device Preset As", None)
        )
        self.actionLoad.setText(QCoreApplication.translate("MainWindow", "Open", None))
        self.actionMeasurement_Presets.setText(
            QCoreApplication.translate("MainWindow", "Measurement-Presets", None)
        )
        self.actionSave_Preset.setText(
            QCoreApplication.translate("MainWindow", "Save Preset", None)
        )
        self.actionOpen_Backup_Device_Preset.setText(
            QCoreApplication.translate("MainWindow", "Load Backup Device Preset", None)
        )
        self.actionLoad_Backup_Preset.setText(
            QCoreApplication.translate("MainWindow", "Load Preset", None)
        )
        self.actionAutosave_on_closing.setText(
            QCoreApplication.translate("MainWindow", "Autosave on closing", None)
        )
        self.actionUpdate_CAMELS.setText(
            QCoreApplication.translate("MainWindow", "Update NOMAD-CAMELS", None)
        )
        self.actionDark_Mode.setText(
            QCoreApplication.translate("MainWindow", "Dark Mode", None)
        )
        self.actionUndo.setText(
            QCoreApplication.translate("MainWindow", "Undo (ctrl + z)", None)
        )
        self.actionRedo.setText(
            QCoreApplication.translate("MainWindow", "Redo (ctrl + y)", None)
        )
        self.actionSettings.setText(
            QCoreApplication.translate("MainWindow", "Settings", None)
        )
        self.actionIOC_Builder.setText(
            QCoreApplication.translate("MainWindow", "IOC-Builder", None)
        )
        self.actionNew_Device_Preset_2.setText(
            QCoreApplication.translate("MainWindow", "New Device Preset", None)
        )
        self.actionSave_Device_Preset.setText(
            QCoreApplication.translate("MainWindow", "Save Device Preset", None)
        )
        self.actionSave_Preset_As.setText(
            QCoreApplication.translate("MainWindow", "Save Preset As", None)
        )
        self.actionNew_Preset.setText(
            QCoreApplication.translate("MainWindow", "New Preset", None)
        )
        self.actionNew_Device_Preset.setText(
            QCoreApplication.translate("MainWindow", "New Device Preset", None)
        )
        self.actionDocumentation.setText(
            QCoreApplication.translate("MainWindow", "Documentation", None)
        )
        self.actionReport_Bug.setText(
            QCoreApplication.translate("MainWindow", "Report Bug", None)
        )
        self.action_driver_builder.setText(
            QCoreApplication.translate("MainWindow", "Driver builder", None)
        )
        self.actionEPICS_driver_builder.setText(
            QCoreApplication.translate("MainWindow", "EPICS-driver-builder", None)
        )
        self.actionExport_from_databroker.setText(
            QCoreApplication.translate("MainWindow", "Export from databroker", None)
        )
        self.actionManage_Extensions.setText(
            QCoreApplication.translate("MainWindow", "Manage Extensions", None)
        )
        self.actionExport_CAMELS_hdf5_to_csv_json.setText(
            QCoreApplication.translate(
                "MainWindow", "Export CAMELS hdf5 to csv/json", None
            )
        )
        self.actionQuit.setText(QCoreApplication.translate("MainWindow", "Quit", None))
        self.pushButton_clear_log.setText(
            QCoreApplication.translate("MainWindow", "Clear Log", None)
        )
        self.pushButton_stop.setText(
            QCoreApplication.translate("MainWindow", "Stop", None)
        )
        self.label_logo.setText("")
        self.pushButton_manage_instr.setText(
            QCoreApplication.translate("MainWindow", "Manage\n" "Instruments", None)
        )
        self.pushButton_editSampleInfo.setText(
            QCoreApplication.translate("MainWindow", "Edit Sample-Information", None)
        )
        self.checkBox_use_nomad_sample.setText(
            QCoreApplication.translate("MainWindow", "use NOMAD sample", None)
        )
        self.pushButton_nomad_sample.setText(
            QCoreApplication.translate("MainWindow", "select NOMAD sample", None)
        )
        self.label_nomad_upload.setText(
            QCoreApplication.translate("MainWindow", "NOMAD Upload:", None)
        )
        self.label_4.setText(QCoreApplication.translate("MainWindow", "Session:", None))
        self.pushButton_editUserInfo.setText(
            QCoreApplication.translate("MainWindow", "Edit User-Information", None)
        )
        self.label_nomad_user.setText(
            QCoreApplication.translate("MainWindow", "not logged in", None)
        )
        self.pushButton_login_nomad.setText(
            QCoreApplication.translate("MainWindow", "NOMAD login", None)
        )
        self.label_8.setText(QCoreApplication.translate("MainWindow", "Sample:", None))
        self.label_no_instruments.setText(
            QCoreApplication.translate(
                "MainWindow",
                '<html><head/><body><p><span style=" font-size:12pt; font-weight:600;">You are currently using no instruments.</span></p><p><span style=" font-size:12pt; font-weight:600;">Click &quot;Manage Instruments&quot; to configure your</span></p><p><span style=" font-size:12pt; font-weight:600;">first instrument and start with NOMAD CAMELS!</span></p></body></html>',
                None,
            )
        )
        self.label_arrow.setText("")
        self.pushButton_add_manual.setText(
            QCoreApplication.translate("MainWindow", "+", None)
        )
        self.label_2.setText(
            QCoreApplication.translate("MainWindow", "Manual Control", None)
        )
        self.label_3.setText(
            QCoreApplication.translate("MainWindow", "Measurement Protocols", None)
        )
        self.pushButton_add_meas.setText(
            QCoreApplication.translate("MainWindow", "+", None)
        )
        self.pushButton_import_protocol.setText(
            QCoreApplication.translate("MainWindow", "import", None)
        )
        self.pushButton_pause.setText(
            QCoreApplication.translate("MainWindow", "Pause", None)
        )
        self.pushButton_resume.setText(
            QCoreApplication.translate("MainWindow", "Resume", None)
        )
        self.pushButton_close_plots.setText(
            QCoreApplication.translate("MainWindow", "Close Plots", None)
        )
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", "File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", "Help", None))
        self.menuTools.setTitle(QCoreApplication.translate("MainWindow", "Tools", None))

    # retranslateUi
