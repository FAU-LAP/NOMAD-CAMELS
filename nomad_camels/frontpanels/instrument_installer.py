import re
import subprocess
import importlib

from nomad_camels.gui.device_installer import Ui_Form
from PySide6.QtWidgets import QWidget, QTableWidgetItem, QCheckBox, QMessageBox
from PySide6.QtGui import QBrush, QColor, QFont
from PySide6.QtCore import Qt, QThread, Signal

import requests
import sys
import os

from nomad_camels.utility.variables_handling import get_color
from nomad_camels.utility import variables_handling, device_handling
from nomad_camels.ui_widgets.warn_popup import WarnPopup

if sys.version_info >= (3, 8):
    import importlib.metadata as importlib_metadata
else:
    import importlib_metadata

all_instr = {}
installed_instr = {}
last_repo = ''
last_branch = ''
last_dir = ''


def getInstalledDevices(force=False, return_packages=False):
    """Goes through the given device_driver_path and returns a list of
    the available devices.

    Parameters
    ----------
    force :
         (Default value = False)
    return_packages :
         (Default value = False)

    Returns
    -------

    """
    global installed_instr
    if installed_instr and not force and not return_packages:
        return installed_instr
    installed_instr.clear()
    for x in importlib_metadata.distributions():
        name = x.metadata['Name']
        version = x.version
        camels_driver_regex = r'^(nomad[-_]{1}camels[-_]{1}driver[-_]{1})(.*)$'
        if re.match(camels_driver_regex, name):
            installed_instr[name[20:].replace('-', '_')] = version
    packages = dict(device_handling.load_local_packages())
    for package in packages:
        installed_instr[package] = 'local'
    for instr in installed_instr:
        if instr not in packages:
            packages[instr] = importlib.import_module(f'nomad_camels_driver_{instr}.{instr}')
    if return_packages:
        return installed_instr, packages
    return installed_instr


def getAllDevices():
    """So far only returns the installed devices, should in future work
    with the online repository of drivers.

    Parameters
    ----------

    Returns
    -------

    """
    global all_instr, last_repo, last_branch, last_dir
    try:
        repo = variables_handling.preferences['driver_repository']
        branch = variables_handling.preferences['repo_branch']
        directory = variables_handling.preferences['repo_directory']
    except:
        repo, branch, directory = '', '', ''
    if all_instr and last_repo == repo and branch == last_branch and directory == last_dir:
        return all_instr
    last_repo, last_branch, last_dir = repo, branch, directory
    all_instr = {}
    try:
        repo_part = repo.split('.com/')[1].split('.git')[0]
        url = f'https://raw.githubusercontent.com/{repo_part}/{branch}/{directory}/driver_list.txt'
        devices_str = requests.get(url).text
    except:
        url = 'https://raw.githubusercontent.com/FAU-LAP/CAMELS_drivers/main/driver_list.txt'
        devices_str = requests.get(url).text
    warned = False
    for x in devices_str.splitlines():
        try:
            name, version = x.split('==')
        except:
            if not warned:
                WarnPopup(None, 'Could not read driver_list.txt from repo.\n'
                                'Check settings if repository and branch are correct.',
                          'No online-drivers found')
            warned = True
            continue
        all_instr[name.replace('-', '_')] = version
    return all_instr


bold_font = QFont()
bold_font.setBold(True)


