from PySide6.QtWidgets import QDialog, QStyleFactory
from PySide6.QtCore import Qt, QCoreApplication
from PySide6.QtGui import QKeyEvent
import qt_material

from nomad_camels.gui.settings_window import Ui_settings_window
from nomad_camels.utility.load_save_functions import standard_pref
from nomad_camels.utility.theme_changing import change_theme

class Settings_Window(Ui_settings_window, QDialog):
    """Dialog to change the settings used in CAMELS."""
    def __init__(self, parent=None, settings=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('NOMAD-CAMELS - Settings')
        # if 'dark_mode' in settings:
        #     self.checkBox_dark_mode.setChecked(settings['dark_mode'])
        # else:
        #     self.checkBox_dark_mode.setChecked(standard_pref['dark_mode'])
        themes = QStyleFactory.keys()
        themes.append('qt-material')
        self.comboBox_theme.addItems(themes)
        if 'graphic_theme' in settings and settings['graphic_theme'] in themes:
            self.comboBox_theme.setCurrentText(settings['graphic_theme'])
        else:
            app = QCoreApplication.instance()
            self.comboBox_theme.setCurrentText(app.style().objectName())
        material_themes = []
        for t in qt_material.list_themes():
            if t.startswith('light_'):
                material_themes.append(t[6:-4])
        self.comboBox_material_theme.addItems(material_themes)
        if 'material_theme' in settings and settings['material_theme'] in themes:
            self.comboBox_material_theme.setCurrentText(settings['material_theme'])
        if 'dark_mode' in settings:
            self.checkBox_dark.setChecked(settings['dark_mode'])
        self.comboBox_theme.currentTextChanged.connect(self.change_theme)
        self.comboBox_material_theme.currentTextChanged.connect(self.change_theme)
        self.checkBox_dark.clicked.connect(self.change_theme)
        self.change_theme()
        if 'autosave' in settings:
            self.checkBox_autosave.setChecked(settings['autosave'])
        else:
            self.checkBox_autosave.setChecked(standard_pref['autosave'])
        if 'autosave_run' in settings:
            self.checkBox_autosave_run.setChecked(settings['autosave_run'])
        else:
            self.checkBox_autosave_run.setChecked(standard_pref['autosave_run'])
        if 'backup_before_run' in settings:
            self.checkBox_backup_before_run.setChecked(settings['backup_before_run'])
        else:
            self.checkBox_backup_before_run.setChecked(standard_pref['backup_before_run'])
        if 'auto_check_updates' in settings:
            self.checkBox_auto_check_updates.setChecked(settings['auto_check_updates'])
        else:
            self.checkBox_auto_check_updates.setChecked(standard_pref['auto_check_updates'])
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
        self.pathButton_py_files.select_directory = True
        self.pathButton_meas_files.select_directory = True
        self.pathButton_device_path.select_directory = True
        if 'databroker_catalog_name' in settings:
            self.lineEdit_catalog_name.setText(settings['databroker_catalog_name'])
        else:
            self.lineEdit_catalog_name.setText(standard_pref['databroker_catalog_name'])
        if 'play_camel_on_error' in settings:
            self.checkBox_play_camel_on_error.setChecked(settings['play_camel_on_error'])
        else:
            self.checkBox_play_camel_on_error.setChecked(standard_pref['play_camel_on_error'])
        if 'driver_repository' in settings:
            self.lineEdit_repo.setText(settings['driver_repository'])
        else:
            self.lineEdit_repo.setText(standard_pref['driver_repository'])
        if 'repo_directory' in settings:
            self.lineEdit_directory.setText(settings['repo_directory'])
        else:
            self.lineEdit_directory.setText(standard_pref['repo_directory'])
        if 'repo_branch' in settings:
            self.lineEdit_branch.setText(settings['repo_branch'])
        else:
            self.lineEdit_branch.setText(standard_pref['repo_branch'])

        self.radioButton_mixed.clicked.connect(self.number_change)
        self.radioButton_plain_numbers.clicked.connect(self.number_change)
        self.radioButton_scientific.clicked.connect(self.number_change)


    def autosave_run_change(self):
        on = self.checkBox_autosave_run.isChecked()
        self.checkBox_backup_before_run.setEnabled(on)


    def number_change(self):
        mixed = self.radioButton_mixed.isChecked()
        self.spinBox_n_decimals.setEnabled(mixed)



    def change_theme(self):
        """ """
        theme = self.comboBox_theme.currentText()
        mat = theme == 'qt-material'
        self.comboBox_material_theme.setEnabled(mat)
        material_theme = self.comboBox_material_theme.currentText()
        dark_mode = self.checkBox_dark.isChecked()
        change_theme(theme, material_theme=material_theme, dark_mode=dark_mode)

    def get_settings(self):
        """Reading all the UI-elements to get the selected settings,
        then returning those as a dictionary.

        Parameters
        ----------

        Returns
        -------

        """
        if self.radioButton_plain_numbers.isChecked():
            numbers = 'plain'
        elif self.radioButton_scientific.isChecked():
            numbers = 'scientific'
        else:
            numbers = 'mixed'
        return {'autosave': self.checkBox_autosave.isChecked(),
                'autosave_run': self.checkBox_autosave_run.isChecked(),
                'backup_before_run': self.checkBox_backup_before_run.isChecked(),
                'dark_mode': self.checkBox_dark.isChecked(),
                'auto_check_updates': self.checkBox_auto_check_updates.isChecked(),
                'graphic_theme': self.comboBox_theme.currentText(),
                'material_theme': self.comboBox_material_theme.currentText(),
                'n_decimals': self.spinBox_n_decimals.value(),
                'number_format': numbers,
                'mixed_from': self.spinBox_scientific_from.value(),
                'py_files_path': self.pathButton_py_files.get_path(),
                'meas_files_path': self.pathButton_meas_files.get_path(),
                'device_driver_path': self.pathButton_device_path.get_path(),
                'databroker_catalog_name': self.lineEdit_catalog_name.text(),
                'driver_repository': self.lineEdit_repo.text(),
                'repo_branch': self.lineEdit_branch.text(),
                'repo_directory': self.lineEdit_directory.text(),
                'play_camel_on_error': self.checkBox_play_camel_on_error.isChecked()}


    def keyPressEvent(self, a0: QKeyEvent) -> None:
        """Overwrites the keyPressEvent of the QDialog so that it does
        not close when pressing Enter/Return.

        Parameters
        ----------
        a0: QKeyEvent :
            

        Returns
        -------

        """
        if a0.key() == Qt.Key_Enter or a0.key() == Qt.Key_Return:
            return
        super().keyPressEvent(a0)
