"""A module used to update CAMELS. The import of nomad_camels is necessary,
since otherwise it would not show in the imported distributions for reading its
current version."""

import os
import sys
import subprocess
import re
import importlib
import nomad_camels  # has to be imported for the distribution version number!
from nomad_camels.ui_widgets import warn_popup
from nomad_camels import graphics

from PySide6.QtWidgets import (
    QMessageBox,
    QDialog,
    QGridLayout,
    QTextEdit,
    QDialogButtonBox,
    QPushButton,
)
from PySide6.QtGui import QIcon


def get_version():
    """checks the installed version of nomad-camels and returns it."""
    try:
        import pkg_resources

        return pkg_resources.get_distribution("nomad-camels").version
    except (AttributeError, pkg_resources.DistributionNotFound):
        try:
            return nomad_camels.__version__
        except Exception:
            return None


def get_latest_version():
    """Checks the latest version of nomad-camels and returns it."""
    import requests

    try:
        response = requests.get("https://pypi.org/pypi/nomad-camels/json", timeout=5)
        response.raise_for_status()
        data = response.json()
        return data["info"]["version"]
    except requests.exceptions.RequestException:
        completed_process = subprocess.run(
            [sys.executable, "-m", "pip", "install", "nomad-camels==random"],
            capture_output=True,
            text=True,
        )
        stderr_output = completed_process.stderr
        versions_string = re.search(r"\(from versions: (.*)\)", stderr_output)
        if versions_string:
            versions = versions_string.group(1).replace(" ", "").split(",")
            latest_version = versions[-1]
            return latest_version
        else:
            return None


def update_camels():
    """Calls a subprocess that updates CAMELS via pip."""
    from pathlib import Path
    from nomad_camels.utility.load_save_functions import appdata_path

    if sys.platform == "win32":
        exe = Path(sys.executable).resolve()
        if not str(exe)[-5] == "w":
            exew = Path(f"{str(exe)[:-4]}w.exe")
        else:
            exew = exe
            exe = Path(f"{str(exew)[:-5]}.exe")
        s = f"{exe} -m pip install --no-cache-dir nomad-camels --upgrade\n"
        s += f"{exew} "
        for a in sys.argv:
            s += f"{a} "
        s += "\nexit"
        f_path = Path(os.path.join(appdata_path, "camels_update.bat"))
        with open(f_path, "w+") as f:
            f.write(s)
        subprocess.Popen(["start", "cmd", "/k", f_path], shell=True)
        sys.exit()
    elif sys.platform.startswith("linux") or sys.platform == "darwin":
        exe = Path(sys.executable).resolve()
        s = f"{exe} -m pip install --no-cache-dir nomad-camels --upgrade\n"
        s += f"{exe} "
        for a in sys.argv:
            s += f"'{a}' "
        f_path = Path(os.path.join(appdata_path, "camels_update.sh"))
        with open(f_path, "w+") as f:
            f.write("#!/bin/bash\n")
            f.write(s)
        subprocess.check_call(["chmod", "+x", str(f_path)])
        subprocess.Popen(["x-terminal-emulator", "-e", "bash", "-c", f_path])
        sys.exit()


def question_message_box(parent=None):
    """
    Retrieves the currently installed version and the available version of
    nomad-camels. If the are the same, a message is displayed, and function
    exits. Otherwise, a question-box appears, whether the user wants to install
    the newer version of CAMELS. If yes, first `update_camels` and then
    `restart_camels` are called.

    Parameters
    ----------
    parent : QWidget
        (Default value = None)
        The parent widget to be used for the message boxes.
    """
    installed_version = get_version()
    available_version = get_latest_version()
    if installed_version == available_version:
        warn_popup.WarnPopup(
            parent,
            "Your version of NOMAD CAMELS is already up to date",
            "Already up to date",
            info_icon=True,
        )
        return
    update_dialog = QMessageBox.question(
        parent,
        "Update NOMAD CAMELS",
        f"Your current version of NOMAD CAMELS is {installed_version}\n"
        f"The newest available version is {available_version}\n"
        f"Do you want to update now? (NOMAD CAMELS will have to restart)",
        QMessageBox.Yes | QMessageBox.No,
    )
    if update_dialog != QMessageBox.Yes:
        return
    update_camels()
    restart_camels(parent)


def restart_camels(parent=None, ask_restart=True):
    """Restarts CAMELS. If `ask_restart`, a question-messagebox appears first,
    to make sure the user actually wants to restart.

    Parameters
    ----------
    parent : QWidget
        (Default value = None)
        The parent widget to be used for the message boxes.
    ask_restart : bool
        (Default value = True)
        If True, the user is asked whether to restart CAMELS.
    """
    if ask_restart:
        restart_dialog = QMessageBox.question(
            parent,
            "Restart NOMAD CAMELS now?",
            "Do you want to restart NOMAD CAMELS now?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if restart_dialog != QMessageBox.Yes:
            return
    os.execl(sys.executable, sys.executable, *sys.argv)


def check_up_to_date():
    """Gets the installed and available version of CAMELS and checks whether
    they are the same. Returns the outcome as a bool."""
    installed_version = get_version()
    available_version = get_latest_version()
    return installed_version == available_version


def auto_update(parent):
    """
    Called if auto-update is set in the preferences. If the currently installed
    version is not up to date, `question_message_box` is called.

    Parameters
    ----------
    parent : QWidget
        (Default value = None)
        The parent widget to be used for the message boxes.
    """
    if not check_up_to_date():
        question_message_box(parent)


def show_release_notes():
    class MarkdownDialog(QDialog):
        def __init__(self, markdown_text):
            super().__init__()
            self.setWindowTitle("Changelog - NOMAD CAMELS")
            self.setWindowIcon(
                QIcon(str(importlib.resources.files(graphics) / "CAMELS_Icon.png"))
            )

            layout = QGridLayout(self)

            # Create a QTextEdit to display the Markdown content
            text_edit = QTextEdit(self)
            text_edit.setMarkdown(markdown_text)
            text_edit.setReadOnly(True)

            # Add OK button
            button_box = QDialogButtonBox(QDialogButtonBox.Ok, self)
            button_box.accepted.connect(self.accept)

            layout.addWidget(text_edit, 0, 0)
            layout.addWidget(button_box, 1, 0)

            self.setLayout(layout)
            self.setMinimumWidth(500)

    # read package's readme file
    try:
        readme = read_readme_from_metadata("nomad_camels")
    except:
        try:
            with importlib.resources.open_text("nomad_camels", "README.md") as f:
                readme = f.read()
        except (FileNotFoundError, ModuleNotFoundError):
            try:
                with open("README.md", "r") as f:
                    readme = f.read()
            except FileNotFoundError:
                try:
                    with open("../README.md", "r") as f:
                        readme = f.read()
                except FileNotFoundError:
                    return
    if readme:
        changelog = readme.split("# Changelog\n")[1]
        while changelog.startswith("\n"):
            changelog = changelog[1:]
        # newest_log = changelog.split("\n#")[0]
        dialog = MarkdownDialog(changelog)
        dialog.exec_()


def read_readme_from_metadata(package_name):
    try:
        # Get the metadata for the package
        metadata = importlib.metadata.metadata(package_name)
        # Extract the long description (which includes the README content)
        readme = metadata.get("Description", None)
        return readme
    except importlib.metadata.PackageNotFoundError:
        return None
