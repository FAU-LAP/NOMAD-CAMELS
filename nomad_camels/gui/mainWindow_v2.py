# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainWindow_v2.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QGridLayout, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QListWidgetItem, QMainWindow, QMenu,
    QMenuBar, QProgressBar, QPushButton, QScrollArea,
    QSizePolicy, QSpacerItem, QSplitter, QStatusBar,
    QTextEdit, QVBoxLayout, QWidget)

from dynamicuploadcombobox import DynamicUploadComboBox
from nomad_camels.ui_widgets.console_redirect import Console_TextEdit
from nomad_camels.ui_widgets.run_queue import RunQueue
from nomad_camels.ui_widgets.variable_table import VariableTable
from nomad_camels.ui_widgets.variable_tool_tip_box import Variable_Box

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1322, 610)
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
        self.actionUpdate_CAMELS = QAction(MainWindow)
        self.actionUpdate_CAMELS.setObjectName(u"actionUpdate_CAMELS")
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
        self.action_driver_builder = QAction(MainWindow)
        self.action_driver_builder.setObjectName(u"action_driver_builder")
        self.actionEPICS_driver_builder = QAction(MainWindow)
        self.actionEPICS_driver_builder.setObjectName(u"actionEPICS_driver_builder")
        self.actionExport_from_databroker = QAction(MainWindow)
        self.actionExport_from_databroker.setObjectName(u"actionExport_from_databroker")
        self.actionManage_Extensions = QAction(MainWindow)
        self.actionManage_Extensions.setObjectName(u"actionManage_Extensions")
        self.actionExport_CAMELS_hdf5_to_csv_json = QAction(MainWindow)
        self.actionExport_CAMELS_hdf5_to_csv_json.setObjectName(u"actionExport_CAMELS_hdf5_to_csv_json")
        self.actionQuit = QAction(MainWindow)
        self.actionQuit.setObjectName(u"actionQuit")
        self.actionWatchdogs = QAction(MainWindow)
        self.actionWatchdogs.setObjectName(u"actionWatchdogs")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_5 = QGridLayout(self.centralwidget)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.gridLayout_4 = QGridLayout(self.widget)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.pushButton_resume = QPushButton(self.widget)
        self.pushButton_resume.setObjectName(u"pushButton_resume")
        self.pushButton_resume.setEnabled(False)
        self.pushButton_resume.setMaximumSize(QSize(130, 16777215))
        self.pushButton_resume.setStyleSheet(u"QPushButton {\n"
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
"    }")

        self.gridLayout_4.addWidget(self.pushButton_resume, 1, 0, 1, 1)

        self.textEdit_console_output = Console_TextEdit(self.widget)
        self.textEdit_console_output.setObjectName(u"textEdit_console_output")
        self.textEdit_console_output.setMaximumSize(QSize(16777215, 16777215))
        self.textEdit_console_output.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByKeyboard|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.gridLayout_4.addWidget(self.textEdit_console_output, 0, 4, 3, 1)

        self.pushButton_close_plots = QPushButton(self.widget)
        self.pushButton_close_plots.setObjectName(u"pushButton_close_plots")
        self.pushButton_close_plots.setStyleSheet(u"")

        self.gridLayout_4.addWidget(self.pushButton_close_plots, 3, 0, 1, 2)

        self.pushButton_stop = QPushButton(self.widget)
        self.pushButton_stop.setObjectName(u"pushButton_stop")
        self.pushButton_stop.setEnabled(False)
        self.pushButton_stop.setMaximumSize(QSize(130, 16777215))
        self.pushButton_stop.setStyleSheet(u"QPushButton {\n"
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
"    }")

        self.gridLayout_4.addWidget(self.pushButton_stop, 1, 2, 1, 1)

        self.pushButton_clear_log = QPushButton(self.widget)
        self.pushButton_clear_log.setObjectName(u"pushButton_clear_log")
        self.pushButton_clear_log.setStyleSheet(u"")

        self.gridLayout_4.addWidget(self.pushButton_clear_log, 3, 4, 1, 1)

        self.pushButton_pause = QPushButton(self.widget)
        self.pushButton_pause.setObjectName(u"pushButton_pause")
        self.pushButton_pause.setEnabled(False)
        self.pushButton_pause.setMaximumSize(QSize(130, 16777215))
        self.pushButton_pause.setStyleSheet(u"QPushButton {\n"
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
"    }")

        self.gridLayout_4.addWidget(self.pushButton_pause, 1, 1, 1, 1)

        self.queue_variable_table = VariableTable(self.widget)
        self.queue_variable_table.setObjectName(u"queue_variable_table")

        self.gridLayout_4.addWidget(self.queue_variable_table, 0, 3, 4, 1)

        self.pushButton_show_log = QPushButton(self.widget)
        self.pushButton_show_log.setObjectName(u"pushButton_show_log")

        self.gridLayout_4.addWidget(self.pushButton_show_log, 3, 2, 1, 1)

        self.gridLayout_7 = QGridLayout()
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.textEdit_meas_description = QTextEdit(self.widget)
        self.textEdit_meas_description.setObjectName(u"textEdit_meas_description")

        self.gridLayout_7.addWidget(self.textEdit_meas_description, 1, 0, 1, 1)

        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setBold(True)
        self.label.setFont(font)

        self.gridLayout_7.addWidget(self.label, 0, 0, 1, 1)

        self.run_queue_widget = RunQueue(self.widget)
        self.run_queue_widget.setObjectName(u"run_queue_widget")

        self.gridLayout_7.addWidget(self.run_queue_widget, 1, 1, 1, 1)

        self.label_queue = QLabel(self.widget)
        self.label_queue.setObjectName(u"label_queue")
        self.label_queue.setFont(font)

        self.gridLayout_7.addWidget(self.label_queue, 0, 1, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout_7, 0, 0, 1, 3)

        self.progressBar_protocols = QProgressBar(self.widget)
        self.progressBar_protocols.setObjectName(u"progressBar_protocols")
        self.progressBar_protocols.setMaximumSize(QSize(16777215, 16777215))
        self.progressBar_protocols.setValue(0)

        self.gridLayout_4.addWidget(self.progressBar_protocols, 2, 0, 1, 2)

        self.label_remaining_time = QLabel(self.widget)
        self.label_remaining_time.setObjectName(u"label_remaining_time")
        self.label_remaining_time.setEnabled(False)
        self.label_remaining_time.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.label_remaining_time, 2, 2, 1, 1)


        self.gridLayout_5.addWidget(self.widget, 4, 9, 1, 2)

        self.label_logo = QLabel(self.centralwidget)
        self.label_logo.setObjectName(u"label_logo")
        self.label_logo.setMaximumSize(QSize(16777215, 70))
        self.label_logo.setPixmap(QPixmap(u"../graphics/camels_horizontal.png"))
        self.label_logo.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_logo, 5, 9, 1, 2)

        self.menu_widget = QWidget(self.centralwidget)
        self.menu_widget.setObjectName(u"menu_widget")
        self.menu_widget.setMaximumSize(QSize(16777215, 60))
        self.gridLayout_6 = QGridLayout(self.menu_widget)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.pushButton_manage_instr = QPushButton(self.menu_widget)
        self.pushButton_manage_instr.setObjectName(u"pushButton_manage_instr")
        self.pushButton_manage_instr.setMaximumSize(QSize(150, 16777215))
        font1 = QFont()
        font1.setBold(True)
        font1.setUnderline(False)
        font1.setStrikeOut(False)
        self.pushButton_manage_instr.setFont(font1)
        self.pushButton_manage_instr.setStyleSheet(u"QPushButton {\n"
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
"    }")

        self.gridLayout_6.addWidget(self.pushButton_manage_instr, 0, 0, 1, 1)

        self.line_2 = QFrame(self.menu_widget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.VLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_6.addWidget(self.line_2, 0, 13, 1, 1)

        self.line = QFrame(self.menu_widget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_6.addWidget(self.line, 0, 8, 1, 1)

        self.comboBox_user_type = QComboBox(self.menu_widget)
        self.comboBox_user_type.setObjectName(u"comboBox_user_type")
        self.comboBox_user_type.setMaximumSize(QSize(110, 16777215))

        self.gridLayout_6.addWidget(self.comboBox_user_type, 0, 1, 1, 1)

        self.sample_widget = QWidget(self.menu_widget)
        self.sample_widget.setObjectName(u"sample_widget")
        self.verticalLayout_2 = QVBoxLayout(self.sample_widget)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.sample_widget_default = QWidget(self.sample_widget)
        self.sample_widget_default.setObjectName(u"sample_widget_default")
        self.horizontalLayout_4 = QHBoxLayout(self.sample_widget_default)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 3, 0, 3)
        self.comboBox_sample = QComboBox(self.sample_widget_default)
        self.comboBox_sample.setObjectName(u"comboBox_sample")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_sample.sizePolicy().hasHeightForWidth())
        self.comboBox_sample.setSizePolicy(sizePolicy)
        self.comboBox_sample.setMaximumSize(QSize(230, 16777215))
        font2 = QFont()
        font2.setPointSize(10)
        self.comboBox_sample.setFont(font2)

        self.horizontalLayout_4.addWidget(self.comboBox_sample)

        self.pushButton_editSampleInfo = QPushButton(self.sample_widget_default)
        self.pushButton_editSampleInfo.setObjectName(u"pushButton_editSampleInfo")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton_editSampleInfo.sizePolicy().hasHeightForWidth())
        self.pushButton_editSampleInfo.setSizePolicy(sizePolicy1)
        self.pushButton_editSampleInfo.setFont(font1)
        self.pushButton_editSampleInfo.setStyleSheet(u"QPushButton {\n"
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
"    }\n"
"QPushButton:disabled {\n"
"        background-color: #808080;\n"
"    }")

        self.horizontalLayout_4.addWidget(self.pushButton_editSampleInfo)


        self.verticalLayout_2.addWidget(self.sample_widget_default)

        self.sample_widget_nomad = QWidget(self.sample_widget)
        self.sample_widget_nomad.setObjectName(u"sample_widget_nomad")
        self.horizontalLayout_3 = QHBoxLayout(self.sample_widget_nomad)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 3, 0, 3)
        self.checkBox_use_nomad_sample = QCheckBox(self.sample_widget_nomad)
        self.checkBox_use_nomad_sample.setObjectName(u"checkBox_use_nomad_sample")

        self.horizontalLayout_3.addWidget(self.checkBox_use_nomad_sample)

        self.pushButton_nomad_sample = QPushButton(self.sample_widget_nomad)
        self.pushButton_nomad_sample.setObjectName(u"pushButton_nomad_sample")
        self.pushButton_nomad_sample.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.pushButton_nomad_sample.sizePolicy().hasHeightForWidth())
        self.pushButton_nomad_sample.setSizePolicy(sizePolicy1)
        self.pushButton_nomad_sample.setFont(font1)
        self.pushButton_nomad_sample.setStyleSheet(u"QPushButton {\n"
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
"    }\n"
"\n"
"QPushButton:disabled {\n"
"        background-color: #808080;\n"
"    }")

        self.horizontalLayout_3.addWidget(self.pushButton_nomad_sample)


        self.verticalLayout_2.addWidget(self.sample_widget_nomad)


        self.gridLayout_6.addWidget(self.sample_widget, 0, 10, 1, 1)

        self.session_upload_widget = QWidget(self.menu_widget)
        self.session_upload_widget.setObjectName(u"session_upload_widget")
        self.verticalLayout_3 = QVBoxLayout(self.session_upload_widget)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.nomad_upload_widget = QWidget(self.session_upload_widget)
        self.nomad_upload_widget.setObjectName(u"nomad_upload_widget")
        self.horizontalLayout_6 = QHBoxLayout(self.nomad_upload_widget)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 3, 0, 3)
        self.label_nomad_upload = QLabel(self.nomad_upload_widget)
        self.label_nomad_upload.setObjectName(u"label_nomad_upload")
        font3 = QFont()
        font3.setPointSize(10)
        font3.setBold(True)
        self.label_nomad_upload.setFont(font3)

        self.horizontalLayout_6.addWidget(self.label_nomad_upload)

        self.comboBox_upload_type = QComboBox(self.nomad_upload_widget)
        self.comboBox_upload_type.setObjectName(u"comboBox_upload_type")

        self.horizontalLayout_6.addWidget(self.comboBox_upload_type)

        self.comboBox_upload_choice = DynamicUploadComboBox(self.nomad_upload_widget)
        self.comboBox_upload_choice.setObjectName(u"comboBox_upload_choice")

        self.horizontalLayout_6.addWidget(self.comboBox_upload_choice)


        self.verticalLayout_3.addWidget(self.nomad_upload_widget)

        self.session_widget = QWidget(self.session_upload_widget)
        self.session_widget.setObjectName(u"session_widget")
        self.horizontalLayout_5 = QHBoxLayout(self.session_widget)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 3, 0, 3)
        self.label_4 = QLabel(self.session_widget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMaximumSize(QSize(1500000, 16777215))
        self.label_4.setFont(font3)
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.label_4)

        self.lineEdit_session = Variable_Box(self.session_widget)
        self.lineEdit_session.setObjectName(u"lineEdit_session")

        self.horizontalLayout_5.addWidget(self.lineEdit_session)

        self.label_6 = QLabel(self.session_widget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font3)

        self.horizontalLayout_5.addWidget(self.label_6)

        self.lineEdit_tags = QLineEdit(self.session_widget)
        self.lineEdit_tags.setObjectName(u"lineEdit_tags")

        self.horizontalLayout_5.addWidget(self.lineEdit_tags)

        self.scrollArea = QScrollArea(self.session_widget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 71, 24))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.horizontalLayout_5.addWidget(self.scrollArea)


        self.verticalLayout_3.addWidget(self.session_widget)


        self.gridLayout_6.addWidget(self.session_upload_widget, 0, 15, 1, 1)

        self.user_widget = QWidget(self.menu_widget)
        self.user_widget.setObjectName(u"user_widget")
        self.verticalLayout = QVBoxLayout(self.user_widget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.user_widget_default = QWidget(self.user_widget)
        self.user_widget_default.setObjectName(u"user_widget_default")
        self.horizontalLayout = QHBoxLayout(self.user_widget_default)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 3, 0, 3)
        self.comboBox_user = QComboBox(self.user_widget_default)
        self.comboBox_user.setObjectName(u"comboBox_user")
        self.comboBox_user.setFont(font2)

        self.horizontalLayout.addWidget(self.comboBox_user)

        self.pushButton_editUserInfo = QPushButton(self.user_widget_default)
        self.pushButton_editUserInfo.setObjectName(u"pushButton_editUserInfo")
        self.pushButton_editUserInfo.setFont(font1)
        self.pushButton_editUserInfo.setStyleSheet(u"QPushButton {\n"
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
"    }")

        self.horizontalLayout.addWidget(self.pushButton_editUserInfo)


        self.verticalLayout.addWidget(self.user_widget_default)

        self.user_widget_nomad = QWidget(self.user_widget)
        self.user_widget_nomad.setObjectName(u"user_widget_nomad")
        self.horizontalLayout_2 = QHBoxLayout(self.user_widget_nomad)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 3, 0, 3)
        self.label_nomad_user = QLabel(self.user_widget_nomad)
        self.label_nomad_user.setObjectName(u"label_nomad_user")
        self.label_nomad_user.setFont(font2)

        self.horizontalLayout_2.addWidget(self.label_nomad_user)

        self.pushButton_login_nomad = QPushButton(self.user_widget_nomad)
        self.pushButton_login_nomad.setObjectName(u"pushButton_login_nomad")
        self.pushButton_login_nomad.setFont(font1)
        self.pushButton_login_nomad.setStyleSheet(u"QPushButton {\n"
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
"    }")

        self.horizontalLayout_2.addWidget(self.pushButton_login_nomad)


        self.verticalLayout.addWidget(self.user_widget_nomad)


        self.gridLayout_6.addWidget(self.user_widget, 0, 2, 1, 1)

        self.label_8 = QLabel(self.menu_widget)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMaximumSize(QSize(70, 16777215))
        self.label_8.setFont(font3)
        self.label_8.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_8, 0, 9, 1, 1)


        self.gridLayout_5.addWidget(self.menu_widget, 1, 2, 1, 9)

        self.widget_2 = QWidget(self.centralwidget)
        self.widget_2.setObjectName(u"widget_2")
        self.gridLayout_3 = QGridLayout(self.widget_2)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_no_instruments = QLabel(self.widget_2)
        self.label_no_instruments.setObjectName(u"label_no_instruments")

        self.gridLayout_3.addWidget(self.label_no_instruments, 0, 1, 1, 1)

        self.label_arrow = QLabel(self.widget_2)
        self.label_arrow.setObjectName(u"label_arrow")
        self.label_arrow.setMaximumSize(QSize(120, 16777215))
        self.label_arrow.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.label_arrow, 0, 0, 1, 1)

        self.main_splitter = QSplitter(self.widget_2)
        self.main_splitter.setObjectName(u"main_splitter")
        self.main_splitter.setOrientation(Qt.Orientation.Vertical)
        self.manual_widget = QWidget(self.main_splitter)
        self.manual_widget.setObjectName(u"manual_widget")
        self.gridLayout = QGridLayout(self.manual_widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 1, 2, 1, 1)

        self.pushButton_add_manual = QPushButton(self.manual_widget)
        self.pushButton_add_manual.setObjectName(u"pushButton_add_manual")
        sizePolicy1.setHeightForWidth(self.pushButton_add_manual.sizePolicy().hasHeightForWidth())
        self.pushButton_add_manual.setSizePolicy(sizePolicy1)
        self.pushButton_add_manual.setMinimumSize(QSize(32, 32))
        self.pushButton_add_manual.setMaximumSize(QSize(32, 32))
        self.pushButton_add_manual.setFont(font1)
        self.pushButton_add_manual.setStyleSheet(u"QPushButton {\n"
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
"                            }")

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
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_2, 1, 3, 1, 1)

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
        self.pushButton_add_meas.setMinimumSize(QSize(32, 32))
        self.pushButton_add_meas.setMaximumSize(QSize(32, 32))
        self.pushButton_add_meas.setFont(font1)
        self.pushButton_add_meas.setStyleSheet(u"QPushButton {\n"
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
"                            }")

        self.gridLayout_2.addWidget(self.pushButton_add_meas, 1, 1, 1, 1)

        self.pushButton_import_protocol = QPushButton(self.meas_widget)
        self.pushButton_import_protocol.setObjectName(u"pushButton_import_protocol")
        sizePolicy1.setHeightForWidth(self.pushButton_import_protocol.sizePolicy().hasHeightForWidth())
        self.pushButton_import_protocol.setSizePolicy(sizePolicy1)
        self.pushButton_import_protocol.setMinimumSize(QSize(32, 32))
        self.pushButton_import_protocol.setMaximumSize(QSize(60, 32))
        self.pushButton_import_protocol.setStyleSheet(u"QPushButton {\n"
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
"    }")

        self.gridLayout_2.addWidget(self.pushButton_import_protocol, 1, 2, 1, 1)

        self.main_splitter.addWidget(self.meas_widget)

        self.gridLayout_3.addWidget(self.main_splitter, 1, 0, 1, 2)


        self.gridLayout_5.addWidget(self.widget_2, 4, 2, 2, 7)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1322, 33))
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
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuHelp.addAction(self.actionDocumentation)
        self.menuHelp.addAction(self.actionReport_Bug)
        self.menuTools.addAction(self.actionWatchdogs)
        self.menuTools.addSeparator()
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
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionPresets.setText(QCoreApplication.translate("MainWindow", u"Device-Presets", None))
        self.actionOptions.setText(QCoreApplication.translate("MainWindow", u"Options", None))
        self.actionSave_Device_Preset_As.setText(QCoreApplication.translate("MainWindow", u"Save Device Preset As", None))
        self.actionLoad.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.actionMeasurement_Presets.setText(QCoreApplication.translate("MainWindow", u"Measurement-Presets", None))
        self.actionSave_Preset.setText(QCoreApplication.translate("MainWindow", u"Save Preset", None))
