import sys
import os
import requests
import re
import importlib
import importlib_metadata
import pathlib
import pkg_resources
import subprocess

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
from nomad_camels.ui_widgets.warn_popup import WarnPopup
from nomad_camels.utility import variables_handling
from nomad_camels.main_classes.device_class import Simple_Config_Sub

from PySide6.QtWidgets import (
    QDialog,
    QTableWidget,
    QTableWidgetItem,
    QLineEdit,
    QGridLayout,
    QPushButton,
    QCheckBox,
    QSplitter,
    QTextBrowser,
    QLabel,
    QWidget,
    QDialogButtonBox,
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont

url = "https://raw.githubusercontent.com/FAU-LAP/CAMELS_extensions/extension_list/extension_list.txt"
repo_url = "https://raw.githubusercontent.com/FAU-LAP/CAMELS_extensions/main"
camels_extension_regex = r"^(nomad[-_]{1}camels[-_]{1}extension[-_]{1})(.*)$"

bold_font = QFont()
bold_font.setBold(True)


def get_online_extensions():
    """Returns a list of all extensions."""
    online_extensions = {}
    try:
        extension_str = requests.get(url).text
        for x in extension_str.splitlines():
            if "==" not in x:
                continue
            name, version = x.split("==")
            online_extensions[name.replace("-", "_")] = version
    except:
        WarnPopup(
            None,
            "Could not (completely) read extension_list.txt from repo.\n"
            "Check internet connectivity.",
            "No extensions found online",
        )
    return online_extensions


def get_installed_extensions():
    """Returns a list of all installed extensions."""
    installed_extensions = {}
    for x in importlib_metadata.distributions():
        name = x.metadata["Name"]
        version = x.version
        if re.match(camels_extension_regex, name, re.IGNORECASE):
            installed_extensions[name[23:].replace("-", "_")] = version
    return installed_extensions


def get_local_extensions():
    """Returns a list of all local extensions."""
    local_extensions = {}
    if "extension_path" in variables_handling.preferences:
        local_extension_path = variables_handling.preferences["extension_path"]
    else:
        from nomad_camels.utility.load_save_functions import standard_pref

        local_extension_path = standard_pref["extension_path"]
    if not os.path.isdir(local_extension_path):
        return local_extensions
    sys.path.append(local_extension_path)
    for f in pathlib.Path(local_extension_path).rglob("*"):
        match = re.match(camels_extension_regex, f.name, re.IGNORECASE)
        if match:
            try:
                sys.path.append(str(f.parent))
                package = importlib.import_module(match.group(0))
                name = match.group(2)
                version = package.EXTENSION_CONFIG["version"]
                local_extensions[name] = version
            except Exception as e:
                print(f, e)
    return local_extensions


def get_readme_text(extension):
    text_url = f"{repo_url}/{extension}/README.md"
    return requests.get(text_url).text


def get_license_text(extension):
    text_url = f"{repo_url}/{extension}/LICENSE.txt"
    return requests.get(text_url).text


class Extension_Manager(QDialog):
    def __init__(self, preferences, parent=None):
        super().__init__(parent=parent)
        self.actual_preferences = preferences
        self.preferences = dict(preferences)
        self.setWindowTitle("Extension Manager - NOMAD CAMELS")
        if "extensions" not in self.preferences:
            self.preferences["extensions"] = []
        self.extensions = self.preferences["extensions"]
        if "extension_settings" not in self.preferences:
            self.preferences["extension_settings"] = {}
        self.extension_data = self.preferences["extension_settings"]

        self.online_extensions = get_online_extensions()
        self.local_extensions = get_local_extensions()
        self.installed_extensions = get_installed_extensions()

        self.extension_table = QTableWidget()
        self.extension_table.setColumnCount(3)
        self.extension_table.setHorizontalHeaderLabels(["Name", "Version", "Installed"])
        self.extension_table.verticalHeader().setVisible(False)

        self.lineEdit_search_name = QLineEdit()
        self.lineEdit_search_name.setPlaceholderText("Search...")
        self.lineEdit_search_name.textChanged.connect(self.build_table)

        self.show_hide_info_button = QPushButton("Show Info")
        self.info_hidden = True
        self.show_hide_info_button.clicked.connect(self.show_hide_info)

        self.selection_label = QLabel("Extension:")
        self.selection_label.setFont(bold_font)

        self.install_button = QPushButton("Install / Update")
        self.install_button.clicked.connect(self.install_selected)

        self.uninstall_button = QPushButton("Uninstall")
        self.uninstall_button.clicked.connect(
            lambda: self.install_selected(uninstall=True)
        )

        self.checkbox_active = QCheckBox("extension active")

        self.info_widget = Info_Widget()

        self.extension_table.clicked.connect(self.table_click)
        self.config_widget = QWidget()

        self.dialog_buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        self.dialog_buttons.accepted.connect(self.accept)
        self.dialog_buttons.rejected.connect(self.reject)

        layout = QGridLayout()
        layout.addWidget(self.lineEdit_search_name, 0, 0)
        layout.addWidget(self.extension_table, 1, 0, 5, 1)
        layout.addWidget(self.selection_label, 0, 1)
        layout.addWidget(self.install_button, 2, 1)
        layout.addWidget(self.uninstall_button, 3, 1)
        layout.addWidget(self.show_hide_info_button, 1, 1)
        layout.addWidget(self.checkbox_active, 4, 1)
        layout.addWidget(self.config_widget, 5, 1)
        layout.addWidget(self.info_widget, 0, 2, 6, 1)
        layout.addWidget(self.dialog_buttons, 6, 0, 1, 3)
        self.setLayout(layout)

        self.current_extension = None

        self.install_thread = None
        self.build_table()
        self.table_click()

    def propagate_exception(self, e):
        raise e

    def install_selected(self, uninstall=False):
        self.setEnabled(False)
        self.setCursor(Qt.WaitCursor)
        ind = self.extension_table.selectedIndexes()[0]
        ext = self.extension_table.item(ind.row(), 0).text()
        self.install_thread = Install_Thread(ext, uninstall=uninstall)
        self.install_thread.exception_signal.connect(self.propagate_exception)
        self.install_thread.finished.connect(self.build_table)
        self.install_thread.start()

    def show_hide_info(self):
        if self.info_hidden:
            self.info_widget.setHidden(False)
            self.show_hide_info_button.setText("Hide Info")
        else:
            self.info_widget.setHidden(True)
            self.show_hide_info_button.setText("Show Info")
        self.info_hidden = not self.info_hidden
        self.table_click()

    def update_config(self):
        try:
            ind = self.extension_table.selectedIndexes()[0]
        except:
            return
        ext = self.extension_table.item(ind.row(), 0).text()
        if self.current_extension:
            self.extension_data[self.current_extension] = (
                self.config_widget.get_config()
            )
        package = importlib.import_module(f"nomad_camels_extension_{ext}")
        # if checkbox checked, add to self.extensions if not already there
        name = f'nomad_camels_extension_{ext.replace("-", "_")}'
        if self.checkbox_active.isChecked():
            if name not in self.extensions:
                self.extensions.append(name)
        # if checkbox unchecked, remove from self.extensions if there
        else:
            if name in self.extensions:
                self.extensions.remove(name)
        if "settings" not in package.EXTENSION_CONFIG:
            return
        settings = package.EXTENSION_CONFIG["settings"]
        if ext in self.extension_data:
            settings.update(self.extension_data[ext])
        config_old = self.config_widget
        self.config_widget = Simple_Config_Sub(config_dict=settings)
        self.layout().replaceWidget(config_old, self.config_widget)
        config_old.deleteLater()

    def table_click(self):
        self.setCursor(Qt.WaitCursor)
        try:
            ind = self.extension_table.selectedIndexes()[0]
            ext = self.extension_table.item(ind.row(), 0).text()
            installed = ext in self.installed_extensions
            local = ext in self.local_extensions
            if local:
                self.selection_label.setText(f"Local extension: {ext}")
            else:
                self.selection_label.setText(f"Extension: {ext}")
            name = f'nomad_camels_extension_{ext.replace("-", "_")}'
            self.checkbox_active.setChecked(name in self.extensions)
            if local or installed:
                self.update_config()
            self.install_button.setEnabled(not local)
            self.uninstall_button.setEnabled(installed and not local)
            self.checkbox_active.setEnabled(installed or local)
            self.show_hide_info_button.setEnabled(True)
            if not self.info_hidden:
                self.info_widget.update_texts(ext)
            self.current_extension = ext
        except Exception as e:
            self.info_widget.setHidden(True)
            self.install_button.setEnabled(False)
            self.uninstall_button.setEnabled(False)
            self.checkbox_active.setEnabled(False)
            self.selection_label.setText("Extension:")
            self.show_hide_info_button.setEnabled(False)
            print(e)
        finally:
            self.adjustSize()
            self.setCursor(Qt.ArrowCursor)

    def build_table(self):
        self.setEnabled(True)
        self.setCursor(Qt.WaitCursor)
        search_text = self.lineEdit_search_name.text()
        self.extension_table.clear()
        self.extension_table.setRowCount(0)
        for i, ext in enumerate(sorted(self.online_extensions.keys())):
            if search_text.lower() not in ext.lower():
                continue
            self.extension_table.insertRow(i)
            item = QTableWidgetItem(ext)
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            self.extension_table.setItem(i, 0, item)
            item = QTableWidgetItem(self.online_extensions[ext])
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            self.extension_table.setItem(i, 1, item)
            if ext in self.installed_extensions:
                item = QTableWidgetItem(self.installed_extensions[ext])
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.extension_table.setItem(i, 2, item)
            elif ext in self.local_extensions:
                item = QTableWidgetItem(self.local_extensions[ext])
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.extension_table.setItem(i, 2, item)
        for i, ext in enumerate(sorted(self.local_extensions.keys())):
            if search_text.lower() not in ext.lower():
                continue
            if ext in self.online_extensions:
                continue
            self.extension_table.insertRow(i)
            item = QTableWidgetItem(ext)
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            self.extension_table.setItem(i, 0, item)
            item = QTableWidgetItem(self.local_extensions[ext])
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            self.extension_table.setItem(i, 1, item)
            if ext in self.installed_extensions:
                item = QTableWidgetItem(self.installed_extensions[ext])
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.extension_table.setItem(i, 2, item)
        self.extension_table.resizeColumnsToContents()
        self.setCursor(Qt.ArrowCursor)

    def accept(self):
        self.update_config()
        self.actual_preferences.update(self.preferences)
        super().accept()


class Info_Widget(QSplitter):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setOrientation(Qt.Orientation.Horizontal)

        self.info_text = QTextBrowser()
        self.info_text.setOpenExternalLinks(True)
        self.info_text.setTextInteractionFlags(
            Qt.TextSelectableByKeyboard
            | Qt.TextSelectableByMouse
            | Qt.LinksAccessibleByMouse
        )
        self.addWidget(self.info_text)

        self.license_text = QTextBrowser()
        self.license_text.setOpenExternalLinks(True)
        self.license_text.setTextInteractionFlags(
            Qt.TextSelectableByKeyboard
            | Qt.TextSelectableByMouse
            | Qt.LinksAccessibleByMouse
        )
        self.addWidget(self.license_text)
        self.info = False

        self.setContentsMargins(0, 0, 0, 0)

    def update_texts(self, extension):
        self.info = False
        hidden = True
        try:
            self.info_text.setHidden(True)
            self.info_text.clear()
            try:
                meta = importlib_metadata.metadata(
                    f"nomad_camels_extension_{extension}"
                )
                text = meta.json["description"]
            except:
                text = get_readme_text(extension)
            self.info_text.setMarkdown(text)
            self.info_text.setHidden(False)
            hidden = False
        except:
            pass
        try:
            self.license_text.setHidden(True)
            self.license_text.clear()
            try:
                text = ""
                for p in pkg_resources.working_set:
                    if not p.key.startswith(
                        f'nomad-camels-driver-{extension.replace("_", "-")}'
                    ):
                        continue
                    lic = p.get_metadata_lines("LICENSE.txt")
                    for l in lic:
                        text += f"{l}\n"
                    break
                if not text:
                    raise Exception("")
                self.license_text.setText(text)
            except:
                text = get_license_text(extension)
                self.license_text.setMarkdown(text)
            self.license_text.setHidden(False)
            hidden = False
        except:
            pass
        self.info = not hidden
        self.setHidden(hidden)


class Install_Thread(QThread):
    exception_signal = Signal(Exception)

    def __init__(self, extension, uninstall=False, parent=None):
        super().__init__(parent=parent)
        self.extension = extension
        self.uninstall = uninstall

    def run(self):
        try:
            name = self.extension.replace("_", "-")
            flags = 0
            if os.name == "nt":
                flags = subprocess.CREATE_NO_WINDOW
            if self.uninstall:
                ret = subprocess.Popen(
                    [
                        sys.executable,
                        "-m",
                        "pip",
                        "uninstall",
                        "-y",
                        f"nomad-camels-extension-{name}",
                    ],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    creationflags=flags,
                )
            else:
                ret = subprocess.Popen(
                    [
                        sys.executable,
                        "-m",
                        "pip",
                        "install",
                        f"nomad-camels-extension-{name}",
                    ],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    creationflags=flags,
                )
            for line in iter(ret.stdout.readline, b""):
                text = line.decode().rstrip()
                print(text)
            errs = ret.stderr.read().decode()
            if ret.returncode or errs:
                self.exception_signal.emit(Exception(errs))
        except Exception as e:
            self.exception_signal.emit(e)


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication

    app = QApplication([])

    widge = Extension_Manager({})
    widge.show()
    app.exec()
