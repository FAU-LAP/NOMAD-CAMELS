import os
import sys
import subprocess
from importlib.metadata import distributions
import nomad_camels
import requests
from nomad_camels.ui_widgets import warn_popup

from PySide6.QtWidgets import QMessageBox

pypi_url = 'https://test.pypi.org/simple/'

def get_version():
    """ """
    for d in distributions():
        if d.metadata['Name'] == 'nomad-camels':
            return d.version
    return None

def update_camels():
    """ """
    subprocess.check_call([sys.executable, '-m', 'pip', 'install',
                           '--no-cache-dir', '--index-url', pypi_url,
                           '--extra-index-url', 'https://pypi.org/simple',
                           'nomad-camels', '--upgrade'])

def question_message_box(parent=None):
    """

    Parameters
    ----------
    parent :
         (Default value = None)

    Returns
    -------

    """
    installed_version = get_version()
    url = f'https://raw.githubusercontent.com/FAU-LAP/NOMAD-CAMELS/development/nomad_camels_version.txt'
    available_version = requests.get(url).text
    if installed_version == available_version:
        warn_popup.WarnPopup(parent,
                             'Your version of NOMAD-CAMELS is already up to date',
                             'Already up to date', info_icon=True)
        return
    update_dialog = QMessageBox.question(parent, 'Update NOMAD-CAMELS',
                                         f'Your current version of NOMAD-CAMELS is {installed_version}\n'
                                         f'The newest available version is {available_version}\n'
                                         f'Do you want to update now? (NOMAD-CAMELS will have to restart)',
                                         QMessageBox.Yes | QMessageBox.No)
    if update_dialog != QMessageBox.Yes:
        return
    update_camels()
    restart_dialog = QMessageBox.question(parent, 'Restart NOMAD-CAMELS now?',
                                          'Do you want to restart NOMAD-CAMELS now?',
                                          QMessageBox.Yes | QMessageBox.No)
    if restart_dialog == QMessageBox.Yes:
        restart_camels()

def restart_camels():
    """ """
    os.execl(sys.executable, sys.executable, *sys.argv)

def check_up_to_date():
    """ """
    installed_version = get_version()
    url = f'https://raw.githubusercontent.com/FAU-LAP/NOMAD-CAMELS/development/nomad_camels_version.txt'
    available_version = requests.get(url).text
    return installed_version == available_version

def auto_update(parent):
    """

    Parameters
    ----------
    parent :
        

    Returns
    -------

    """
    if not check_up_to_date():
        question_message_box(parent)

if __name__ == '__main__':
    update_camels()