#if QT_CONFIG(tooltip)
        self.actionSave_Preset.setToolTip(QCoreApplication.translate("MainWindow", u"Save your current instrument configuration and protocols\n"
"(CAMELS automatically saves on closing the program)", None))
#endif // QT_CONFIG(tooltip)
        self.actionOpen_Backup_Device_Preset.setText(QCoreApplication.translate("MainWindow", u"Load Backup Device Preset", None))
        self.actionLoad_Backup_Preset.setText(QCoreApplication.translate("MainWindow", u"Load Preset", None))
#if QT_CONFIG(tooltip)
        self.actionLoad_Backup_Preset.setToolTip(QCoreApplication.translate("MainWindow", u"Load another preset", None))
#endif // QT_CONFIG(tooltip)
        self.actionAutosave_on_closing.setText(QCoreApplication.translate("MainWindow", u"Autosave on closing", None))
        self.actionUpdate_CAMELS.setText(QCoreApplication.translate("MainWindow", u"Update NOMAD-CAMELS", None))
        self.actionDark_Mode.setText(QCoreApplication.translate("MainWindow", u"Dark Mode", None))
        self.actionUndo.setText(QCoreApplication.translate("MainWindow", u"Undo (ctrl + z)", None))
        self.actionRedo.setText(QCoreApplication.translate("MainWindow", u"Redo (ctrl + y)", None))
        self.actionSettings.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.actionIOC_Builder.setText(QCoreApplication.translate("MainWindow", u"IOC-Builder", None))
        self.actionNew_Device_Preset_2.setText(QCoreApplication.translate("MainWindow", u"New Device Preset", None))
        self.actionSave_Device_Preset.setText(QCoreApplication.translate("MainWindow", u"Save Device Preset", None))
        self.actionSave_Preset_As.setText(QCoreApplication.translate("MainWindow", u"Save Preset As", None))
        self.actionNew_Preset.setText(QCoreApplication.translate("MainWindow", u"New Preset", None))
