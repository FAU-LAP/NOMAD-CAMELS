from PySide6.QtWidgets import QDialog, QStyleFactory, QMessageBox, QApplication
from PySide6.QtCore import Qt, QCoreApplication
from PySide6.QtGui import QKeyEvent
try:
    import qt_material

    QT_MATERIAL = True
except ImportError:
    QT_MATERIAL = False

from nomad_camels.gui.settings_window import Ui_settings_window
from nomad_camels.utility import load_save_functions
from nomad_camels.utility.theme_changing import change_theme
from nomad_camels.utility.logging_settings import log_levels
from nomad_camels.nomad_integration.nomad_communication import make_correct_url

import secrets
import hashlib
import sqlite3
import os


class Settings_Window(Ui_settings_window, QDialog):
    """Dialog to change the settings used in CAMELS."""

    def __init__(self, parent=None, settings=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Settings - NOMAD CAMELS")

        self.pathButton_config_path.set_path(load_save_functions.appdata_path)
        self.pathButton_config_path.select_directory = True

        themes = QStyleFactory.keys()
        themes.append("qt-material")
        self.comboBox_theme.addItems(themes)
        if "graphic_theme" in settings and settings["graphic_theme"] in themes:
            self.comboBox_theme.setCurrentText(settings["graphic_theme"])
        else:
            app = QCoreApplication.instance()
            self.comboBox_theme.setCurrentText(app.style().objectName())
        material_themes = []
        if QT_MATERIAL:
            for t in qt_material.list_themes():
                if t.startswith("light_"):
                    material_themes.append(t[6:-4])
        self.comboBox_material_theme.addItems(material_themes)
        if (
            "material_theme" in settings
            and settings["material_theme"] in material_themes
        ):
            self.comboBox_material_theme.setCurrentText(settings["material_theme"])
        if "dark_mode" in settings:
            self.checkBox_dark.setChecked(settings["dark_mode"])
        self.comboBox_theme.currentTextChanged.connect(self.change_theme)
        self.comboBox_material_theme.currentTextChanged.connect(self.change_theme)
        self.checkBox_dark.clicked.connect(self.change_theme)
        self.change_theme()

        self.pushButton_generate_Api_key.clicked.connect(self.generate_api_key)
        self.pushButton_copy_Api_key_clipboard.clicked.connect(self.copy_to_clipboard)
        self.pushButton_delete_Api_keys.clicked.connect(self.confirm_delete_api_keys)
        self.checkBox_enable_Api.clicked.connect(self.change_enable_API)

        standard_pref = load_save_functions.standard_pref

        if "autosave" in settings:
            self.checkBox_autosave.setChecked(settings["autosave"])
        else:
            self.checkBox_autosave.setChecked(standard_pref["autosave"])
        if "autosave_run" in settings:
            self.checkBox_autosave_run.setChecked(settings["autosave_run"])
        else:
            self.checkBox_autosave_run.setChecked(standard_pref["autosave_run"])
        if "backup_before_run" in settings:
            self.checkBox_backup_before_run.setChecked(settings["backup_before_run"])
        else:
            self.checkBox_backup_before_run.setChecked(
                standard_pref["backup_before_run"]
            )
        if "auto_check_updates" in settings:
            self.checkBox_auto_check_updates.setChecked(settings["auto_check_updates"])
        else:
            self.checkBox_auto_check_updates.setChecked(
                standard_pref["auto_check_updates"]
            )
        if "number_format" in settings:
            if settings["number_format"] == "plain":
                self.radioButton_plain_numbers.setChecked(True)
            elif settings["number_format"] == "scientific":
                self.radioButton_scientific.setChecked(True)
            else:
                self.radioButton_mixed.setChecked(True)
        else:
            self.radioButton_mixed.setChecked(True)
        if "mixed_from" in settings:
            self.spinBox_scientific_from.setValue(settings["mixed_from"])
        else:
            self.spinBox_scientific_from.setValue(standard_pref["mixed_from"])
        if "n_decimals" in settings:
            self.spinBox_n_decimals.setValue(settings["n_decimals"])
        else:
            self.spinBox_n_decimals.setValue(standard_pref["n_decimals"])
        if "py_files_path" in settings:
            self.pathButton_py_files.set_path(settings["py_files_path"])
        else:
            self.pathButton_py_files.set_path(standard_pref["py_files_path"])
        if "meas_files_path" in settings:
            self.pathButton_meas_files.set_path(settings["meas_files_path"])
        else:
            self.pathButton_meas_files.set_path(standard_pref["meas_files_path"])
        if "device_driver_path" in settings:
            self.pathButton_device_path.set_path(settings["device_driver_path"])
        else:
            self.pathButton_device_path.set_path(standard_pref["device_driver_path"])
        self.pathButton_py_files.select_directory = True
        self.pathButton_meas_files.select_directory = True
        self.pathButton_device_path.select_directory = True
        self.pathButton_extension_path.select_directory = True
        if "databroker_catalog_name" in settings:
            self.lineEdit_catalog_name.setText(settings["databroker_catalog_name"])
        else:
            self.lineEdit_catalog_name.setText(standard_pref["databroker_catalog_name"])
        if "number_databroker_files" in settings:
            self.spinBox_n_databroker_files.setValue(
                settings["number_databroker_files"]
            )
        else:
            self.spinBox_n_databroker_files.setValue(
                standard_pref["number_databroker_files"]
            )
        self.spinBox_n_databroker_files.setToolTip("0 files means keep all")
        if "play_camel_on_error" in settings:
            self.checkBox_play_camel_on_error.setChecked(
                settings["play_camel_on_error"]
            )
        else:
            self.checkBox_play_camel_on_error.setChecked(
                standard_pref["play_camel_on_error"]
            )

        for level in log_levels:
            self.comboBox_log_level.addItem(level)
        if "log_level" in settings:
            self.comboBox_log_level.setCurrentText(settings["log_level"])
        else:
            self.comboBox_log_level.setCurrentText(standard_pref["log_level"])
        if "logfile_size" in settings:
            self.spinBox_logfile_size.setValue(settings["logfile_size"])
        else:
            self.spinBox_logfile_size.setValue(standard_pref["logfile_size"])
        if "logfile_backups" in settings:
            self.spinBox_logfile_number.setValue(settings["logfile_backups"])
        else:
            self.spinBox_logfile_number.setValue(standard_pref["logfile_backups"])
        if "backups" in settings:
            if settings["backups"] == "all":
                self.radioButton_all_backups.setChecked(True)
            elif settings["backups"] == "number":
                self.radioButton_n_backups.setChecked(True)
            else:
                self.radioButton_smart_backups.setChecked(True)

        if "NOMAD_URL" in settings:
            self.lineEdit_oasis.setText(settings["NOMAD_URL"])
        else:
            self.lineEdit_oasis.setText(standard_pref["NOMAD_URL"])

        self.radioButton_mixed.clicked.connect(self.number_change)
        self.radioButton_plain_numbers.clicked.connect(self.number_change)
        self.radioButton_scientific.clicked.connect(self.number_change)
        if "extensions" in settings:
            self.extensions = settings["extensions"]
        else:
            self.extensions = standard_pref["extensions"]
        if "extension_path" in settings:
            self.pathButton_extension_path.set_path(settings["extension_path"])
        else:
            self.pathButton_extension_path.set_path(standard_pref["extension_path"])

        if "new_file_each_run" in settings:
            self.checkBox_new_file_each_run.setChecked(settings["new_file_each_run"])
        else:
            self.checkBox_new_file_each_run.setChecked(
                standard_pref["new_file_each_run"]
            )

        if "password_protection" in settings:
            self.checkBox_password.setChecked(settings["password_protection"])
        else:
            self.checkBox_password.setChecked(standard_pref["password_protection"])
        self.password_hash = ""
        if "password_hash" in settings:
            self.password_hash = settings["password_hash"]
        if "enable_API" in settings:
            self.checkBox_enable_Api.setChecked(settings["enable_API"])
            # Disable the generate and delete API keys push buttons if the API is disenabled
            if not self.checkBox_enable_Api.isChecked():
                self.pushButton_generate_Api_key.setEnabled(False)
                self.pushButton_copy_Api_key_clipboard.setEnabled(False)
                self.pushButton_delete_Api_keys.setEnabled(False)
        if "API_port" in settings:
            self.lineEdit_api_port.setText(settings["API_port"])
        self.pushButton_API_docu.clicked.connect(self.open_api_docu)
        self.pushButton_API_docu.setToolTip(
            "If the page does not load, accept your settings and try again. The API server might not be started yet."
        )

    def autosave_run_change(self):
        on = self.checkBox_autosave_run.isChecked()
        self.checkBox_backup_before_run.setEnabled(on)

    def number_change(self):
        mixed = self.radioButton_mixed.isChecked()
        self.spinBox_n_decimals.setEnabled(mixed)

    def accept(self):
        if self.password_hash:
            from nomad_camels.utility.password_widgets import Password_Dialog

            pw = Password_Dialog(parent=self, compare_hash=self.password_hash)
            if not pw.exec():
                return
        if self.checkBox_password.isChecked() and self.password_hash:
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Change Password?")
            msg_box.setText("Do you want to change the password?")
            msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            if msg_box.exec() != QMessageBox.Yes:
                super().accept()
        if self.checkBox_password.isChecked() and not self.password_hash:
            from nomad_camels.utility import password_widgets

            pw = password_widgets.Password_Dialog(parent=self, double_pass=True)
            if not pw.exec():
                return
            self.password_hash = password_widgets.hash_password(pw.password)

        super().accept()

    def change_theme(self):
        """ """
        theme = self.comboBox_theme.currentText()
        mat = theme == "qt-material"
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
        load_save_functions.update_config_path(self.pathButton_config_path.get_path())
        if not self.checkBox_password.isChecked():
            self.password_hash = None
        if self.radioButton_plain_numbers.isChecked():
            numbers = "plain"
        elif self.radioButton_scientific.isChecked():
            numbers = "scientific"
        else:
            numbers = "mixed"
        if self.radioButton_all_backups.isChecked():
            backups = "all"
        elif self.radioButton_n_backups.isChecked():
            backups = "number"
        else:
            backups = "smart"
        return {
            "autosave": self.checkBox_autosave.isChecked(),
            "autosave_run": self.checkBox_autosave_run.isChecked(),
            "backup_before_run": self.checkBox_backup_before_run.isChecked(),
            "dark_mode": self.checkBox_dark.isChecked(),
            "auto_check_updates": self.checkBox_auto_check_updates.isChecked(),
            "graphic_theme": self.comboBox_theme.currentText(),
            "material_theme": self.comboBox_material_theme.currentText(),
            "n_decimals": self.spinBox_n_decimals.value(),
            "number_format": numbers,
            "mixed_from": self.spinBox_scientific_from.value(),
            "py_files_path": self.pathButton_py_files.get_path(),
            "meas_files_path": self.pathButton_meas_files.get_path(),
            "device_driver_path": self.pathButton_device_path.get_path(),
            "databroker_catalog_name": self.lineEdit_catalog_name.text(),
            "number_databroker_files": self.spinBox_n_databroker_files.value(),
            "play_camel_on_error": self.checkBox_play_camel_on_error.isChecked(),
            "log_level": self.comboBox_log_level.currentText(),
            "logfile_size": self.spinBox_logfile_size.value(),
            "logfile_backups": self.spinBox_logfile_number.value(),
            "backups": backups,
            "NOMAD_URL": make_correct_url(self.lineEdit_oasis.text()),
            "password_protection": self.checkBox_password.isChecked(),
            "password_hash": self.password_hash,
            "new_file_each_run": self.checkBox_new_file_each_run.isChecked(),
            "extensions": self.extensions,
            "extension_path": self.pathButton_extension_path.get_path(),
            "enable_API": self.checkBox_enable_Api.isChecked(),
            "API_port": self.lineEdit_api_port.text(),
        }

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

    def generate_api_key(self):
        # Generate a random API key (example: 40 characters long)
        api_key = secrets.token_urlsafe(40)
        self.Api_key_lineEdit.setText(api_key)
        # Save hash of the API key to the SQlite database file
        # Database setup
        data_base_path = os.path.join(load_save_functions.appdata_path, "CAMELS_API.db")
        conn = sqlite3.connect(data_base_path, check_same_thread=False)
        c = conn.cursor()
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS api_keys (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """
        )
        conn.commit()
        # Store hashed API Key
        store_api_key(api_key, conn)
        conn.close()
        # Disable the "Generate API Key" button and enable the "Copy to Clipboard" button
        self.pushButton_generate_Api_key.setEnabled(False)
        self.pushButton_copy_Api_key_clipboard.setEnabled(True)
        # Turn the background of the copy_api_key_clipboard button to green
        self.pushButton_copy_Api_key_clipboard.setStyleSheet(
            "background-color: #0db002"
        )

    def confirm_delete_api_keys(self):
        reply = QMessageBox.question(
            self,
            "Confirm Action",
            "Are you sure you want to delete ALL API keys?\nYou can not reverse this action!\nIt will break all applications using API keys to communicate with CAMELS!",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            data_base_path = os.path.join(
                load_save_functions.appdata_path, "CAMELS_API.db"
            )
            conn = sqlite3.connect(data_base_path, check_same_thread=False)
            c = conn.cursor()
            # SQL statement to drop the api_keys table
            c.execute("DROP TABLE IF EXISTS api_keys")
            conn.commit()
            conn.close()
        else:
            pass

    def copy_to_clipboard(self):
        api_key = self.Api_key_lineEdit.text()
        if api_key:
            clipboard = QApplication.clipboard()
            clipboard.setText(api_key)
            QMessageBox.information(self, "Copied", "API Key copied to clipboard!")
        else:
            QMessageBox.warning(self, "Warning", "No API Key to copy!")

    def change_enable_API(self):
        if self.checkBox_enable_Api.isChecked():
            if self.check_if_api_modules_are_available():
                self.pushButton_generate_Api_key.setEnabled(True)
                self.pushButton_delete_Api_keys.setEnabled(True)
                self.pushButton_API_docu.setEnabled(True)
            else:
                self.checkBox_enable_Api.setChecked(False)
        else:
            self.pushButton_generate_Api_key.setEnabled(False)
            self.pushButton_copy_Api_key_clipboard.setEnabled(False)
            self.pushButton_delete_Api_keys.setEnabled(False)
            self.pushButton_API_docu.setEnabled(False)
            self.pushButton_copy_Api_key_clipboard.setStyleSheet("")

    def open_api_docu(self):
        from nomad_camels.utility import variables_handling

        link = f"http://127.0.0.1:{self.lineEdit_api_port.text()}/docs"
        variables_handling.open_link(link)

    def check_if_api_modules_are_available(self):
        # Function to check if a module is installed.
        # List the required modules.
        required_modules = ["fastapi", "uvicorn", "httpx"]

        # Determine which modules are missing.
        missing_modules = [mod for mod in required_modules if not is_module_available(mod)]

        if missing_modules:
            # Create the message to warn the user.
            msg = (
                f"The following modules are required: {', '.join(missing_modules)}.\n\n"
                "These modules may take a few seconds to install. You only need to do this once.\n"
                "Do you want to install them now?"
            )

            # Show a question message box.
            reply_update_modules = QMessageBox.question(
                None,
                "Install Required Modules",
                msg,
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )

            if reply_update_modules == QMessageBox.Yes:
                try:
                    import sys
                    import subprocess

                    # Build the pip install command.
                    try:
                        command = [
                            sys.executable,
                            "-m",
                            "pip",
                            "install",
                            "nomad-camels[api]",
                        ]
                        subprocess.check_call(command)
                        missing_modules = [
                            mod for mod in required_modules if not is_module_available(mod)
                        ]
                        if missing_modules:
                            raise Exception("Failed to install nomad-camels[api]")
                        return True

                    except Exception as e:
                        print(e)
                        command = [sys.executable, "-m", "pip", "install"] + missing_modules
                    # Optionally, you might show another popup or a console message indicating progress.
                    subprocess.check_call(command)
                    QMessageBox.information(
                        None,
                        "Installation Complete",
                        "The required modules have been installed.\nYou can now start the API server and use the API.",
                    )
                    return True
                except Exception as e:
                    QMessageBox.critical(
                        None,
                        "Installation Failed",
                        f"An error occurred during installation:\n{str(e)}",
                    )
                    return False
                # Exit the application (or you could try to continue, if that makes sense in your context).
            else:
                QMessageBox.warning(
                    None,
                    "Modules Missing",
                    "You can not use the API without the required modules!",
                )
                return False



def hash_api_key(api_key):
    return hashlib.sha256(api_key.encode()).hexdigest()


# Store API Key
def store_api_key(api_key, conn):
    hashed_key = hash_api_key(api_key)
    c = conn.cursor()
    c.execute("INSERT INTO api_keys (key) VALUES (?)", (hashed_key,))
    conn.commit()

def is_module_available(module_name):
    try:
        __import__(module_name)
        return True
    except ImportError:
        return False


