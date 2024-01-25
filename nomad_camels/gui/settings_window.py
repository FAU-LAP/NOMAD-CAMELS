# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings_window.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QComboBox,
    QDialog, QDialogButtonBox, QFrame, QGridLayout,
    QLabel, QLineEdit, QRadioButton, QSizePolicy,
    QSpacerItem, QSpinBox, QWidget)

from nomad_camels.ui_widgets.path_button_edit import Path_Button_Edit

class Ui_settings_window(object):
    def setupUi(self, settings_window):
        if not settings_window.objectName():
            settings_window.setObjectName(u"settings_window")
        settings_window.resize(634, 495)
        self.gridLayout = QGridLayout(settings_window)
        self.gridLayout.setObjectName(u"gridLayout")
        self.right = QWidget(settings_window)
        self.right.setObjectName(u"right")
        self.gridLayout_9 = QGridLayout(self.right)
        self.gridLayout_9.setSpacing(9)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(3, 3, 3, 3)
        self.drivers = QWidget(self.right)
        self.drivers.setObjectName(u"drivers")
        self.gridLayout_10 = QGridLayout(self.drivers)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setContentsMargins(0, 0, 0, 0)
        self.label_12 = QLabel(self.drivers)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout_10.addWidget(self.label_12, 1, 0, 1, 1)

        self.label_8 = QLabel(self.drivers)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMaximumSize(QSize(16777215, 17))

        self.gridLayout_10.addWidget(self.label_8, 3, 0, 1, 1)

        self.lineEdit_branch = QLineEdit(self.drivers)
        self.lineEdit_branch.setObjectName(u"lineEdit_branch")

        self.gridLayout_10.addWidget(self.lineEdit_branch, 2, 1, 1, 1)

        self.label_13 = QLabel(self.drivers)
        self.label_13.setObjectName(u"label_13")
        font = QFont()
        font.setBold(True)
        self.label_13.setFont(font)

        self.gridLayout_10.addWidget(self.label_13, 0, 0, 1, 1)

        self.lineEdit_directory = QLineEdit(self.drivers)
        self.lineEdit_directory.setObjectName(u"lineEdit_directory")

        self.gridLayout_10.addWidget(self.lineEdit_directory, 2, 2, 1, 1)

        self.label_14 = QLabel(self.drivers)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout_10.addWidget(self.label_14, 2, 0, 1, 1)

        self.lineEdit_repo = QLineEdit(self.drivers)
        self.lineEdit_repo.setObjectName(u"lineEdit_repo")

        self.gridLayout_10.addWidget(self.lineEdit_repo, 1, 1, 1, 2)

        self.pathButton_device_path = Path_Button_Edit(self.drivers)
        self.pathButton_device_path.setObjectName(u"pathButton_device_path")

        self.gridLayout_10.addWidget(self.pathButton_device_path, 3, 1, 1, 2)

        self.line_5 = QFrame(self.drivers)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShadow(QFrame.Raised)
        self.line_5.setLineWidth(5)
        self.line_5.setFrameShape(QFrame.HLine)

        self.gridLayout_10.addWidget(self.line_5, 4, 0, 1, 3)


        self.gridLayout_9.addWidget(self.drivers, 1, 0, 1, 1)

        self.eln = QWidget(self.right)
        self.eln.setObjectName(u"eln")
        self.gridLayout_11 = QGridLayout(self.eln)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setContentsMargins(0, 0, 0, 0)
        self.label_19 = QLabel(self.eln)
        self.label_19.setObjectName(u"label_19")

        self.gridLayout_11.addWidget(self.label_19, 1, 0, 1, 1)

        self.lineEdit_oasis = QLineEdit(self.eln)
        self.lineEdit_oasis.setObjectName(u"lineEdit_oasis")

        self.gridLayout_11.addWidget(self.lineEdit_oasis, 1, 1, 1, 1)

        self.label_18 = QLabel(self.eln)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setFont(font)

        self.gridLayout_11.addWidget(self.label_18, 0, 0, 1, 2)

        self.line_3 = QFrame(self.eln)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShadow(QFrame.Raised)
        self.line_3.setLineWidth(5)
        self.line_3.setFrameShape(QFrame.HLine)

        self.gridLayout_11.addWidget(self.line_3, 2, 0, 1, 2)


        self.gridLayout_9.addWidget(self.eln, 2, 0, 1, 1)

        self.files = QWidget(self.right)
        self.files.setObjectName(u"files")
        self.gridLayout_7 = QGridLayout(self.files)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.label_7 = QLabel(self.files)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMaximumSize(QSize(16777215, 17))

        self.gridLayout_7.addWidget(self.label_7, 2, 0, 1, 1)

        self.label_6 = QLabel(self.files)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMaximumSize(QSize(16777215, 17))

        self.gridLayout_7.addWidget(self.label_6, 1, 0, 1, 1)

        self.label_10 = QLabel(self.files)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_7.addWidget(self.label_10, 3, 0, 1, 1)

        self.lineEdit_catalog_name = QLineEdit(self.files)
        self.lineEdit_catalog_name.setObjectName(u"lineEdit_catalog_name")

        self.gridLayout_7.addWidget(self.lineEdit_catalog_name, 3, 1, 1, 1)

        self.line_6 = QFrame(self.files)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setFrameShadow(QFrame.Raised)
        self.line_6.setLineWidth(5)
        self.line_6.setFrameShape(QFrame.HLine)

        self.gridLayout_7.addWidget(self.line_6, 6, 0, 1, 2)

        self.label_5 = QLabel(self.files)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMaximumSize(QSize(16777215, 17))
        self.label_5.setFont(font)

        self.gridLayout_7.addWidget(self.label_5, 0, 0, 1, 1)

        self.pathButton_meas_files = Path_Button_Edit(self.files)
        self.pathButton_meas_files.setObjectName(u"pathButton_meas_files")

        self.gridLayout_7.addWidget(self.pathButton_meas_files, 2, 1, 1, 1)

        self.pathButton_py_files = Path_Button_Edit(self.files)
        self.pathButton_py_files.setObjectName(u"pathButton_py_files")

        self.gridLayout_7.addWidget(self.pathButton_py_files, 1, 1, 1, 1)

        self.label_20 = QLabel(self.files)
        self.label_20.setObjectName(u"label_20")

        self.gridLayout_7.addWidget(self.label_20, 5, 0, 1, 1)

        self.spinBox_n_databroker_files = QSpinBox(self.files)
        self.spinBox_n_databroker_files.setObjectName(u"spinBox_n_databroker_files")

        self.gridLayout_7.addWidget(self.spinBox_n_databroker_files, 5, 1, 1, 1)


        self.gridLayout_9.addWidget(self.files, 0, 0, 1, 1)

        self.extensions = QWidget(self.right)
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
        self.label_22.setFont(font)

        self.gridLayout_12.addWidget(self.label_22, 0, 0, 1, 2)

        self.pathButton_extension_path = Path_Button_Edit(self.extensions)
        self.pathButton_extension_path.setObjectName(u"pathButton_extension_path")

        self.gridLayout_12.addWidget(self.pathButton_extension_path, 1, 1, 1, 1)

        self.line_9 = QFrame(self.extensions)
        self.line_9.setObjectName(u"line_9")
        self.line_9.setFrameShadow(QFrame.Raised)
        self.line_9.setLineWidth(5)
        self.line_9.setFrameShape(QFrame.HLine)

        self.gridLayout_12.addWidget(self.line_9, 2, 0, 1, 2)


        self.gridLayout_9.addWidget(self.extensions, 3, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_9.addItem(self.verticalSpacer_2, 5, 0, 1, 1)

        self.updates = QWidget(self.right)
        self.updates.setObjectName(u"updates")
        self.gridLayout_13 = QGridLayout(self.updates)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_13.setContentsMargins(0, 0, 0, 0)
        self.checkBox_auto_check_updates = QCheckBox(self.updates)
        self.checkBox_auto_check_updates.setObjectName(u"checkBox_auto_check_updates")

        self.gridLayout_13.addWidget(self.checkBox_auto_check_updates, 1, 0, 1, 1)

        self.label_23 = QLabel(self.updates)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setFont(font)

        self.gridLayout_13.addWidget(self.label_23, 0, 0, 1, 1)

        self.line_10 = QFrame(self.updates)
        self.line_10.setObjectName(u"line_10")
        self.line_10.setFrameShadow(QFrame.Raised)
        self.line_10.setLineWidth(5)
        self.line_10.setFrameShape(QFrame.HLine)

        self.gridLayout_13.addWidget(self.line_10, 2, 0, 1, 1)


        self.gridLayout_9.addWidget(self.updates, 4, 0, 1, 1)


        self.gridLayout.addWidget(self.right, 0, 3, 1, 1)

        self.line_vertical = QFrame(settings_window)
        self.line_vertical.setObjectName(u"line_vertical")
        self.line_vertical.setFrameShadow(QFrame.Raised)
        self.line_vertical.setLineWidth(5)
        self.line_vertical.setFrameShape(QFrame.VLine)

        self.gridLayout.addWidget(self.line_vertical, 0, 2, 1, 1)

        self.buttonBox = QDialogButtonBox(settings_window)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 4)

        self.left = QWidget(settings_window)
        self.left.setObjectName(u"left")
        self.gridLayout_3 = QGridLayout(self.left)
        self.gridLayout_3.setSpacing(9)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(3, 3, 3, 3)
        self.logging = QWidget(self.left)
        self.logging.setObjectName(u"logging")
        self.gridLayout_4 = QGridLayout(self.logging)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label_9 = QLabel(self.logging)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setFont(font)

        self.gridLayout_4.addWidget(self.label_9, 0, 0, 1, 1)

        self.spinBox_logfile_size = QSpinBox(self.logging)
        self.spinBox_logfile_size.setObjectName(u"spinBox_logfile_size")
        self.spinBox_logfile_size.setValue(1)

        self.gridLayout_4.addWidget(self.spinBox_logfile_size, 2, 1, 1, 1)

        self.spinBox_logfile_number = QSpinBox(self.logging)
        self.spinBox_logfile_number.setObjectName(u"spinBox_logfile_number")
        self.spinBox_logfile_number.setValue(1)

        self.gridLayout_4.addWidget(self.spinBox_logfile_number, 2, 2, 1, 1)

        self.label_17 = QLabel(self.logging)
        self.label_17.setObjectName(u"label_17")

        self.gridLayout_4.addWidget(self.label_17, 1, 2, 1, 1)

        self.label_16 = QLabel(self.logging)
        self.label_16.setObjectName(u"label_16")

        self.gridLayout_4.addWidget(self.label_16, 1, 1, 1, 1)

        self.comboBox_log_level = QComboBox(self.logging)
        self.comboBox_log_level.setObjectName(u"comboBox_log_level")

        self.gridLayout_4.addWidget(self.comboBox_log_level, 2, 0, 1, 1)

        self.label_15 = QLabel(self.logging)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout_4.addWidget(self.label_15, 1, 0, 1, 1)

        self.line_8 = QFrame(self.logging)
        self.line_8.setObjectName(u"line_8")
        self.line_8.setFrameShadow(QFrame.Raised)
        self.line_8.setLineWidth(5)
        self.line_8.setFrameShape(QFrame.HLine)

        self.gridLayout_4.addWidget(self.line_8, 3, 0, 1, 3)


        self.gridLayout_3.addWidget(self.logging, 1, 0, 1, 1)

        self.saving = QWidget(self.left)
        self.saving.setObjectName(u"saving")
        self.gridLayout_2 = QGridLayout(self.saving)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.radioButton_smart_backups = QRadioButton(self.saving)
        self.radioButton_smart_backups.setObjectName(u"radioButton_smart_backups")
        self.radioButton_smart_backups.setChecked(True)

        self.gridLayout_2.addWidget(self.radioButton_smart_backups, 3, 2, 1, 1)

        self.spinBox_backup_number = QSpinBox(self.saving)
        self.spinBox_backup_number.setObjectName(u"spinBox_backup_number")

        self.gridLayout_2.addWidget(self.spinBox_backup_number, 4, 1, 1, 1)

        self.radioButton_all_backups = QRadioButton(self.saving)
        self.radioButton_all_backups.setObjectName(u"radioButton_all_backups")

        self.gridLayout_2.addWidget(self.radioButton_all_backups, 3, 0, 1, 1)

        self.radioButton_n_backups = QRadioButton(self.saving)
        self.radioButton_n_backups.setObjectName(u"radioButton_n_backups")

        self.gridLayout_2.addWidget(self.radioButton_n_backups, 3, 1, 1, 1)

        self.line_4 = QFrame(self.saving)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShadow(QFrame.Raised)
        self.line_4.setLineWidth(5)
        self.line_4.setFrameShape(QFrame.HLine)

        self.gridLayout_2.addWidget(self.line_4, 6, 0, 1, 3)

        self.checkBox_autosave_run = QCheckBox(self.saving)
        self.checkBox_autosave_run.setObjectName(u"checkBox_autosave_run")

        self.gridLayout_2.addWidget(self.checkBox_autosave_run, 2, 2, 1, 1)

        self.checkBox_backup_before_run = QCheckBox(self.saving)
        self.checkBox_backup_before_run.setObjectName(u"checkBox_backup_before_run")

        self.gridLayout_2.addWidget(self.checkBox_backup_before_run, 2, 1, 1, 1)

        self.label = QLabel(self.saving)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(16777215, 17))
        font1 = QFont()
        font1.setBold(True)
        font1.setItalic(False)
        self.label.setFont(font1)

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 3)

        self.checkBox_autosave = QCheckBox(self.saving)
        self.checkBox_autosave.setObjectName(u"checkBox_autosave")

        self.gridLayout_2.addWidget(self.checkBox_autosave, 2, 0, 1, 1)

        self.checkBox_password = QCheckBox(self.saving)
        self.checkBox_password.setObjectName(u"checkBox_password")

        self.gridLayout_2.addWidget(self.checkBox_password, 1, 0, 1, 3)

        self.checkBox_new_file_each_run = QCheckBox(self.saving)
        self.checkBox_new_file_each_run.setObjectName(u"checkBox_new_file_each_run")

        self.gridLayout_2.addWidget(self.checkBox_new_file_each_run, 5, 0, 1, 3)


        self.gridLayout_3.addWidget(self.saving, 0, 0, 1, 1)

        self.sounds = QWidget(self.left)
        self.sounds.setObjectName(u"sounds")
        self.gridLayout_8 = QGridLayout(self.sounds)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(0, 0, 0, 0)
        self.checkBox_play_camel_on_error = QCheckBox(self.sounds)
        self.checkBox_play_camel_on_error.setObjectName(u"checkBox_play_camel_on_error")

        self.gridLayout_8.addWidget(self.checkBox_play_camel_on_error, 1, 0, 1, 1)

        self.label_11 = QLabel(self.sounds)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setFont(font)

        self.gridLayout_8.addWidget(self.label_11, 0, 0, 1, 1)

        self.line = QFrame(self.sounds)
        self.line.setObjectName(u"line")
        self.line.setFrameShadow(QFrame.Raised)
        self.line.setLineWidth(5)
        self.line.setFrameShape(QFrame.HLine)

        self.gridLayout_8.addWidget(self.line, 2, 0, 1, 1)


        self.gridLayout_3.addWidget(self.sounds, 3, 0, 1, 1)

        self.number_format = QWidget(self.left)
        self.number_format.setObjectName(u"number_format")
        self.gridLayout_6 = QGridLayout(self.number_format)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.number_format)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMaximumSize(QSize(16777215, 17))
        self.label_3.setFont(font)

        self.gridLayout_6.addWidget(self.label_3, 0, 0, 1, 3)

        self.radioButton_mixed = QRadioButton(self.number_format)
        self.radioButton_mixed.setObjectName(u"radioButton_mixed")

        self.gridLayout_6.addWidget(self.radioButton_mixed, 1, 2, 1, 1)

        self.radioButton_plain_numbers = QRadioButton(self.number_format)
        self.radioButton_plain_numbers.setObjectName(u"radioButton_plain_numbers")
        self.radioButton_plain_numbers.setCheckable(True)
        self.radioButton_plain_numbers.setChecked(True)

        self.gridLayout_6.addWidget(self.radioButton_plain_numbers, 1, 0, 1, 1)

        self.spinBox_n_decimals = QSpinBox(self.number_format)
        self.spinBox_n_decimals.setObjectName(u"spinBox_n_decimals")
        self.spinBox_n_decimals.setValue(2)

        self.gridLayout_6.addWidget(self.spinBox_n_decimals, 3, 1, 1, 2)

        self.spinBox_scientific_from = QSpinBox(self.number_format)
        self.spinBox_scientific_from.setObjectName(u"spinBox_scientific_from")
        self.spinBox_scientific_from.setValue(3)

        self.gridLayout_6.addWidget(self.spinBox_scientific_from, 2, 2, 1, 1)

        self.label_4 = QLabel(self.number_format)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMaximumSize(QSize(16777215, 17))

        self.gridLayout_6.addWidget(self.label_4, 3, 0, 1, 1)

        self.radioButton_scientific = QRadioButton(self.number_format)
        self.radioButton_scientific.setObjectName(u"radioButton_scientific")

        self.gridLayout_6.addWidget(self.radioButton_scientific, 1, 1, 1, 1)

        self.line_7 = QFrame(self.number_format)
        self.line_7.setObjectName(u"line_7")
        self.line_7.setFrameShadow(QFrame.Raised)
        self.line_7.setLineWidth(5)
        self.line_7.setFrameShape(QFrame.HLine)

        self.gridLayout_6.addWidget(self.line_7, 4, 0, 1, 3)


        self.gridLayout_3.addWidget(self.number_format, 5, 0, 1, 1)

        self.theme = QWidget(self.left)
        self.theme.setObjectName(u"theme")
        self.gridLayout_5 = QGridLayout(self.theme)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.checkBox_dark = QCheckBox(self.theme)
        self.checkBox_dark.setObjectName(u"checkBox_dark")

        self.gridLayout_5.addWidget(self.checkBox_dark, 1, 2, 1, 1)

        self.label_2 = QLabel(self.theme)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMaximumSize(QSize(16777215, 17))
        self.label_2.setFont(font)

        self.gridLayout_5.addWidget(self.label_2, 0, 0, 1, 3)

        self.comboBox_theme = QComboBox(self.theme)
        self.comboBox_theme.setObjectName(u"comboBox_theme")

        self.gridLayout_5.addWidget(self.comboBox_theme, 1, 0, 1, 1)

        self.comboBox_material_theme = QComboBox(self.theme)
        self.comboBox_material_theme.setObjectName(u"comboBox_material_theme")

        self.gridLayout_5.addWidget(self.comboBox_material_theme, 1, 1, 1, 1)

        self.line_2 = QFrame(self.theme)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShadow(QFrame.Raised)
        self.line_2.setLineWidth(5)
        self.line_2.setFrameShape(QFrame.HLine)

        self.gridLayout_5.addWidget(self.line_2, 2, 0, 1, 3)


        self.gridLayout_3.addWidget(self.theme, 4, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer, 6, 0, 1, 1)


        self.gridLayout.addWidget(self.left, 0, 0, 2, 2)


        self.retranslateUi(settings_window)
        self.buttonBox.accepted.connect(settings_window.accept)
        self.buttonBox.rejected.connect(settings_window.reject)

        QMetaObject.connectSlotsByName(settings_window)
    # setupUi

    def retranslateUi(self, settings_window):
        settings_window.setWindowTitle(QCoreApplication.translate("settings_window", u"Dialog", None))
        self.label_12.setText(QCoreApplication.translate("settings_window", u"Driver Repository URL", None))
        self.label_8.setText(QCoreApplication.translate("settings_window", u"Local drivers path", None))
        self.lineEdit_branch.setPlaceholderText(QCoreApplication.translate("settings_window", u"branch", None))
        self.label_13.setText(QCoreApplication.translate("settings_window", u"Drivers", None))
        self.lineEdit_directory.setPlaceholderText(QCoreApplication.translate("settings_window", u"directory", None))
        self.label_14.setText(QCoreApplication.translate("settings_window", u"Branch / Directory", None))
        self.label_19.setText(QCoreApplication.translate("settings_window", u"NOMAD Oasis URL", None))
        self.label_18.setText(QCoreApplication.translate("settings_window", u"ELN integration", None))
        self.label_7.setText(QCoreApplication.translate("settings_window", u"Measurement-Data Path", None))
        self.label_6.setText(QCoreApplication.translate("settings_window", u"Python-Files Path", None))
        self.label_10.setText(QCoreApplication.translate("settings_window", u"Databroker catalog-name", None))
        self.label_5.setText(QCoreApplication.translate("settings_window", u"Files", None))
        self.label_20.setText(QCoreApplication.translate("settings_window", u"# databroker files", None))