#if QT_CONFIG(tooltip)
        self.actionNew_Preset.setToolTip(QCoreApplication.translate("MainWindow", u"Create a new Preset, i.e. an empty version of CAMELS with no configured instruments or protocols", None))
#endif // QT_CONFIG(tooltip)
        self.actionNew_Device_Preset.setText(QCoreApplication.translate("MainWindow", u"New Device Preset", None))
        self.actionDocumentation.setText(QCoreApplication.translate("MainWindow", u"Documentation", None))
        self.actionReport_Bug.setText(QCoreApplication.translate("MainWindow", u"Report Bug", None))
        self.action_driver_builder.setText(QCoreApplication.translate("MainWindow", u"Driver builder", None))
        self.actionEPICS_driver_builder.setText(QCoreApplication.translate("MainWindow", u"EPICS-driver-builder", None))
        self.actionExport_from_databroker.setText(QCoreApplication.translate("MainWindow", u"Export from databroker", None))
        self.actionManage_Extensions.setText(QCoreApplication.translate("MainWindow", u"Manage Extensions", None))
        self.actionExport_CAMELS_hdf5_to_csv_json.setText(QCoreApplication.translate("MainWindow", u"Export CAMELS hdf5 to csv/json", None))
        self.actionQuit.setText(QCoreApplication.translate("MainWindow", u"Quit", None))
        self.actionWatchdogs.setText(QCoreApplication.translate("MainWindow", u"Watchdogs", None))
