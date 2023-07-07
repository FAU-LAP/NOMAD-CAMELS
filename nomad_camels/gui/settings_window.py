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
    QSpinBox, QWidget)

from nomad_camels.ui_widgets.path_button_edit import Path_Button_Edit

class Ui_settings_window(object):
    def setupUi(self, settings_window):
        if not settings_window.objectName():
            settings_window.setObjectName(u"settings_window")
        settings_window.resize(391, 578)
        self.gridLayout = QGridLayout(settings_window)
        self.gridLayout.setObjectName(u"gridLayout")
        self.checkBox_play_camel_on_error = QCheckBox(settings_window)
        self.checkBox_play_camel_on_error.setObjectName(u"checkBox_play_camel_on_error")

        self.gridLayout.addWidget(self.checkBox_play_camel_on_error, 30, 1, 1, 3)

        self.pathButton_meas_files = Path_Button_Edit(settings_window)
        self.pathButton_meas_files.setObjectName(u"pathButton_meas_files")

        self.gridLayout.addWidget(self.pathButton_meas_files, 21, 2, 1, 2)

        self.pathButton_py_files = Path_Button_Edit(settings_window)
        self.pathButton_py_files.setObjectName(u"pathButton_py_files")

        self.gridLayout.addWidget(self.pathButton_py_files, 18, 2, 1, 2)

        self.pathButton_device_path = Path_Button_Edit(settings_window)
        self.pathButton_device_path.setObjectName(u"pathButton_device_path")

        self.gridLayout.addWidget(self.pathButton_device_path, 27, 2, 1, 2)

        self.line_6 = QFrame(settings_window)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setFrameShadow(QFrame.Raised)
        self.line_6.setLineWidth(5)
        self.line_6.setFrameShape(QFrame.HLine)

        self.gridLayout.addWidget(self.line_6, 23, 1, 1, 3)

        self.lineEdit_branch = QLineEdit(settings_window)
        self.lineEdit_branch.setObjectName(u"lineEdit_branch")

        self.gridLayout.addWidget(self.lineEdit_branch, 26, 2, 1, 1)

        self.label_3 = QLabel(settings_window)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMaximumSize(QSize(16777215, 17))
        font = QFont()
        font.setBold(True)
        self.label_3.setFont(font)

        self.gridLayout.addWidget(self.label_3, 12, 1, 1, 3)

        self.comboBox_theme = QComboBox(settings_window)
        self.comboBox_theme.setObjectName(u"comboBox_theme")

        self.gridLayout.addWidget(self.comboBox_theme, 9, 1, 1, 1)

        self.line_2 = QFrame(settings_window)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShadow(QFrame.Raised)
        self.line_2.setLineWidth(5)
        self.line_2.setFrameShape(QFrame.HLine)

        self.gridLayout.addWidget(self.line_2, 10, 1, 1, 3)

        self.lineEdit_catalog_name = QLineEdit(settings_window)
        self.lineEdit_catalog_name.setObjectName(u"lineEdit_catalog_name")

        self.gridLayout.addWidget(self.lineEdit_catalog_name, 22, 2, 1, 2)

        self.line_5 = QFrame(settings_window)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShadow(QFrame.Raised)
        self.line_5.setLineWidth(5)
        self.line_5.setFrameShape(QFrame.HLine)

        self.gridLayout.addWidget(self.line_5, 28, 1, 1, 3)

        self.radioButton_scientific = QRadioButton(settings_window)
        self.radioButton_scientific.setObjectName(u"radioButton_scientific")

        self.gridLayout.addWidget(self.radioButton_scientific, 13, 2, 1, 1)

        self.label_2 = QLabel(settings_window)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMaximumSize(QSize(16777215, 17))
        self.label_2.setFont(font)

        self.gridLayout.addWidget(self.label_2, 8, 1, 1, 3)

        self.label_5 = QLabel(settings_window)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMaximumSize(QSize(16777215, 17))
        self.label_5.setFont(font)

        self.gridLayout.addWidget(self.label_5, 17, 1, 1, 3)

        self.label_7 = QLabel(settings_window)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMaximumSize(QSize(16777215, 17))

        self.gridLayout.addWidget(self.label_7, 21, 1, 1, 1)

        self.label_8 = QLabel(settings_window)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMaximumSize(QSize(16777215, 17))

        self.gridLayout.addWidget(self.label_8, 27, 1, 1, 1)

        self.lineEdit_directory = QLineEdit(settings_window)
        self.lineEdit_directory.setObjectName(u"lineEdit_directory")

        self.gridLayout.addWidget(self.lineEdit_directory, 26, 3, 1, 1)

        self.lineEdit_repo = QLineEdit(settings_window)
        self.lineEdit_repo.setObjectName(u"lineEdit_repo")

        self.gridLayout.addWidget(self.lineEdit_repo, 25, 2, 1, 2)

        self.spinBox_n_decimals = QSpinBox(settings_window)
        self.spinBox_n_decimals.setObjectName(u"spinBox_n_decimals")
        self.spinBox_n_decimals.setValue(2)

        self.gridLayout.addWidget(self.spinBox_n_decimals, 15, 2, 1, 2)

        self.line = QFrame(settings_window)
        self.line.setObjectName(u"line")
        self.line.setFrameShadow(QFrame.Raised)
        self.line.setLineWidth(5)
        self.line.setFrameShape(QFrame.HLine)

        self.gridLayout.addWidget(self.line, 7, 1, 1, 3)

        self.label_13 = QLabel(settings_window)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setFont(font)

        self.gridLayout.addWidget(self.label_13, 24, 1, 1, 3)

        self.label_6 = QLabel(settings_window)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMaximumSize(QSize(16777215, 17))

        self.gridLayout.addWidget(self.label_6, 18, 1, 1, 1)

        self.line_3 = QFrame(settings_window)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShadow(QFrame.Raised)
        self.line_3.setLineWidth(5)
        self.line_3.setFrameShape(QFrame.HLine)

        self.gridLayout.addWidget(self.line_3, 16, 1, 1, 3)

        self.comboBox_material_theme = QComboBox(settings_window)
        self.comboBox_material_theme.setObjectName(u"comboBox_material_theme")

        self.gridLayout.addWidget(self.comboBox_material_theme, 9, 2, 1, 1)

        self.radioButton_mixed = QRadioButton(settings_window)
        self.radioButton_mixed.setObjectName(u"radioButton_mixed")

        self.gridLayout.addWidget(self.radioButton_mixed, 13, 3, 1, 1)

        self.radioButton_plain_numbers = QRadioButton(settings_window)
        self.radioButton_plain_numbers.setObjectName(u"radioButton_plain_numbers")
        self.radioButton_plain_numbers.setCheckable(True)
        self.radioButton_plain_numbers.setChecked(True)

        self.gridLayout.addWidget(self.radioButton_plain_numbers, 13, 1, 1, 1)

        self.checkBox_dark = QCheckBox(settings_window)
        self.checkBox_dark.setObjectName(u"checkBox_dark")

        self.gridLayout.addWidget(self.checkBox_dark, 9, 3, 1, 1)

        self.label_11 = QLabel(settings_window)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setFont(font)

        self.gridLayout.addWidget(self.label_11, 29, 1, 1, 3)

        self.label = QLabel(settings_window)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(16777215, 17))
        font1 = QFont()
        font1.setBold(True)
        font1.setItalic(False)
        self.label.setFont(font1)

        self.gridLayout.addWidget(self.label, 0, 1, 1, 3)

        self.spinBox_scientific_from = QSpinBox(settings_window)
        self.spinBox_scientific_from.setObjectName(u"spinBox_scientific_from")
        self.spinBox_scientific_from.setValue(3)

        self.gridLayout.addWidget(self.spinBox_scientific_from, 14, 3, 1, 1)

        self.label_14 = QLabel(settings_window)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout.addWidget(self.label_14, 26, 1, 1, 1)

        self.buttonBox = QDialogButtonBox(settings_window)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 31, 1, 1, 3)

        self.label_12 = QLabel(settings_window)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout.addWidget(self.label_12, 25, 1, 1, 1)

        self.label_4 = QLabel(settings_window)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMaximumSize(QSize(16777215, 17))

        self.gridLayout.addWidget(self.label_4, 15, 1, 1, 1)

        self.label_10 = QLabel(settings_window)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout.addWidget(self.label_10, 22, 1, 1, 1)

        self.checkBox_autosave = QCheckBox(settings_window)
        self.checkBox_autosave.setObjectName(u"checkBox_autosave")

        self.gridLayout.addWidget(self.checkBox_autosave, 1, 1, 1, 1)

        self.checkBox_backup_before_run = QCheckBox(settings_window)
        self.checkBox_backup_before_run.setObjectName(u"checkBox_backup_before_run")

        self.gridLayout.addWidget(self.checkBox_backup_before_run, 1, 3, 1, 1)

        self.checkBox_autosave_run = QCheckBox(settings_window)
        self.checkBox_autosave_run.setObjectName(u"checkBox_autosave_run")

        self.gridLayout.addWidget(self.checkBox_autosave_run, 1, 2, 1, 1)

        self.checkBox_auto_check_updates = QCheckBox(settings_window)
        self.checkBox_auto_check_updates.setObjectName(u"checkBox_auto_check_updates")

        self.gridLayout.addWidget(self.checkBox_auto_check_updates, 2, 1, 1, 3)

        self.line_4 = QFrame(settings_window)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShadow(QFrame.Raised)
        self.line_4.setLineWidth(5)
        self.line_4.setFrameShape(QFrame.HLine)

        self.gridLayout.addWidget(self.line_4, 3, 1, 1, 3)

        self.label_17 = QLabel(settings_window)
        self.label_17.setObjectName(u"label_17")

        self.gridLayout.addWidget(self.label_17, 5, 3, 1, 1)

        self.label_15 = QLabel(settings_window)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout.addWidget(self.label_15, 5, 1, 1, 1)

        self.label_9 = QLabel(settings_window)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setFont(font)

        self.gridLayout.addWidget(self.label_9, 4, 1, 1, 3)

        self.label_16 = QLabel(settings_window)
        self.label_16.setObjectName(u"label_16")

        self.gridLayout.addWidget(self.label_16, 5, 2, 1, 1)

        self.spinBox_logfile_size = QSpinBox(settings_window)
        self.spinBox_logfile_size.setObjectName(u"spinBox_logfile_size")
        self.spinBox_logfile_size.setValue(1)

        self.gridLayout.addWidget(self.spinBox_logfile_size, 6, 2, 1, 1)

        self.spinBox_logfile_number = QSpinBox(settings_window)
        self.spinBox_logfile_number.setObjectName(u"spinBox_logfile_number")
        self.spinBox_logfile_number.setValue(1)

        self.gridLayout.addWidget(self.spinBox_logfile_number, 6, 3, 1, 1)

        self.comboBox_log_level = QComboBox(settings_window)
        self.comboBox_log_level.setObjectName(u"comboBox_log_level")

        self.gridLayout.addWidget(self.comboBox_log_level, 6, 1, 1, 1)


        self.retranslateUi(settings_window)
        self.buttonBox.accepted.connect(settings_window.accept)
        self.buttonBox.rejected.connect(settings_window.reject)

        QMetaObject.connectSlotsByName(settings_window)
    # setupUi

    def retranslateUi(self, settings_window):
        settings_window.setWindowTitle(QCoreApplication.translate("settings_window", u"Dialog", None))
        self.checkBox_play_camel_on_error.setText(QCoreApplication.translate("settings_window", u"Play Camel-Roar on error", None))
        self.lineEdit_branch.setPlaceholderText(QCoreApplication.translate("settings_window", u"branch", None))
        self.label_3.setText(QCoreApplication.translate("settings_window", u"Number-Formatting (only visual)", None))
        self.radioButton_scientific.setText(QCoreApplication.translate("settings_window", u"Scientific", None))
        self.label_2.setText(QCoreApplication.translate("settings_window", u"Theme", None))
        self.label_5.setText(QCoreApplication.translate("settings_window", u"Files", None))
        self.label_7.setText(QCoreApplication.translate("settings_window", u"Measurement-Data Path", None))
        self.label_8.setText(QCoreApplication.translate("settings_window", u"Local drivers path", None))
        self.lineEdit_directory.setPlaceholderText(QCoreApplication.translate("settings_window", u"directory", None))
        self.label_13.setText(QCoreApplication.translate("settings_window", u"Drivers", None))
        self.label_6.setText(QCoreApplication.translate("settings_window", u"Python-Files Path", None))
        self.radioButton_mixed.setText(QCoreApplication.translate("settings_window", u"Scientific from 1e...", None))
        self.radioButton_plain_numbers.setText(QCoreApplication.translate("settings_window", u"Plain", None))
        self.checkBox_dark.setText(QCoreApplication.translate("settings_window", u"dark mode", None))
        self.label_11.setText(QCoreApplication.translate("settings_window", u"Sounds", None))
        self.label.setText(QCoreApplication.translate("settings_window", u"Saving", None))
        self.label_14.setText(QCoreApplication.translate("settings_window", u"Branch / Directory", None))
        self.label_12.setText(QCoreApplication.translate("settings_window", u"Driver Repository URL", None))
        self.label_4.setText(QCoreApplication.translate("settings_window", u"# decimals:", None))
        self.label_10.setText(QCoreApplication.translate("settings_window", u"Databroker catalog-name", None))
        self.checkBox_autosave.setText(QCoreApplication.translate("settings_window", u"autosave on closing", None))
        self.checkBox_backup_before_run.setText(QCoreApplication.translate("settings_window", u"backup before run", None))
        self.checkBox_autosave_run.setText(QCoreApplication.translate("settings_window", u"autosave before run", None))
        self.checkBox_auto_check_updates.setText(QCoreApplication.translate("settings_window", u"automatically search for updates", None))
        self.label_17.setText(QCoreApplication.translate("settings_window", u"old logfile backups", None))
        self.label_15.setText(QCoreApplication.translate("settings_window", u"Log-Level", None))
        self.label_9.setText(QCoreApplication.translate("settings_window", u"Logging", None))
        self.label_16.setText(QCoreApplication.translate("settings_window", u"max. logfile size (MB)", None))
    # retranslateUi

