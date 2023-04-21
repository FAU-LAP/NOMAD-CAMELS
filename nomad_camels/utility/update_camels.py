import os
import sys
import subprocess
from importlib.metadata import distributions
import nomad_camels
import requests

from PySide6.QtWidgets import QMessageBox

pypi_url = 'https://test.pypi.org/simple/'

def get_version():
    for d in distributions():
        if d.metadata['Name'] == 'nomad-camels':
            return d.version
    return None

def update_camels():
    subprocess.check_call([sys.executable, '-m', 'pip', 'install',
                           '--no-cache-dir', '--index-url', pypi_url,
                           '--extra-index-url', 'https://pypi.org/simple',
                           'nomad-camels', '--upgrade'])

def question_message_box(parent=None):
    installed_version = get_version()
    url = f'https://raw.githubusercontent.com/FAU-LAP/NOMAD-CAMELS/development/nomad_camels_version.txt'
    available_version = requests.get(url).text
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
    os.execl(sys.executable, sys.executable, *sys.argv)

if __name__ == '__main__':
    update_camels()