#if QT_CONFIG(tooltip)
        self.pushButton_resume.setToolTip(QCoreApplication.translate("MainWindow", u"resume the paused protocol", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_resume.setText(QCoreApplication.translate("MainWindow", u"Resume", None))
#if QT_CONFIG(tooltip)
        self.textEdit_console_output.setToolTip(QCoreApplication.translate("MainWindow", u"These are messages from the running CAMELS, mostly useful for debugging", None))
#endif // QT_CONFIG(tooltip)
        self.textEdit_console_output.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Log is currently empty.", None))
#if QT_CONFIG(tooltip)
        self.pushButton_close_plots.setToolTip(QCoreApplication.translate("MainWindow", u"close all open plots\n"
"plots from a running protocol reopen with new data", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_close_plots.setText(QCoreApplication.translate("MainWindow", u"Close Plots", None))
#if QT_CONFIG(tooltip)
        self.pushButton_stop.setToolTip(QCoreApplication.translate("MainWindow", u"abort the running protocol", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_stop.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
#if QT_CONFIG(tooltip)
        self.pushButton_clear_log.setToolTip(QCoreApplication.translate("MainWindow", u"clear the log window", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_clear_log.setText(QCoreApplication.translate("MainWindow", u"Clear Log", None))
#if QT_CONFIG(tooltip)
        self.pushButton_pause.setToolTip(QCoreApplication.translate("MainWindow", u"pause the running protocol", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_pause.setText(QCoreApplication.translate("MainWindow", u"Pause", None))
#if QT_CONFIG(tooltip)
        self.pushButton_show_log.setToolTip(QCoreApplication.translate("MainWindow", u"open / close the log with advanced system messages", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_show_log.setText(QCoreApplication.translate("MainWindow", u"Show Log", None))
        self.textEdit_meas_description.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Add a measurmeent description here.", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Measurement Description", None))
#if QT_CONFIG(tooltip)
        self.run_queue_widget.setToolTip(QCoreApplication.translate("MainWindow", u"Add a new protocol to the queue or customize queued protocols, e.g. modify variables ", None))
#endif // QT_CONFIG(tooltip)
        self.label_queue.setText(QCoreApplication.translate("MainWindow", u"Queue", None))
#if QT_CONFIG(tooltip)
        self.progressBar_protocols.setToolTip(QCoreApplication.translate("MainWindow", u"Calculated from the number of steps in the protocol.\n"
"Protocols with While Loops or If statements may have bad calculations!", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.label_remaining_time.setToolTip(QCoreApplication.translate("MainWindow", u"elapsed time of the protocol run /\n"
"estimated time to finish", None))
#endif // QT_CONFIG(tooltip)
        self.label_remaining_time.setText(QCoreApplication.translate("MainWindow", u"00:00 / 00:00", None))
        self.label_logo.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_manage_instr.setToolTip(QCoreApplication.translate("MainWindow", u"Configure your instruments or install new drivers", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_manage_instr.setText(QCoreApplication.translate("MainWindow", u"Manage\n"
"Instruments", None))
#if QT_CONFIG(tooltip)
        self.comboBox_sample.setToolTip(QCoreApplication.translate("MainWindow", u"Select the sample you are currently measuring.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.pushButton_editSampleInfo.setToolTip(QCoreApplication.translate("MainWindow", u"Add or modify samples. ", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_editSampleInfo.setText(QCoreApplication.translate("MainWindow", u"Edit Sample-Information", None))
#if QT_CONFIG(tooltip)
        self.checkBox_use_nomad_sample.setToolTip(QCoreApplication.translate("MainWindow", u"only when this box is checked, the sample from NOMAD is used for the data", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_use_nomad_sample.setText(QCoreApplication.translate("MainWindow", u"use NOMAD sample", None))
#if QT_CONFIG(tooltip)
        self.pushButton_nomad_sample.setToolTip(QCoreApplication.translate("MainWindow", u"Choose a sample from your NOMAD entries", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_nomad_sample.setText(QCoreApplication.translate("MainWindow", u"select NOMAD sample", None))
        self.label_nomad_upload.setText(QCoreApplication.translate("MainWindow", u"NOMAD Upload:", None))
#if QT_CONFIG(tooltip)
        self.label_4.setToolTip(QCoreApplication.translate("MainWindow", u"- Optional -\n"
"Adds a sub-folder for the saved data with the name of the session\n"
"Used to distinguish different measurements", None))
#endif // QT_CONFIG(tooltip)
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Session:", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_session.setToolTip(QCoreApplication.translate("MainWindow", u"- Optional -\n"
"Adds a sub-folder for the saved data with the name of the session\n"
"Used to distinguish different measurements", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_session.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Add optional Session name", None))
#if QT_CONFIG(tooltip)
        self.label_6.setToolTip(QCoreApplication.translate("MainWindow", u"Press Enter to add Tags. Remove Tags by pressing the red x on the tag.", None))
#endif // QT_CONFIG(tooltip)
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Tags", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_tags.setToolTip(QCoreApplication.translate("MainWindow", u"Press Enter to add Tags. Remove Tags by pressing the black x on the tag. \n"
"Useful to identify / filter measurements", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_tags.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Press Enter to add Tag", None))
#if QT_CONFIG(tooltip)
        self.scrollArea.setToolTip(QCoreApplication.translate("MainWindow", u"Currently used Tags. Remove by pressing the black x", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.comboBox_user.setToolTip(QCoreApplication.translate("MainWindow", u"Select the user that is currently measuring.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.pushButton_editUserInfo.setToolTip(QCoreApplication.translate("MainWindow", u"Add or modify users. ", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_editUserInfo.setText(QCoreApplication.translate("MainWindow", u"Edit User-Information", None))
        self.label_nomad_user.setText(QCoreApplication.translate("MainWindow", u"not logged in", None))
#if QT_CONFIG(tooltip)
        self.pushButton_login_nomad.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.pushButton_login_nomad.setText(QCoreApplication.translate("MainWindow", u"NOMAD login", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Sample:", None))
        self.label_no_instruments.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">You are currently using no instruments.</span></p><p><span style=\" font-size:12pt; font-weight:600;\">Click &quot;Manage Instruments&quot; to configure your</span></p><p><span style=\" font-size:12pt; font-weight:600;\">first instrument and start with NOMAD CAMELS!</span></p></body></html>", None))
        self.label_arrow.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_add_manual.setToolTip(QCoreApplication.translate("MainWindow", u"add a new manual control", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_add_manual.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Manual Control", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Measurement Protocols", None))
#if QT_CONFIG(tooltip)
        self.pushButton_add_meas.setToolTip(QCoreApplication.translate("MainWindow", u"create a new protocol", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_add_meas.setText(QCoreApplication.translate("MainWindow", u"+", None))
#if QT_CONFIG(tooltip)
        self.pushButton_import_protocol.setToolTip(QCoreApplication.translate("MainWindow", u"Import a previously run / exported protocol", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_import_protocol.setText(QCoreApplication.translate("MainWindow", u"import", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.menuTools.setTitle(QCoreApplication.translate("MainWindow", u"Tools", None))
    # retranslateUi

