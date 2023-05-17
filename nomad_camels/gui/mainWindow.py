# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainWindow.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QGridLayout, QHeaderView, QLabel, QLineEdit,
    QListView, QMainWindow, QMenu, QMenuBar,
    QProgressBar, QPushButton, QSizePolicy, QSpacerItem,
    QSplitter, QStatusBar, QTextEdit, QToolButton,
    QTreeView, QVBoxLayout, QWidget)

from nomad_camels.ui_widgets.console_redirect import Console_TextEdit

class Ui_MainWindow(object):
    """ """
    def setupUi(self, MainWindow):
        """

        Parameters
        ----------
        MainWindow :
            

        Returns
        -------

        """
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(994, 819)
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
        self.pushButton_editUserInfo = QPushButton(self.centralwidget)
        self.pushButton_editUserInfo.setObjectName(u"pushButton_editUserInfo")

        self.gridLayout_5.addWidget(self.pushButton_editUserInfo, 0, 8, 1, 1)

        self.label_8 = QLabel(self.centralwidget)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMaximumSize(QSize(50, 16777215))
        self.label_8.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_8, 0, 10, 1, 1)

        self.pushButton_editSampleInfo = QPushButton(self.centralwidget)
        self.pushButton_editSampleInfo.setObjectName(u"pushButton_editSampleInfo")

        self.gridLayout_5.addWidget(self.pushButton_editSampleInfo, 0, 12, 1, 1)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.gridLayout_5.addWidget(self.line, 0, 9, 1, 1)

        self.comboBox_sample = QComboBox(self.centralwidget)
        self.comboBox_sample.setObjectName(u"comboBox_sample")

        self.gridLayout_5.addWidget(self.comboBox_sample, 0, 11, 1, 1)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMaximumSize(QSize(80, 16777215))
        self.label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_5.addWidget(self.label, 0, 6, 1, 1)

        self.line_2 = QFrame(self.centralwidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.gridLayout_5.addWidget(self.line_2, 0, 5, 1, 1)

        self.comboBox_user = QComboBox(self.centralwidget)
        self.comboBox_user.setObjectName(u"comboBox_user")

        self.gridLayout_5.addWidget(self.comboBox_user, 0, 7, 1, 1)

        self.comboBox_preset = QComboBox(self.centralwidget)
        self.comboBox_preset.setObjectName(u"comboBox_preset")

        self.gridLayout_5.addWidget(self.comboBox_preset, 0, 4, 1, 1)

        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMaximumSize(QSize(50, 16777215))
        self.label_7.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_7, 0, 3, 1, 1)

        self.add_on_widget = QWidget(self.centralwidget)
        self.add_on_widget.setObjectName(u"add_on_widget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.add_on_widget.sizePolicy().hasHeightForWidth())
        self.add_on_widget.setSizePolicy(sizePolicy1)
        self.add_on_widget.setMaximumSize(QSize(100, 16777215))
        self.gridLayout_16 = QGridLayout(self.add_on_widget)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.gridLayout_16.setContentsMargins(0, 0, 0, 0)
        self.add_on_buttons = QWidget(self.add_on_widget)
        self.add_on_buttons.setObjectName(u"add_on_buttons")
        sizePolicy1.setHeightForWidth(self.add_on_buttons.sizePolicy().hasHeightForWidth())
        self.add_on_buttons.setSizePolicy(sizePolicy1)
        self.add_on_buttons.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout = QVBoxLayout(self.add_on_buttons)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.gridLayout_16.addWidget(self.add_on_buttons, 1, 0, 1, 1)

        self.label_9 = QLabel(self.add_on_widget)
        self.label_9.setObjectName(u"label_9")
        sizePolicy1.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy1)
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.label_9.setFont(font)
        self.label_9.setWordWrap(False)

        self.gridLayout_16.addWidget(self.label_9, 0, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_16.addItem(self.verticalSpacer, 2, 0, 1, 1)

        self.line_3 = QFrame(self.add_on_widget)
        self.line_3.setObjectName(u"line_3")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.line_3.sizePolicy().hasHeightForWidth())
        self.line_3.setSizePolicy(sizePolicy2)
        self.line_3.setMaximumSize(QSize(5, 16777215))
        self.line_3.setFrameShape(QFrame.VLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.gridLayout_16.addWidget(self.line_3, 0, 1, 3, 1)


        self.gridLayout_5.addWidget(self.add_on_widget, 0, 1, 3, 1)

        self.dev_meas_splitter = QSplitter(self.centralwidget)
        self.dev_meas_splitter.setObjectName(u"dev_meas_splitter")
        self.dev_meas_splitter.setOrientation(Qt.Horizontal)
        self.devices_main_widget = QWidget(self.dev_meas_splitter)
        self.devices_main_widget.setObjectName(u"devices_main_widget")
        self.gridLayout = QGridLayout(self.devices_main_widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(6)
        self.gridLayout.setContentsMargins(9, 0, 9, 9)
        self.label_6 = QLabel(self.devices_main_widget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMaximumSize(QSize(16777215, 19))
        font1 = QFont()
        font1.setPointSize(12)
        font1.setBold(True)
        self.label_6.setFont(font1)

        self.gridLayout.addWidget(self.label_6, 1, 0, 1, 2)

        self.devices_widget = QWidget(self.devices_main_widget)
        self.devices_widget.setObjectName(u"devices_widget")
        sizePolicy.setHeightForWidth(self.devices_widget.sizePolicy().hasHeightForWidth())
        self.devices_widget.setSizePolicy(sizePolicy)
        self.devices_widget.setMinimumSize(QSize(0, 300))
        self.gridLayout_12 = QGridLayout(self.devices_widget)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setContentsMargins(0, 0, 0, 0)
        self.devices_splitter = QSplitter(self.devices_widget)
        self.devices_splitter.setObjectName(u"devices_splitter")
        self.devices_splitter.setFrameShape(QFrame.NoFrame)
        self.devices_splitter.setLineWidth(8)
        self.devices_splitter.setMidLineWidth(8)
        self.devices_splitter.setOrientation(Qt.Vertical)
        self.devices_splitter.setOpaqueResize(True)
        self.devices_splitter.setHandleWidth(5)
        self.device_list_widget = QWidget(self.devices_splitter)
        self.device_list_widget.setObjectName(u"device_list_widget")
        self.device_list_widget.setMinimumSize(QSize(0, 200))
        self.gridLayout_11 = QGridLayout(self.device_list_widget)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setContentsMargins(0, 0, 0, 0)
        self.pushButton_add_device = QPushButton(self.device_list_widget)
        self.pushButton_add_device.setObjectName(u"pushButton_add_device")
        self.pushButton_add_device.setMinimumSize(QSize(30, 23))
        self.pushButton_add_device.setMaximumSize(QSize(30, 16777215))

        self.gridLayout_11.addWidget(self.pushButton_add_device, 0, 1, 1, 1)

        self.lineEdit_device_search = QLineEdit(self.device_list_widget)
        self.lineEdit_device_search.setObjectName(u"lineEdit_device_search")

        self.gridLayout_11.addWidget(self.lineEdit_device_search, 0, 0, 1, 1)

        self.pushButton_remove_device = QPushButton(self.device_list_widget)
        self.pushButton_remove_device.setObjectName(u"pushButton_remove_device")
        self.pushButton_remove_device.setMinimumSize(QSize(30, 23))
        self.pushButton_remove_device.setMaximumSize(QSize(30, 16777215))

        self.gridLayout_11.addWidget(self.pushButton_remove_device, 0, 2, 1, 1)

        self.treeView_devices = QTreeView(self.device_list_widget)
        self.treeView_devices.setObjectName(u"treeView_devices")

        self.gridLayout_11.addWidget(self.treeView_devices, 3, 0, 2, 3)

        self.devices_splitter.addWidget(self.device_list_widget)
        self.device_epics_widget = QWidget(self.devices_splitter)
        self.device_epics_widget.setObjectName(u"device_epics_widget")
        sizePolicy1.setHeightForWidth(self.device_epics_widget.sizePolicy().hasHeightForWidth())
        self.device_epics_widget.setSizePolicy(sizePolicy1)
        self.device_epics_widget.setMinimumSize(QSize(0, 0))
        self.device_epics_widget.setMaximumSize(QSize(16777215, 16777215))
        self.gridLayout_2 = QGridLayout(self.device_epics_widget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.pushButton_make_EPICS_environment = QPushButton(self.device_epics_widget)
        self.pushButton_make_EPICS_environment.setObjectName(u"pushButton_make_EPICS_environment")

        self.gridLayout_2.addWidget(self.pushButton_make_EPICS_environment, 0, 0, 1, 1)

        self.textEdit_console_output = QTextEdit(self.device_epics_widget)
        self.textEdit_console_output.setObjectName(u"textEdit_console_output")
        self.textEdit_console_output.setTextInteractionFlags(Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)

        self.gridLayout_2.addWidget(self.textEdit_console_output, 5, 0, 1, 3)

        self.pushButton_run_ioc = QPushButton(self.device_epics_widget)
        self.pushButton_run_ioc.setObjectName(u"pushButton_run_ioc")

        self.gridLayout_2.addWidget(self.pushButton_run_ioc, 1, 0, 1, 1)

        self.progressBar_devices = QProgressBar(self.device_epics_widget)
        self.progressBar_devices.setObjectName(u"progressBar_devices")
        self.progressBar_devices.setEnabled(True)
        self.progressBar_devices.setValue(0)

        self.gridLayout_2.addWidget(self.progressBar_devices, 0, 1, 1, 1)

        self.checkBox_ioc_running = QCheckBox(self.device_epics_widget)
        self.checkBox_ioc_running.setObjectName(u"checkBox_ioc_running")
        self.checkBox_ioc_running.setEnabled(False)
        self.checkBox_ioc_running.setCheckable(True)

        self.gridLayout_2.addWidget(self.checkBox_ioc_running, 1, 1, 1, 1)

        self.lineEdit_send_to_IOC = QLineEdit(self.device_epics_widget)
        self.lineEdit_send_to_IOC.setObjectName(u"lineEdit_send_to_IOC")
        self.lineEdit_send_to_IOC.setEnabled(False)

        self.gridLayout_2.addWidget(self.lineEdit_send_to_IOC, 3, 0, 1, 1)

        self.pushButton_write_to_console = QPushButton(self.device_epics_widget)
        self.pushButton_write_to_console.setObjectName(u"pushButton_write_to_console")
        self.pushButton_write_to_console.setEnabled(False)

        self.gridLayout_2.addWidget(self.pushButton_write_to_console, 3, 1, 1, 1)

        self.pushButton_show_console_output = QPushButton(self.device_epics_widget)
        self.pushButton_show_console_output.setObjectName(u"pushButton_show_console_output")

        self.gridLayout_2.addWidget(self.pushButton_show_console_output, 2, 0, 1, 1)

        self.pushButton_clear_EPICS_output = QPushButton(self.device_epics_widget)
        self.pushButton_clear_EPICS_output.setObjectName(u"pushButton_clear_EPICS_output")

        self.gridLayout_2.addWidget(self.pushButton_clear_EPICS_output, 2, 1, 1, 1)

        self.devices_splitter.addWidget(self.device_epics_widget)
        self.device_config_widget = QWidget(self.devices_splitter)
        self.device_config_widget.setObjectName(u"device_config_widget")
        self.gridLayout_7 = QGridLayout(self.device_config_widget)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.devices_splitter.addWidget(self.device_config_widget)

        self.gridLayout_12.addWidget(self.devices_splitter, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.devices_widget, 2, 0, 1, 2)

        self.dev_meas_splitter.addWidget(self.devices_main_widget)
        self.meas_main_widget = QWidget(self.dev_meas_splitter)
        self.meas_main_widget.setObjectName(u"meas_main_widget")
        self.gridLayout_4 = QGridLayout(self.meas_main_widget)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(-1, -1, 0, -1)
        self.meas_widget = QWidget(self.meas_main_widget)
        self.meas_widget.setObjectName(u"meas_widget")
        self.gridLayout_3 = QGridLayout(self.meas_widget)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.meas_splitter = QSplitter(self.meas_widget)
        self.meas_splitter.setObjectName(u"meas_splitter")
        self.meas_splitter.setFrameShape(QFrame.NoFrame)
        self.meas_splitter.setLineWidth(10)
        self.meas_splitter.setMidLineWidth(10)
        self.meas_splitter.setOrientation(Qt.Horizontal)
        self.protocols_main_widget = QWidget(self.meas_splitter)
        self.protocols_main_widget.setObjectName(u"protocols_main_widget")
        self.gridLayout_6 = QGridLayout(self.protocols_main_widget)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(9, 0, 9, 0)
        self.pushButton_run_protocol = QPushButton(self.protocols_main_widget)
        self.pushButton_run_protocol.setObjectName(u"pushButton_run_protocol")

        self.gridLayout_6.addWidget(self.pushButton_run_protocol, 1, 0, 1, 1)

        self.label_protocols = QLabel(self.protocols_main_widget)
        self.label_protocols.setObjectName(u"label_protocols")
        self.label_protocols.setFont(font1)

        self.gridLayout_6.addWidget(self.label_protocols, 0, 0, 1, 1)

        self.pushButton_pause_protocol = QPushButton(self.protocols_main_widget)
        self.pushButton_pause_protocol.setObjectName(u"pushButton_pause_protocol")
        self.pushButton_pause_protocol.setEnabled(False)

        self.gridLayout_6.addWidget(self.pushButton_pause_protocol, 1, 1, 1, 1)

        self.pushButton_stop_protocol = QPushButton(self.protocols_main_widget)
        self.pushButton_stop_protocol.setObjectName(u"pushButton_stop_protocol")
        self.pushButton_stop_protocol.setEnabled(False)

        self.gridLayout_6.addWidget(self.pushButton_stop_protocol, 1, 2, 1, 1)

        self.protocols_widget = QWidget(self.protocols_main_widget)
        self.protocols_widget.setObjectName(u"protocols_widget")
        self.gridLayout_15 = QGridLayout(self.protocols_widget)
        self.gridLayout_15.setSpacing(0)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.gridLayout_15.setContentsMargins(0, 0, 0, 0)
        self.protocols_splitter = QSplitter(self.protocols_widget)
        self.protocols_splitter.setObjectName(u"protocols_splitter")
        self.protocols_splitter.setOrientation(Qt.Vertical)
        self.protocols_list_widget = QWidget(self.protocols_splitter)
        self.protocols_list_widget.setObjectName(u"protocols_list_widget")
        self.gridLayout_13 = QGridLayout(self.protocols_list_widget)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_13.setContentsMargins(0, 0, 0, 0)
        self.pushButton_add_protocol = QPushButton(self.protocols_list_widget)
        self.pushButton_add_protocol.setObjectName(u"pushButton_add_protocol")
        self.pushButton_add_protocol.setMinimumSize(QSize(30, 23))
        self.pushButton_add_protocol.setMaximumSize(QSize(30, 16777215))

        self.gridLayout_13.addWidget(self.pushButton_add_protocol, 0, 1, 1, 1)

        self.pushButton_remove_protocol = QPushButton(self.protocols_list_widget)
        self.pushButton_remove_protocol.setObjectName(u"pushButton_remove_protocol")
        self.pushButton_remove_protocol.setMinimumSize(QSize(30, 23))
        self.pushButton_remove_protocol.setMaximumSize(QSize(30, 16777215))

        self.gridLayout_13.addWidget(self.pushButton_remove_protocol, 0, 2, 1, 1)

        self.lineEdit_protocol_search = QLineEdit(self.protocols_list_widget)
        self.lineEdit_protocol_search.setObjectName(u"lineEdit_protocol_search")

        self.gridLayout_13.addWidget(self.lineEdit_protocol_search, 0, 0, 1, 1)

        self.listView_protocols = QListView(self.protocols_list_widget)
        self.listView_protocols.setObjectName(u"listView_protocols")

        self.gridLayout_13.addWidget(self.listView_protocols, 1, 0, 1, 3)

        self.protocols_splitter.addWidget(self.protocols_list_widget)
        self.protocols_build_widget = QWidget(self.protocols_splitter)
        self.protocols_build_widget.setObjectName(u"protocols_build_widget")
        self.gridLayout_14 = QGridLayout(self.protocols_build_widget)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.gridLayout_14.setContentsMargins(0, 0, 0, 0)
        self.pushButton_build_protocol = QPushButton(self.protocols_build_widget)
        self.pushButton_build_protocol.setObjectName(u"pushButton_build_protocol")

        self.gridLayout_14.addWidget(self.pushButton_build_protocol, 0, 0, 1, 1)

        self.pushButton_open_protocol_external = QPushButton(self.protocols_build_widget)
        self.pushButton_open_protocol_external.setObjectName(u"pushButton_open_protocol_external")

        self.gridLayout_14.addWidget(self.pushButton_open_protocol_external, 0, 1, 1, 1)

        self.pushButton_clear_output_meas = QPushButton(self.protocols_build_widget)
        self.pushButton_clear_output_meas.setObjectName(u"pushButton_clear_output_meas")

        self.gridLayout_14.addWidget(self.pushButton_clear_output_meas, 2, 1, 1, 1)

        self.progressBar_protocols = QProgressBar(self.protocols_build_widget)
        self.progressBar_protocols.setObjectName(u"progressBar_protocols")
        self.progressBar_protocols.setValue(0)

        self.gridLayout_14.addWidget(self.progressBar_protocols, 1, 0, 1, 2)

        self.textEdit_console_output_meas = Console_TextEdit(self.protocols_build_widget)
        self.textEdit_console_output_meas.setObjectName(u"textEdit_console_output_meas")
        self.textEdit_console_output_meas.setTextInteractionFlags(Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)

        self.gridLayout_14.addWidget(self.textEdit_console_output_meas, 4, 0, 1, 2)

        self.pushButton_show_output_meas = QPushButton(self.protocols_build_widget)
        self.pushButton_show_output_meas.setObjectName(u"pushButton_show_output_meas")

        self.gridLayout_14.addWidget(self.pushButton_show_output_meas, 2, 0, 1, 1)

        self.lineEdit_write_to_ipython = QLineEdit(self.protocols_build_widget)
        self.lineEdit_write_to_ipython.setObjectName(u"lineEdit_write_to_ipython")

        self.gridLayout_14.addWidget(self.lineEdit_write_to_ipython, 3, 0, 1, 1)

        self.pushButton_write_to_ipython = QPushButton(self.protocols_build_widget)
        self.pushButton_write_to_ipython.setObjectName(u"pushButton_write_to_ipython")

        self.gridLayout_14.addWidget(self.pushButton_write_to_ipython, 3, 1, 1, 1)

        self.protocols_splitter.addWidget(self.protocols_build_widget)

        self.gridLayout_15.addWidget(self.protocols_splitter, 0, 0, 1, 1)


        self.gridLayout_6.addWidget(self.protocols_widget, 3, 0, 1, 3)

        self.meas_splitter.addWidget(self.protocols_main_widget)
        self.sequence_main_widget = QWidget(self.meas_splitter)
        self.sequence_main_widget.setObjectName(u"sequence_main_widget")
        self.gridLayout_8 = QGridLayout(self.sequence_main_widget)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(-1, 0, -1, 0)
        self.pushButton_move_step_out = QPushButton(self.sequence_main_widget)
        self.pushButton_move_step_out.setObjectName(u"pushButton_move_step_out")

        self.gridLayout_8.addWidget(self.pushButton_move_step_out, 4, 1, 1, 1)

        self.pushButton_move_step_in = QPushButton(self.sequence_main_widget)
        self.pushButton_move_step_in.setObjectName(u"pushButton_move_step_in")

        self.gridLayout_8.addWidget(self.pushButton_move_step_in, 3, 1, 1, 1)

        self.pushButton_move_step_up = QPushButton(self.sequence_main_widget)
        self.pushButton_move_step_up.setObjectName(u"pushButton_move_step_up")

        self.gridLayout_8.addWidget(self.pushButton_move_step_up, 3, 0, 1, 1)

        self.pushButton_move_step_down = QPushButton(self.sequence_main_widget)
        self.pushButton_move_step_down.setObjectName(u"pushButton_move_step_down")

        self.gridLayout_8.addWidget(self.pushButton_move_step_down, 4, 0, 1, 1)

        self.label_sequence = QLabel(self.sequence_main_widget)
        self.label_sequence.setObjectName(u"label_sequence")
        self.label_sequence.setMaximumSize(QSize(16777215, 19))
        self.label_sequence.setFont(font1)

        self.gridLayout_8.addWidget(self.label_sequence, 0, 0, 1, 1)

        self.treeView_protocol_sequence = QTreeView(self.sequence_main_widget)
        self.treeView_protocol_sequence.setObjectName(u"treeView_protocol_sequence")

        self.gridLayout_8.addWidget(self.treeView_protocol_sequence, 6, 0, 1, 3)

        self.pushButton_show_protocol_settings = QPushButton(self.sequence_main_widget)
        self.pushButton_show_protocol_settings.setObjectName(u"pushButton_show_protocol_settings")

        self.gridLayout_8.addWidget(self.pushButton_show_protocol_settings, 1, 0, 1, 3)

        self.toolButton_add_step = QToolButton(self.sequence_main_widget)
        self.toolButton_add_step.setObjectName(u"toolButton_add_step")
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.toolButton_add_step.sizePolicy().hasHeightForWidth())
        self.toolButton_add_step.setSizePolicy(sizePolicy3)
        self.toolButton_add_step.setMinimumSize(QSize(30, 23))
        self.toolButton_add_step.setMaximumSize(QSize(30, 16777215))

        self.gridLayout_8.addWidget(self.toolButton_add_step, 3, 2, 1, 1)

        self.pushButton_remove_step = QPushButton(self.sequence_main_widget)
        self.pushButton_remove_step.setObjectName(u"pushButton_remove_step")
        self.pushButton_remove_step.setMinimumSize(QSize(30, 23))
        self.pushButton_remove_step.setMaximumSize(QSize(30, 16777215))

        self.gridLayout_8.addWidget(self.pushButton_remove_step, 4, 2, 1, 1)

        self.meas_splitter.addWidget(self.sequence_main_widget)
        self.configuration_main_widget = QWidget(self.meas_splitter)
        self.configuration_main_widget.setObjectName(u"configuration_main_widget")
        self.gridLayout_9 = QGridLayout(self.configuration_main_widget)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(-1, 0, 0, 0)
        self.label_configuration = QLabel(self.configuration_main_widget)
        self.label_configuration.setObjectName(u"label_configuration")
        self.label_configuration.setMaximumSize(QSize(16777215, 19))
        self.label_configuration.setFont(font1)

        self.gridLayout_9.addWidget(self.label_configuration, 0, 0, 1, 1)

        self.loopstep_configuration_widget = QWidget(self.configuration_main_widget)
        self.loopstep_configuration_widget.setObjectName(u"loopstep_configuration_widget")
        self.gridLayout_10 = QGridLayout(self.loopstep_configuration_widget)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setContentsMargins(0, 0, 0, 0)

        self.gridLayout_9.addWidget(self.loopstep_configuration_widget, 1, 0, 1, 1)

        self.meas_splitter.addWidget(self.configuration_main_widget)

        self.gridLayout_3.addWidget(self.meas_splitter, 0, 0, 1, 1)


        self.gridLayout_4.addWidget(self.meas_widget, 0, 0, 1, 2)

        self.dev_meas_splitter.addWidget(self.meas_main_widget)

        self.gridLayout_5.addWidget(self.dev_meas_splitter, 1, 3, 2, 10)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 994, 21))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuPreferences = QMenu(self.menubar)
        self.menuPreferences.setObjectName(u"menuPreferences")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        self.menuTools = QMenu(self.menubar)
        self.menuTools.setObjectName(u"menuTools")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        QWidget.setTabOrder(self.lineEdit_device_search, self.pushButton_add_device)
        QWidget.setTabOrder(self.pushButton_add_device, self.pushButton_remove_device)
        QWidget.setTabOrder(self.pushButton_remove_device, self.treeView_devices)
        QWidget.setTabOrder(self.treeView_devices, self.pushButton_make_EPICS_environment)
        QWidget.setTabOrder(self.pushButton_make_EPICS_environment, self.textEdit_console_output)
        QWidget.setTabOrder(self.textEdit_console_output, self.pushButton_run_protocol)
        QWidget.setTabOrder(self.pushButton_run_protocol, self.lineEdit_protocol_search)
        QWidget.setTabOrder(self.lineEdit_protocol_search, self.pushButton_add_protocol)
        QWidget.setTabOrder(self.pushButton_add_protocol, self.pushButton_remove_protocol)
        QWidget.setTabOrder(self.pushButton_remove_protocol, self.listView_protocols)
        QWidget.setTabOrder(self.listView_protocols, self.pushButton_build_protocol)
        QWidget.setTabOrder(self.pushButton_build_protocol, self.textEdit_console_output_meas)
        QWidget.setTabOrder(self.textEdit_console_output_meas, self.pushButton_show_protocol_settings)
        QWidget.setTabOrder(self.pushButton_show_protocol_settings, self.pushButton_move_step_up)
        QWidget.setTabOrder(self.pushButton_move_step_up, self.pushButton_move_step_in)
        QWidget.setTabOrder(self.pushButton_move_step_in, self.pushButton_move_step_down)
        QWidget.setTabOrder(self.pushButton_move_step_down, self.pushButton_move_step_out)
        QWidget.setTabOrder(self.pushButton_move_step_out, self.toolButton_add_step)
        QWidget.setTabOrder(self.toolButton_add_step, self.pushButton_remove_step)
        QWidget.setTabOrder(self.pushButton_remove_step, self.treeView_protocol_sequence)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuPreferences.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionNew_Preset)
        self.menuFile.addAction(self.actionSave_Preset)
        self.menuFile.addAction(self.actionSave_Preset_As)
        self.menuFile.addAction(self.actionLoad_Backup_Preset)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSettings)
        self.menuPreferences.addAction(self.actionUndo)
        self.menuPreferences.addAction(self.actionRedo)
        self.menuPreferences.addSeparator()
        self.menuHelp.addAction(self.actionDocumentation)
        self.menuHelp.addAction(self.actionReport_Bug)
        self.menuTools.addAction(self.actionDevice_Driver_Builder)
        self.menuTools.addAction(self.actionVISA_device_builder)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        """

        Parameters
        ----------
        MainWindow :
            

        Returns
        -------

        """
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionPresets.setText(QCoreApplication.translate("MainWindow", u"Device-Presets", None))
        self.actionOptions.setText(QCoreApplication.translate("MainWindow", u"Options", None))
        self.actionSave_Device_Preset_As.setText(QCoreApplication.translate("MainWindow", u"Save Device Preset As", None))
        self.actionLoad.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.actionMeasurement_Presets.setText(QCoreApplication.translate("MainWindow", u"Measurement-Presets", None))
        self.actionSave_Preset.setText(QCoreApplication.translate("MainWindow", u"Save Preset", None))
        self.actionOpen_Backup_Device_Preset.setText(QCoreApplication.translate("MainWindow", u"Load Backup Device Preset", None))
        self.actionLoad_Backup_Preset.setText(QCoreApplication.translate("MainWindow", u"Load Backup Preset", None))
        self.actionAutosave_on_closing.setText(QCoreApplication.translate("MainWindow", u"Autosave on closing", None))
        self.actionDevice_Driver_Builder.setText(QCoreApplication.translate("MainWindow", u"Update NOMAD-CAMELS", None))
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
        self.pushButton_editUserInfo.setText(QCoreApplication.translate("MainWindow", u"Edit User-Information", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Sample:", None))
        self.pushButton_editSampleInfo.setText(QCoreApplication.translate("MainWindow", u"Edit Sample-Information", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"User:", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Preset:", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Add-Ons", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Devices", None))
        self.pushButton_add_device.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.lineEdit_device_search.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Search", None))
        self.pushButton_remove_device.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.pushButton_make_EPICS_environment.setText(QCoreApplication.translate("MainWindow", u"Make EPICS IOC", None))
        self.pushButton_run_ioc.setText(QCoreApplication.translate("MainWindow", u"Run IOC", None))
        self.checkBox_ioc_running.setText(QCoreApplication.translate("MainWindow", u"not running", None))
        self.pushButton_write_to_console.setText(QCoreApplication.translate("MainWindow", u"Write to console", None))
        self.pushButton_show_console_output.setText(QCoreApplication.translate("MainWindow", u"Hide output", None))
        self.pushButton_clear_EPICS_output.setText(QCoreApplication.translate("MainWindow", u"Clear output", None))
        self.pushButton_run_protocol.setText(QCoreApplication.translate("MainWindow", u"Run", None))
        self.label_protocols.setText(QCoreApplication.translate("MainWindow", u"Protocols", None))
        self.pushButton_pause_protocol.setText(QCoreApplication.translate("MainWindow", u"Pause", None))
        self.pushButton_stop_protocol.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.pushButton_add_protocol.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.pushButton_remove_protocol.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.lineEdit_protocol_search.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Search", None))
        self.pushButton_build_protocol.setText(QCoreApplication.translate("MainWindow", u"Build Protocol", None))
        self.pushButton_open_protocol_external.setText(QCoreApplication.translate("MainWindow", u"Open Protocol externally", None))
        self.pushButton_clear_output_meas.setText(QCoreApplication.translate("MainWindow", u"Clear output", None))
        self.pushButton_show_output_meas.setText(QCoreApplication.translate("MainWindow", u"Hide output", None))
        self.pushButton_write_to_ipython.setText(QCoreApplication.translate("MainWindow", u"Write to console", None))
        self.pushButton_move_step_out.setText(QCoreApplication.translate("MainWindow", u"move out", None))
        self.pushButton_move_step_in.setText(QCoreApplication.translate("MainWindow", u"move in", None))
        self.pushButton_move_step_up.setText(QCoreApplication.translate("MainWindow", u"move up", None))
        self.pushButton_move_step_down.setText(QCoreApplication.translate("MainWindow", u"move down", None))
        self.label_sequence.setText(QCoreApplication.translate("MainWindow", u"Sequence", None))
        self.pushButton_show_protocol_settings.setText(QCoreApplication.translate("MainWindow", u"Protocol Configuration", None))
        self.toolButton_add_step.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.pushButton_remove_step.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.label_configuration.setText(QCoreApplication.translate("MainWindow", u"Configuration", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuPreferences.setTitle(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.menuTools.setTitle(QCoreApplication.translate("MainWindow", u"Tools", None))
    # retranslateUi