class Instrument_Installer(Ui_Form, QWidget):
    """ """
    instruments_updated = Signal()

    """
    Parameters
    ----------
    parent : QWidget
        handed over to QWidget."""

    def __init__(self, active_instruments=None, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        self.active_instruments = active_instruments or {}

        self.device_table.setColumnCount(3)
        self.device_table.setHorizontalHeaderLabels(['instrument', 'available', 'installed'])
        self.device_table.verticalHeader().setVisible(False)

        self.all_devs = getAllDevices()
        self.installed_devs = getInstalledDevices()
        self.checkboxes = []

        self.disables = []
        for c in self.children():
            if c not in [self.progressBar, self.textEdit_device_info, self.label,
                         self.label_2]:
                self.disables.append(c)

        self.pushButton_sel_all.clicked.connect(self.select_all)
        self.pushButton_sel_none.clicked.connect(self.select_none)
        self.lineEdit_search_name.textChanged.connect(self.build_table)
        self.build_table()

        self.install_thread = None

        self.pushButton_install_update_selected.clicked.connect(self.install_selected)
        self.pushButton_uninstall.clicked.connect(self.uninstall_selected)
        self.pushButton_update_drivers.clicked.connect(self.update_installed)

    def checkBox_change(self, row):
        """

        Parameters
        ----------
        row :
            

        Returns
        -------

        """
        for i in range(3):
            checked = self.device_table.cellWidget(row, 0).isChecked()
            item = self.device_table.item(row, i)
            brush = QBrush(QColor(get_color('blue' if checked else 'white')))
            item.setBackground(brush)

    def get_checked_devs(self, ignore_version=False):
        """

        Parameters
        ----------
        ignore_version :
             (Default value = False)

        Returns
        -------

        """
        devs = []
        for box in self.checkboxes:
            if not box.isChecked():
                continue
            dev = box.text()
            if ignore_version:
                remove_dialog = QMessageBox.question(self, 'Uninstall instrument?',
                                                     f'You are trying to uninstall the instrument "{dev}", but it may still be in use.\nContinue?',
                                                     QMessageBox.Yes | QMessageBox.No)
                if remove_dialog != QMessageBox.Yes:
                    continue
                devs.append(dev)
                continue
            if dev in self.installed_devs and self.all_devs[dev] == self.installed_devs[dev]:
                continue
            devs.append(dev)
        return devs

    def update_installed(self):
        """ """
        devs = []
        for dev, version in self.installed_devs.items():
            if version != self.all_devs[dev]:
                devs.append(dev)
        self.install_thread = Install_Thread(devs, False, self)
        self.install_thread.info_step.connect(self.textEdit_device_info.append)
        self.install_thread.val_step.connect(self.progressBar.setValue)
        self.install_thread.finished.connect(self.thread_done)
        for c in self.disables:
            c.setEnabled(False)
        self.install_thread.start()

    def uninstall_selected(self):
        """ """
        self.install_selected(True)

    def install_selected(self, uninstall=False):
        """

        Parameters
        ----------
        uninstall :
             (Default value = False)

        Returns
        -------

        """
        self.textEdit_device_info.clear()
        devs = self.get_checked_devs(uninstall)
        self.install_thread = Install_Thread(devs, uninstall, self)
        self.install_thread.info_step.connect(self.textEdit_device_info.append)
        self.install_thread.val_step.connect(self.progressBar.setValue)
        self.install_thread.finished.connect(self.thread_done)
        for c in self.disables:
            c.setEnabled(False)
        self.setCursor(Qt.WaitCursor)
        self.install_thread.start()

    def thread_done(self):
        """ """
        for c in self.disables:
            c.setEnabled(True)
        self.setCursor(Qt.ArrowCursor)
        self.all_devs = getAllDevices()
        self.installed_devs = getInstalledDevices(True)
        self.build_table()
        self.instruments_updated.emit()

    def select_all(self):
        """ """
        for box in self.checkboxes:
            box.setChecked(True)

    def select_none(self):
        """ """
        for box in self.checkboxes:
            box.setChecked(False)

    def build_table(self):
        """ """
        search_text = self.lineEdit_search_name.text()
        self.checkboxes.clear()
        self.device_table.clear()
        self.device_table.setRowCount(0)
        self.device_table.setHorizontalHeaderLabels(['instrument', 'available', 'installed'])
        i = 0
        for dev in sorted(self.all_devs.keys()):
            if search_text.lower() not in dev.lower():
                continue
            self.device_table.setRowCount(i + 1)
            item = QTableWidgetItem()
            checkbox = QCheckBox(dev)
            self.checkboxes.append(checkbox)
            checkbox.stateChanged.connect(lambda a0, x=i: self.checkBox_change(x))
            self.device_table.setCellWidget(i, 0, checkbox)

            item_v = QTableWidgetItem(self.all_devs[dev])
            item_v.setFont(bold_font)
            item_v.setFlags(item_v.flags() & ~Qt.ItemIsEditable)
            inst_v = self.installed_devs[dev] if dev in self.installed_devs else ''
            item_inst = QTableWidgetItem(inst_v)
            if inst_v:
                brush = QBrush(QColor(
                    get_color('dark_green' if inst_v == self.all_devs[dev] else 'orange')))
                item_inst.setForeground(brush)
            item_inst.setFlags(item_inst.flags() & ~Qt.ItemIsEditable)
            item_inst.setFont(bold_font)
            self.device_table.setItem(i, 0, item)
            self.device_table.setItem(i, 1, item_v)
            self.device_table.setItem(i, 2, item_inst)
            i += 1


class Install_Thread(QThread):
    """ """
    info_step = Signal(str)
    val_step = Signal(int)

    def __init__(self, devs, uninstall=False, parent=None):
        super().__init__(parent=parent)
        self.devs = devs
        self.uninstall = uninstall

    def run(self):
        """ """
        n = len(self.devs)
        path = os.path.dirname(sys.executable)
        for i, dev in enumerate(self.devs):
            self.val_step.emit(i / n * 100)
            if self.uninstall:
                device_name = dev.replace("_", "-")
                flags = 0
                if os.name == 'nt':
                    flags = subprocess.CREATE_NO_WINDOW
                ret = subprocess.Popen([sys.executable, '-m', 'pip',
                                        'uninstall', '-y',
                                        f'nomad-camels-driver-{device_name}'],
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT,
                                       stdin=subprocess.PIPE,
                                       creationflags=flags)
                if ret.returncode:
                    raise OSError(f'Failed to uninstall nomad-camels-driver-{device_name}')
            else:
                device_name = dev.replace("_", "-")
                ret = install_instrument(device_name)
            for line in iter(ret.stdout.readline, b''):
                text = line.decode().rstrip()
                self.info_step.emit(text)
        getInstalledDevices(True)
        for i, dev in enumerate(self.devs):
            if self.uninstall and dev in installed_instr:
                WarnPopup(self,
                          f'Uninstall of {dev} failed!',
                          f'Uninstall of {dev} failed!')
            elif not self.uninstall and dev not in installed_instr:
                WarnPopup(self,
                          f'Installation of {dev} failed!',
                          f'Installation of {dev} failed!')
        self.val_step.emit(100)


def install_instrument(device_name):
    """

    Parameters
    ----------
    device_name :
        

    Returns
    -------

    """
    pypi_url = r'https://test.pypi.org/simple/'  # TODO Change to regular PyPi
    flags = 0
    if os.name == 'nt':
        flags = subprocess.CREATE_NO_WINDOW
    ret = subprocess.Popen([sys.executable, '-m', 'pip',
                            'install', '--no-cache-dir',
                            '--index-url', pypi_url,
                            '--extra-index-url',
                            'https://pypi.org/simple',
                            f'nomad-camels-driver-{device_name}'],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT,
                           stdin=subprocess.PIPE,
                           creationflags=flags)
    if ret.returncode:
        raise OSError(f'Failed to install nomad-camels-driver-{device_name}')
    return ret


if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication

    app = QApplication([])

    widge = Instrument_Installer()
    widge.show()
    app.exec()