from setuptools import setup, find_packages

setup(
    name='camels_driver_bruker_magnet_ni_daq',
    version='1.0',
    description='This packes provides everything to run a Bruker magnet '
                'controlled by an NI DAQ-box with CAMELS',
    author='Johannes Lehmeyer / Alexander Fuchs',
    author_email='johannes.lehmeyer@fau.de',
    packages=find_packages(),
    install_requires=[]
)