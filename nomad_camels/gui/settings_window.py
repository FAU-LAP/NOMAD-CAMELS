# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings_window.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QAbstractSpinBox, QApplication, QCheckBox,
    QComboBox, QDialog, QDialogButtonBox, QDoubleSpinBox,
    QFrame, QGridLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QRadioButton, QSizePolicy,
    QSpacerItem, QSpinBox, QTabWidget, QVBoxLayout,
    QWidget)

from nomad_camels.ui_widgets.path_button_edit import Path_Button_Edit
import settings_window_resource_rc

class Ui_settings_window(object):
    def setupUi(self, settings_window):
        if not settings_window.objectName():
            settings_window.setObjectName(u"settings_window")
        settings_window.resize(455, 435)
        self.gridLayout = QGridLayout(settings_window)
        self.gridLayout.setObjectName(u"gridLayout")
        self.tabWidget = QTabWidget(settings_window)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.verticalLayout = QVBoxLayout(self.tab_3)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.saving = QWidget(self.tab_3)
        self.saving.setObjectName(u"saving")
        self.gridLayout_2 = QGridLayout(self.saving)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.radioButton_n_backups = QRadioButton(self.saving)
        self.radioButton_n_backups.setObjectName(u"radioButton_n_backups")

        self.gridLayout_2.addWidget(self.radioButton_n_backups, 3, 1, 1, 1)

        self.checkBox_backup_before_run = QCheckBox(self.saving)
        self.checkBox_backup_before_run.setObjectName(u"checkBox_backup_before_run")

        self.gridLayout_2.addWidget(self.checkBox_backup_before_run, 2, 2, 1, 1)

        self.checkBox_new_file_each_run = QCheckBox(self.saving)
        self.checkBox_new_file_each_run.setObjectName(u"checkBox_new_file_each_run")

        self.gridLayout_2.addWidget(self.checkBox_new_file_each_run, 5, 0, 1, 3)

        self.checkBox_new_meas_hours = QCheckBox(self.saving)
        self.checkBox_new_meas_hours.setObjectName(u"checkBox_new_meas_hours")

        self.gridLayout_2.addWidget(self.checkBox_new_meas_hours, 6, 0, 1, 1)

        self.line_4 = QFrame(self.saving)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShadow(QFrame.Shadow.Raised)
        self.line_4.setLineWidth(5)
        self.line_4.setFrameShape(QFrame.Shape.HLine)

        self.gridLayout_2.addWidget(self.line_4, 8, 0, 1, 3)

        self.radioButton_smart_backups = QRadioButton(self.saving)
        self.radioButton_smart_backups.setObjectName(u"radioButton_smart_backups")
        self.radioButton_smart_backups.setChecked(True)

        self.gridLayout_2.addWidget(self.radioButton_smart_backups, 3, 2, 1, 1)

        self.spinBox_new_meas_hours = QDoubleSpinBox(self.saving)
        self.spinBox_new_meas_hours.setObjectName(u"spinBox_new_meas_hours")
        font = QFont()
        font.setKerning(True)
        self.spinBox_new_meas_hours.setFont(font)
        self.spinBox_new_meas_hours.setDecimals(3)
        self.spinBox_new_meas_hours.setMinimum(0.001000000000000)
        self.spinBox_new_meas_hours.setMaximum(1000.000000000000000)
        self.spinBox_new_meas_hours.setStepType(QAbstractSpinBox.StepType.AdaptiveDecimalStepType)

        self.gridLayout_2.addWidget(self.spinBox_new_meas_hours, 6, 1, 1, 1)

        self.checkBox_autosave = QCheckBox(self.saving)
        self.checkBox_autosave.setObjectName(u"checkBox_autosave")

        self.gridLayout_2.addWidget(self.checkBox_autosave, 2, 0, 1, 1)

        self.pathButton_config_path = Path_Button_Edit(self.saving)
        self.pathButton_config_path.setObjectName(u"pathButton_config_path")

        self.gridLayout_2.addWidget(self.pathButton_config_path, 7, 1, 1, 2)

        self.spinBox_backup_number = QSpinBox(self.saving)
        self.spinBox_backup_number.setObjectName(u"spinBox_backup_number")

        self.gridLayout_2.addWidget(self.spinBox_backup_number, 4, 1, 1, 1)

        self.radioButton_all_backups = QRadioButton(self.saving)
        self.radioButton_all_backups.setObjectName(u"radioButton_all_backups")

        self.gridLayout_2.addWidget(self.radioButton_all_backups, 3, 0, 1, 1)

        self.checkBox_password = QCheckBox(self.saving)
        self.checkBox_password.setObjectName(u"checkBox_password")

        self.gridLayout_2.addWidget(self.checkBox_password, 1, 0, 1, 3)

        self.label_24 = QLabel(self.saving)
        self.label_24.setObjectName(u"label_24")

        self.gridLayout_2.addWidget(self.label_24, 6, 2, 1, 1)

        self.label_12 = QLabel(self.saving)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout_2.addWidget(self.label_12, 7, 0, 1, 1)

        self.checkBox_autosave_run = QCheckBox(self.saving)
        self.checkBox_autosave_run.setObjectName(u"checkBox_autosave_run")

        self.gridLayout_2.addWidget(self.checkBox_autosave_run, 2, 1, 1, 1)

        self.label = QLabel(self.saving)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(16777215, 17))
        font1 = QFont()
        font1.setBold(True)
        font1.setItalic(False)
        self.label.setFont(font1)

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 3)


        self.verticalLayout.addWidget(self.saving)

        self.logging = QWidget(self.tab_3)
        self.logging.setObjectName(u"logging")
        self.gridLayout_4 = QGridLayout(self.logging)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.spinBox_logfile_size = QSpinBox(self.logging)
        self.spinBox_logfile_size.setObjectName(u"spinBox_logfile_size")
        self.spinBox_logfile_size.setValue(1)

        self.gridLayout_4.addWidget(self.spinBox_logfile_size, 2, 1, 1, 1)

        self.comboBox_log_level = QComboBox(self.logging)
        self.comboBox_log_level.setObjectName(u"comboBox_log_level")

        self.gridLayout_4.addWidget(self.comboBox_log_level, 2, 0, 1, 1)

        self.spinBox_logfile_number = QSpinBox(self.logging)
        self.spinBox_logfile_number.setObjectName(u"spinBox_logfile_number")
        self.spinBox_logfile_number.setAcceptDrops(False)
        self.spinBox_logfile_number.setValue(1)

        self.gridLayout_4.addWidget(self.spinBox_logfile_number, 2, 2, 1, 1)

        self.label_9 = QLabel(self.logging)
        self.label_9.setObjectName(u"label_9")
        font2 = QFont()
        font2.setBold(True)
        self.label_9.setFont(font2)

        self.gridLayout_4.addWidget(self.label_9, 0, 0, 1, 1)

        self.label_16 = QLabel(self.logging)
        self.label_16.setObjectName(u"label_16")

        self.gridLayout_4.addWidget(self.label_16, 1, 1, 1, 1)

        self.label_17 = QLabel(self.logging)
        self.label_17.setObjectName(u"label_17")

        self.gridLayout_4.addWidget(self.label_17, 1, 2, 1, 1)

        self.label_15 = QLabel(self.logging)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout_4.addWidget(self.label_15, 1, 0, 1, 1)


        self.verticalLayout.addWidget(self.logging)

        self.line_10 = QFrame(self.tab_3)
        self.line_10.setObjectName(u"line_10")
        self.line_10.setFrameShadow(QFrame.Shadow.Raised)
        self.line_10.setLineWidth(5)
        self.line_10.setFrameShape(QFrame.Shape.HLine)

        self.verticalLayout.addWidget(self.line_10)

        self.updates = QWidget(self.tab_3)
        self.updates.setObjectName(u"updates")
        self.gridLayout_13 = QGridLayout(self.updates)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_13.setContentsMargins(0, 0, 0, 0)
        self.label_23 = QLabel(self.updates)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setFont(font2)
        self.label_23.setStyleSheet(u"")

        self.gridLayout_13.addWidget(self.label_23, 0, 0, 1, 1)

        self.checkBox_auto_check_updates = QCheckBox(self.updates)
        self.checkBox_auto_check_updates.setObjectName(u"checkBox_auto_check_updates")

        self.gridLayout_13.addWidget(self.checkBox_auto_check_updates, 1, 0, 1, 1)


        self.verticalLayout.addWidget(self.updates)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.verticalLayout_2 = QVBoxLayout(self.tab_4)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.sounds = QWidget(self.tab_4)
        self.sounds.setObjectName(u"sounds")
        self.gridLayout_8 = QGridLayout(self.sounds)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(0, 0, 0, 0)
        self.checkBox_finished_sound = QCheckBox(self.sounds)
        self.checkBox_finished_sound.setObjectName(u"checkBox_finished_sound")

        self.gridLayout_8.addWidget(self.checkBox_finished_sound, 1, 1, 1, 1)

        self.line = QFrame(self.sounds)
        self.line.setObjectName(u"line")
        self.line.setFrameShadow(QFrame.Shadow.Raised)
        self.line.setLineWidth(5)
        self.line.setFrameShape(QFrame.Shape.HLine)

        self.gridLayout_8.addWidget(self.line, 2, 0, 1, 2)

        self.checkBox_play_camel_on_error = QCheckBox(self.sounds)
        self.checkBox_play_camel_on_error.setObjectName(u"checkBox_play_camel_on_error")

        self.gridLayout_8.addWidget(self.checkBox_play_camel_on_error, 1, 0, 1, 1)

        self.label_11 = QLabel(self.sounds)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setFont(font2)

        self.gridLayout_8.addWidget(self.label_11, 0, 0, 1, 1)


        self.verticalLayout_2.addWidget(self.sounds)

        self.theme = QWidget(self.tab_4)
        self.theme.setObjectName(u"theme")
        self.gridLayout_5 = QGridLayout(self.theme)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.line_2 = QFrame(self.theme)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShadow(QFrame.Shadow.Raised)
        self.line_2.setLineWidth(5)
        self.line_2.setFrameShape(QFrame.Shape.HLine)

        self.gridLayout_5.addWidget(self.line_2, 2, 0, 1, 3)

        self.checkBox_dark = QCheckBox(self.theme)
        self.checkBox_dark.setObjectName(u"checkBox_dark")

        self.gridLayout_5.addWidget(self.checkBox_dark, 1, 2, 1, 1)

        self.comboBox_material_theme = QComboBox(self.theme)
        self.comboBox_material_theme.setObjectName(u"comboBox_material_theme")

        self.gridLayout_5.addWidget(self.comboBox_material_theme, 1, 1, 1, 1)

        self.comboBox_theme = QComboBox(self.theme)
        self.comboBox_theme.setObjectName(u"comboBox_theme")

        self.gridLayout_5.addWidget(self.comboBox_theme, 1, 0, 1, 1)

        self.label_2 = QLabel(self.theme)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMaximumSize(QSize(16777215, 17))
        self.label_2.setFont(font2)

        self.gridLayout_5.addWidget(self.label_2, 0, 0, 1, 3)


        self.verticalLayout_2.addWidget(self.theme)

        self.number_format = QWidget(self.tab_4)
        self.number_format.setObjectName(u"number_format")
        self.gridLayout_6 = QGridLayout(self.number_format)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.number_format)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMaximumSize(QSize(16777215, 17))
        self.label_3.setFont(font2)

        self.gridLayout_6.addWidget(self.label_3, 0, 0, 1, 3)

        self.label_4 = QLabel(self.number_format)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMaximumSize(QSize(16777215, 17))

        self.gridLayout_6.addWidget(self.label_4, 3, 0, 1, 1)

        self.radioButton_scientific = QRadioButton(self.number_format)
        self.radioButton_scientific.setObjectName(u"radioButton_scientific")

        self.gridLayout_6.addWidget(self.radioButton_scientific, 1, 1, 1, 1)

        self.spinBox_n_decimals = QSpinBox(self.number_format)
        self.spinBox_n_decimals.setObjectName(u"spinBox_n_decimals")
        self.spinBox_n_decimals.setValue(2)

        self.gridLayout_6.addWidget(self.spinBox_n_decimals, 3, 1, 1, 2)

        self.radioButton_mixed = QRadioButton(self.number_format)
        self.radioButton_mixed.setObjectName(u"radioButton_mixed")

        self.gridLayout_6.addWidget(self.radioButton_mixed, 1, 2, 1, 1)

        self.radioButton_plain_numbers = QRadioButton(self.number_format)
        self.radioButton_plain_numbers.setObjectName(u"radioButton_plain_numbers")
        self.radioButton_plain_numbers.setCheckable(True)
        self.radioButton_plain_numbers.setChecked(True)

        self.gridLayout_6.addWidget(self.radioButton_plain_numbers, 1, 0, 1, 1)

        self.spinBox_scientific_from = QSpinBox(self.number_format)
        self.spinBox_scientific_from.setObjectName(u"spinBox_scientific_from")
        self.spinBox_scientific_from.setValue(3)

        self.gridLayout_6.addWidget(self.spinBox_scientific_from, 2, 2, 1, 1)


        self.verticalLayout_2.addWidget(self.number_format)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_3)

        self.tabWidget.addTab(self.tab_4, "")
        self.tab_5 = QWidget()
        self.tab_5.setObjectName(u"tab_5")
        self.verticalLayout_3 = QVBoxLayout(self.tab_5)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.files = QWidget(self.tab_5)
        self.files.setObjectName(u"files")
        self.gridLayout_7 = QGridLayout(self.files)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.label_7 = QLabel(self.files)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMaximumSize(QSize(16777215, 17))

        self.gridLayout_7.addWidget(self.label_7, 2, 0, 1, 1)

        self.label_20 = QLabel(self.files)
        self.label_20.setObjectName(u"label_20")

        self.gridLayout_7.addWidget(self.label_20, 5, 0, 1, 1)

        self.label_6 = QLabel(self.files)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMaximumSize(QSize(16777215, 17))

        self.gridLayout_7.addWidget(self.label_6, 1, 0, 1, 1)

        self.line_6 = QFrame(self.files)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setFrameShadow(QFrame.Shadow.Raised)
        self.line_6.setLineWidth(5)
        self.line_6.setFrameShape(QFrame.Shape.HLine)

        self.gridLayout_7.addWidget(self.line_6, 6, 0, 1, 2)

        self.pathButton_py_files = Path_Button_Edit(self.files)
        self.pathButton_py_files.setObjectName(u"pathButton_py_files")

        self.gridLayout_7.addWidget(self.pathButton_py_files, 1, 1, 1, 1)

        self.lineEdit_catalog_name = QLineEdit(self.files)
        self.lineEdit_catalog_name.setObjectName(u"lineEdit_catalog_name")

        self.gridLayout_7.addWidget(self.lineEdit_catalog_name, 3, 1, 1, 1)

        self.spinBox_n_databroker_files = QSpinBox(self.files)
        self.spinBox_n_databroker_files.setObjectName(u"spinBox_n_databroker_files")

        self.gridLayout_7.addWidget(self.spinBox_n_databroker_files, 5, 1, 1, 1)

        self.label_10 = QLabel(self.files)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_7.addWidget(self.label_10, 3, 0, 1, 1)

        self.pathButton_meas_files = Path_Button_Edit(self.files)
        self.pathButton_meas_files.setObjectName(u"pathButton_meas_files")

        self.gridLayout_7.addWidget(self.pathButton_meas_files, 2, 1, 1, 1)

        self.label_5 = QLabel(self.files)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMaximumSize(QSize(16777215, 17))
        self.label_5.setFont(font2)

        self.gridLayout_7.addWidget(self.label_5, 0, 0, 1, 1)


        self.verticalLayout_3.addWidget(self.files)

        self.drivers = QWidget(self.tab_5)
        self.drivers.setObjectName(u"drivers")
        self.gridLayout_10 = QGridLayout(self.drivers)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setContentsMargins(0, 0, 0, 0)
        self.label_8 = QLabel(self.drivers)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMaximumSize(QSize(16777215, 17))

        self.gridLayout_10.addWidget(self.label_8, 1, 0, 1, 1)

        self.label_13 = QLabel(self.drivers)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setFont(font2)

        self.gridLayout_10.addWidget(self.label_13, 0, 0, 1, 1)

        self.pathButton_device_path = Path_Button_Edit(self.drivers)
        self.pathButton_device_path.setObjectName(u"pathButton_device_path")

        self.gridLayout_10.addWidget(self.pathButton_device_path, 1, 1, 1, 2)


        self.verticalLayout_3.addWidget(self.drivers)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_4)

        self.tabWidget.addTab(self.tab_5, "")
        self.tab_6 = QWidget()
        self.tab_6.setObjectName(u"tab_6")
        self.verticalLayout_4 = QVBoxLayout(self.tab_6)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.eln = QWidget(self.tab_6)
        self.eln.setObjectName(u"eln")
        self.gridLayout_11 = QGridLayout(self.eln)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setContentsMargins(0, 0, 0, 0)
        self.label_18 = QLabel(self.eln)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setFont(font2)

        self.gridLayout_11.addWidget(self.label_18, 0, 0, 1, 2)

        self.lineEdit_oasis = QLineEdit(self.eln)
        self.lineEdit_oasis.setObjectName(u"lineEdit_oasis")

        self.gridLayout_11.addWidget(self.lineEdit_oasis, 1, 1, 1, 1)

        self.label_19 = QLabel(self.eln)
        self.label_19.setObjectName(u"label_19")

        self.gridLayout_11.addWidget(self.label_19, 1, 0, 1, 1)

        self.line_3 = QFrame(self.eln)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShadow(QFrame.Shadow.Raised)
        self.line_3.setLineWidth(5)
        self.line_3.setFrameShape(QFrame.Shape.HLine)

        self.gridLayout_11.addWidget(self.line_3, 2, 0, 1, 2)


        self.verticalLayout_4.addWidget(self.eln)

        self.extensions = QWidget(self.tab_6)
        self.extensions.setObjectName(u"extensions")
        self.gridLayout_12 = QGridLayout(self.extensions)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setContentsMargins(0, 0, 0, 0)
        self.label_21 = QLabel(self.extensions)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setMaximumSize(QSize(16777215, 17))

        self.gridLayout_12.addWidget(self.label_21, 1, 0, 1, 1)

        self.label_22 = QLabel(self.extensions)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setFont(font2)

        self.gridLayout_12.addWidget(self.label_22, 0, 0, 1, 2)

        self.pathButton_extension_path = Path_Button_Edit(self.extensions)
        self.pathButton_extension_path.setObjectName(u"pathButton_extension_path")

        self.gridLayout_12.addWidget(self.pathButton_extension_path, 1, 1, 1, 1)

        self.line_9 = QFrame(self.extensions)
        self.line_9.setObjectName(u"line_9")
        self.line_9.setFrameShadow(QFrame.Shadow.Raised)
        self.line_9.setLineWidth(5)
        self.line_9.setFrameShape(QFrame.Shape.HLine)

        self.gridLayout_12.addWidget(self.line_9, 2, 0, 1, 2)


        self.verticalLayout_4.addWidget(self.extensions)

        self.right = QWidget(self.tab_6)
        self.right.setObjectName(u"right")
        self.gridLayout_9 = QGridLayout(self.right)
        self.gridLayout_9.setSpacing(9)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(3, 3, 3, 3)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, -1, -1, 0)
        self.checkBox_enable_Api = QCheckBox(self.right)
        self.checkBox_enable_Api.setObjectName(u"checkBox_enable_Api")
        self.checkBox_enable_Api.setFont(font2)

        self.horizontalLayout_2.addWidget(self.checkBox_enable_Api)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.label_14 = QLabel(self.right)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setFont(font2)

        self.horizontalLayout_2.addWidget(self.label_14)

        self.lineEdit_api_port = QLineEdit(self.right)
        self.lineEdit_api_port.setObjectName(u"lineEdit_api_port")

        self.horizontalLayout_2.addWidget(self.lineEdit_api_port)


        self.gridLayout_9.addLayout(self.horizontalLayout_2, 4, 0, 1, 1)

        self.pushButton_API_docu = QPushButton(self.right)
        self.pushButton_API_docu.setObjectName(u"pushButton_API_docu")

        self.gridLayout_9.addWidget(self.pushButton_API_docu, 5, 0, 1, 1)

        self.label_ApiKey = QLabel(self.right)
        self.label_ApiKey.setObjectName(u"label_ApiKey")
        self.label_ApiKey.setStyleSheet(u"font-weight: bold;")

        self.gridLayout_9.addWidget(self.label_ApiKey, 3, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 0)
        self.pushButton_generate_Api_key = QPushButton(self.right)
        self.pushButton_generate_Api_key.setObjectName(u"pushButton_generate_Api_key")
        font3 = QFont()
        font3.setPointSize(9)
        font3.setBold(True)
        self.pushButton_generate_Api_key.setFont(font3)
        self.pushButton_generate_Api_key.setStyleSheet(u"QPushButton {\n"
"    background-color: #0db002;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    background-color:#4fa14a; /* A grayish-green color */\n"
"}")

        self.horizontalLayout.addWidget(self.pushButton_generate_Api_key)

        self.pushButton_delete_Api_keys = QPushButton(self.right)
        self.pushButton_delete_Api_keys.setObjectName(u"pushButton_delete_Api_keys")
        self.pushButton_delete_Api_keys.setFont(font3)
        self.pushButton_delete_Api_keys.setStyleSheet(u"QPushButton {\n"
"    background-color: #fa0000;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    background-color: #A52A2A; /* A grayish-red color */\n"
"}")

        self.horizontalLayout.addWidget(self.pushButton_delete_Api_keys)


        self.gridLayout_9.addLayout(self.horizontalLayout, 9, 0, 4, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.Api_key_lineEdit = QLineEdit(self.right)
        self.Api_key_lineEdit.setObjectName(u"Api_key_lineEdit")
        self.Api_key_lineEdit.setReadOnly(True)

        self.horizontalLayout_4.addWidget(self.Api_key_lineEdit)

        self.pushButton_copy_Api_key_clipboard = QPushButton(self.right)
        self.pushButton_copy_Api_key_clipboard.setObjectName(u"pushButton_copy_Api_key_clipboard")
        self.pushButton_copy_Api_key_clipboard.setEnabled(False)
        self.pushButton_copy_Api_key_clipboard.setStyleSheet(u"")
        icon = QIcon()
        icon.addFile(u":/images/graphics/copy_to_clipboard.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_copy_Api_key_clipboard.setIcon(icon)
        self.pushButton_copy_Api_key_clipboard.setIconSize(QSize(16, 16))

        self.horizontalLayout_4.addWidget(self.pushButton_copy_Api_key_clipboard)


        self.gridLayout_9.addLayout(self.horizontalLayout_4, 13, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_9.addItem(self.verticalSpacer_2, 20, 0, 1, 1)


        self.verticalLayout_4.addWidget(self.right)

        self.tabWidget.addTab(self.tab_6, "")

        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(settings_window)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)


        self.retranslateUi(settings_window)
        self.buttonBox.accepted.connect(settings_window.accept)
        self.buttonBox.rejected.connect(settings_window.reject)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(settings_window)
    # setupUi

    def retranslateUi(self, settings_window):
        settings_window.setWindowTitle(QCoreApplication.translate("settings_window", u"Dialog", None))
#if QT_CONFIG(tooltip)
        self.radioButton_n_backups.setToolTip(QCoreApplication.translate("settings_window", u"keep the defined number of newest backups", None))
#endif // QT_CONFIG(tooltip)
        self.radioButton_n_backups.setText(QCoreApplication.translate("settings_window", u"keep only...", None))
#if QT_CONFIG(tooltip)
        self.checkBox_backup_before_run.setToolTip(QCoreApplication.translate("settings_window", u"also does a backup when autosave before run", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_backup_before_run.setText(QCoreApplication.translate("settings_window", u"backup before run", None))
#if QT_CONFIG(tooltip)
        self.checkBox_new_file_each_run.setToolTip(QCoreApplication.translate("settings_window", u"creates a new datafile for each measurement instead of saving new entries in the same hdf5 file", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_new_file_each_run.setText(QCoreApplication.translate("settings_window", u"save each measurement run in new file", None))
        self.checkBox_new_meas_hours.setText(QCoreApplication.translate("settings_window", u"save to a new file each", None))
#if QT_CONFIG(tooltip)
        self.radioButton_smart_backups.setToolTip(QCoreApplication.translate("settings_window", u"keep all backups of the last 7 days,\n"
"one for for each of the last 30,\n"
"one for each of the last 12 months\n"
"and one for each year", None))
#endif // QT_CONFIG(tooltip)
        self.radioButton_smart_backups.setText(QCoreApplication.translate("settings_window", u"\"smart\" backups", None))
#if QT_CONFIG(tooltip)
        self.checkBox_autosave.setToolTip(QCoreApplication.translate("settings_window", u"When CAMELS is closed, the current state is saved.", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_autosave.setText(QCoreApplication.translate("settings_window", u"autosave on closing", None))
#if QT_CONFIG(tooltip)
        self.radioButton_all_backups.setToolTip(QCoreApplication.translate("settings_window", u"keep all backups of the CAMELS state", None))
#endif // QT_CONFIG(tooltip)
        self.radioButton_all_backups.setText(QCoreApplication.translate("settings_window", u"keep all backups", None))
#if QT_CONFIG(tooltip)
        self.checkBox_password.setToolTip(QCoreApplication.translate("settings_window", u"The user is not allowed to change protocols or instrument configuration without the password.", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_password.setText(QCoreApplication.translate("settings_window", u"password protection", None))
        self.label_24.setText(QCoreApplication.translate("settings_window", u"hours", None))
        self.label_12.setText(QCoreApplication.translate("settings_window", u"path for configuration files:", None))
#if QT_CONFIG(tooltip)
        self.checkBox_autosave_run.setToolTip(QCoreApplication.translate("settings_window", u"autosaves when running a protocol", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_autosave_run.setText(QCoreApplication.translate("settings_window", u"autosave before run", None))
        self.label.setText(QCoreApplication.translate("settings_window", u"Saving", None))
#if QT_CONFIG(tooltip)
        self.spinBox_logfile_size.setToolTip(QCoreApplication.translate("settings_window", u"maximum size of the logfile\n"
"if reached, a new file is started", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.comboBox_log_level.setToolTip(QCoreApplication.translate("settings_window", u"the minimum level to write to the log file", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.spinBox_logfile_number.setToolTip(QCoreApplication.translate("settings_window", u"number of old files to keep, when starting a new logfile", None))
#endif // QT_CONFIG(tooltip)
        self.label_9.setText(QCoreApplication.translate("settings_window", u"Logging", None))
        self.label_16.setText(QCoreApplication.translate("settings_window", u"max. logfile size (MB)", None))
        self.label_17.setText(QCoreApplication.translate("settings_window", u"old logfile backups", None))
        self.label_15.setText(QCoreApplication.translate("settings_window", u"Log-Level", None))
        self.label_23.setText(QCoreApplication.translate("settings_window", u"Updates", None))
        self.checkBox_auto_check_updates.setText(QCoreApplication.translate("settings_window", u"automatically search for updates", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("settings_window", u"Saving", None))
#if QT_CONFIG(tooltip)
        self.checkBox_finished_sound.setToolTip(QCoreApplication.translate("settings_window", u"a short sound when a protocol is done", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_finished_sound.setText(QCoreApplication.translate("settings_window", u"Sound on finished protocol", None))
#if QT_CONFIG(tooltip)
        self.checkBox_play_camel_on_error.setToolTip(QCoreApplication.translate("settings_window", u"when an error occurs,\n"
"you will hear a beautiful sound ;)", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_play_camel_on_error.setText(QCoreApplication.translate("settings_window", u"Play Camel-Roar on error", None))
        self.label_11.setText(QCoreApplication.translate("settings_window", u"Sounds", None))
        self.checkBox_dark.setText(QCoreApplication.translate("settings_window", u"dark mode", None))
#if QT_CONFIG(tooltip)
        self.comboBox_material_theme.setToolTip(QCoreApplication.translate("settings_window", u"change the the themes color", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.comboBox_theme.setToolTip(QCoreApplication.translate("settings_window", u"change the appearance of CAMELS", None))
#endif // QT_CONFIG(tooltip)
        self.label_2.setText(QCoreApplication.translate("settings_window", u"Theme", None))
        self.label_3.setText(QCoreApplication.translate("settings_window", u"Number-Formatting (only visual)", None))
        self.label_4.setText(QCoreApplication.translate("settings_window", u"# decimals:", None))
        self.radioButton_scientific.setText(QCoreApplication.translate("settings_window", u"Scientific", None))
        self.radioButton_mixed.setText(QCoreApplication.translate("settings_window", u"Scientific from 1e...", None))
        self.radioButton_plain_numbers.setText(QCoreApplication.translate("settings_window", u"Plain", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QCoreApplication.translate("settings_window", u"Interface", None))
        self.label_7.setText(QCoreApplication.translate("settings_window", u"Measurement-Data Path", None))
        self.label_20.setText(QCoreApplication.translate("settings_window", u"# databroker files", None))
        self.label_6.setText(QCoreApplication.translate("settings_window", u"Python-Files Path", None))
#if QT_CONFIG(tooltip)
        self.pathButton_py_files.setToolTip(QCoreApplication.translate("settings_window", u"where the produced protocol python files are saved", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.lineEdit_catalog_name.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.spinBox_n_databroker_files.setToolTip(QCoreApplication.translate("settings_window", u"with \"0\" all files will be kept", None))
#endif // QT_CONFIG(tooltip)
        self.label_10.setText(QCoreApplication.translate("settings_window", u"Databroker catalog-name", None))
#if QT_CONFIG(tooltip)
        self.pathButton_meas_files.setToolTip(QCoreApplication.translate("settings_window", u"where the data is saved", None))
#endif // QT_CONFIG(tooltip)
        self.label_5.setText(QCoreApplication.translate("settings_window", u"Measurements", None))
        self.label_8.setText(QCoreApplication.translate("settings_window", u"Local drivers path", None))
        self.label_13.setText(QCoreApplication.translate("settings_window", u"Drivers", None))
#if QT_CONFIG(tooltip)
        self.pathButton_device_path.setToolTip(QCoreApplication.translate("settings_window", u"path to local instrument drivers,\n"
"e.g. self-written or adjusted ones", None))
#endif // QT_CONFIG(tooltip)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), QCoreApplication.translate("settings_window", u"Files/Paths", None))
        self.label_18.setText(QCoreApplication.translate("settings_window", u"ELN integration", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_oasis.setToolTip(QCoreApplication.translate("settings_window", u"define your NOMAD Oasis here,\n"
"for quick login", None))
#endif // QT_CONFIG(tooltip)
        self.label_19.setText(QCoreApplication.translate("settings_window", u"NOMAD Oasis URL", None))
        self.label_21.setText(QCoreApplication.translate("settings_window", u"Local extensions path", None))
        self.label_22.setText(QCoreApplication.translate("settings_window", u"Extensions", None))
#if QT_CONFIG(tooltip)
        self.pathButton_extension_path.setToolTip(QCoreApplication.translate("settings_window", u"where to find extensions for CAMELS", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_enable_Api.setText(QCoreApplication.translate("settings_window", u"Enable API", None))
        self.label_14.setText(QCoreApplication.translate("settings_window", u"API Port:", None))
        self.lineEdit_api_port.setPlaceholderText(QCoreApplication.translate("settings_window", u"API Port", None))
        self.pushButton_API_docu.setText(QCoreApplication.translate("settings_window", u"API documentation", None))
        self.label_ApiKey.setText(QCoreApplication.translate("settings_window", u"API Key", None))
        self.pushButton_generate_Api_key.setText(QCoreApplication.translate("settings_window", u"Generate\n"
"API Key", None))
        self.pushButton_delete_Api_keys.setText(QCoreApplication.translate("settings_window", u"Delete ALL\n"
"API keys", None))
        self.pushButton_copy_Api_key_clipboard.setText(QCoreApplication.translate("settings_window", u"Copy key to clipboard", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_6), QCoreApplication.translate("settings_window", u"Advanced", None))
    # retranslateUi

