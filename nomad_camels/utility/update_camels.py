import sys
import subprocess
from importlib.metadata import distributions
import nomad_camels

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


if __name__ == '__main__':
    update_camels()
