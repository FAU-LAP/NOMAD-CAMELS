from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent

from gui.settings_window import Ui_settings_window
from utility.load_save_functions import standard_pref

class Settings_Window(QDialog, Ui_settings_window):
    def __init__(self, parent=None, settings=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('CAMELS - Settings')
        if 'dark_mode' in settings:
            self.checkBox_dark_mode.setChecked(settings['dark_mode'])
        else:
            self.checkBox_dark_mode.setChecked(standard_pref['dark_mode'])
        if 'autosave' in settings:
            self.checkBox_autosave.setChecked(settings['autosave'])
        else:
            self.checkBox_autosave.setChecked(standard_pref['autosave'])
        if 'number_format' in settings:
            if settings['number_format'] == 'plain':
                self.radioButton_plain_numbers.setChecked(True)
            elif settings['number_format'] == 'scientific':
                self.radioButton_scientific.setChecked(True)
            else:
                self.radioButton_mixed.setChecked(True)
        else:
            self.radioButton_mixed.setChecked(True)
        if 'mixed_from' in settings:
            self.spinBox_scientific_from.setValue(settings['mixed_from'])
        else:
            self.spinBox_scientific_from.setValue(standard_pref['mixed_from'])
        if 'n_decimals' in settings:
            self.spinBox_n_decimals.setValue(settings['n_decimals'])
        else:
            self.spinBox_n_decimals.setValue(standard_pref['n_decimals'])
        if 'py_files_path' in settings:
            self.pathButton_py_files.set_path(settings['py_files_path'])
        else:
            self.pathButton_py_files.set_path(standard_pref['py_files_path'])
        if 'meas_files_path' in settings:
            self.pathButton_meas_files.set_path(settings['meas_files_path'])
        else:
            self.pathButton_meas_files.set_path(standard_pref['meas_files_path'])
        if 'device_driver_path' in settings:
            self.pathButton_device_path.set_path(settings['device_driver_path'])
        else:
            self.pathButton_device_path.set_path(standard_pref['device_driver_path'])

    def get_settings(self):
        if self.radioButton_plain_numbers.isChecked():
            numbers = 'plain'
        elif self.radioButton_scientific.isChecked():
            numbers = 'scientific'
        else:
            numbers = 'mixed'
        return {'dark_mode': self.checkBox_dark_mode.checkState(),
                'autosave': self.checkBox_autosave.checkState(),
                'n_decimals': self.spinBox_n_decimals.value(),
                'number_format': numbers,
                'mixed_from': self.spinBox_scientific_from.value(),
                'py_files_path': self.pathButton_py_files.get_path(),
                'meas_files_path': self.pathButton_meas_files.get_path(),
                'device_driver_path': self.pathButton_device_path.get_path()}


    def keyPressEvent(self, a0: QKeyEvent) -> None:
        """Overwrites the keyPressEvent of the QDialog so that it does not close when pressing Enter/Return."""
        if a0.key() == Qt.Key_Enter or a0.key() == Qt.Key_Return:
            return
        super().keyPressEvent(a0)