#if QT_CONFIG(tooltip)
        self.spinBox_n_databroker_files.setToolTip(QCoreApplication.translate("settings_window", u"with \"0\" all files will be kept", None))
#endif // QT_CONFIG(tooltip)
        self.label_21.setText(QCoreApplication.translate("settings_window", u"Local extensions path", None))
        self.label_22.setText(QCoreApplication.translate("settings_window", u"Extensions", None))
        self.checkBox_auto_check_updates.setText(QCoreApplication.translate("settings_window", u"automatically search for updates", None))
        self.label_23.setText(QCoreApplication.translate("settings_window", u"Updates", None))
        self.label_9.setText(QCoreApplication.translate("settings_window", u"Logging", None))
        self.label_17.setText(QCoreApplication.translate("settings_window", u"old logfile backups", None))
        self.label_16.setText(QCoreApplication.translate("settings_window", u"max. logfile size (MB)", None))
        self.label_15.setText(QCoreApplication.translate("settings_window", u"Log-Level", None))
        self.radioButton_smart_backups.setText(QCoreApplication.translate("settings_window", u"\"smart\" backups", None))
        self.radioButton_all_backups.setText(QCoreApplication.translate("settings_window", u"keep all backups", None))
        self.radioButton_n_backups.setText(QCoreApplication.translate("settings_window", u"keep only...", None))
        self.checkBox_autosave_run.setText(QCoreApplication.translate("settings_window", u"autosave before run", None))
        self.checkBox_backup_before_run.setText(QCoreApplication.translate("settings_window", u"backup before run", None))
        self.label.setText(QCoreApplication.translate("settings_window", u"Saving", None))
        self.checkBox_autosave.setText(QCoreApplication.translate("settings_window", u"autosave on closing", None))
        self.checkBox_password.setText(QCoreApplication.translate("settings_window", u"password protection", None))
        self.checkBox_new_file_each_run.setText(QCoreApplication.translate("settings_window", u"save each measurement run in new file", None))
        self.checkBox_play_camel_on_error.setText(QCoreApplication.translate("settings_window", u"Play Camel-Roar on error", None))
        self.label_11.setText(QCoreApplication.translate("settings_window", u"Sounds", None))
        self.label_3.setText(QCoreApplication.translate("settings_window", u"Number-Formatting (only visual)", None))
        self.radioButton_mixed.setText(QCoreApplication.translate("settings_window", u"Scientific from 1e...", None))
        self.radioButton_plain_numbers.setText(QCoreApplication.translate("settings_window", u"Plain", None))
        self.label_4.setText(QCoreApplication.translate("settings_window", u"# decimals:", None))
        self.radioButton_scientific.setText(QCoreApplication.translate("settings_window", u"Scientific", None))
        self.checkBox_dark.setText(QCoreApplication.translate("settings_window", u"dark mode", None))
        self.label_2.setText(QCoreApplication.translate("settings_window", u"Theme", None))
    # retranslateUi

