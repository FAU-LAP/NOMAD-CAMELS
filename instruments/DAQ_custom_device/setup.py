from setuptools import setup, find_packages

setup(
    name='camels_driver_DAQ_custom_device',
    version='1.0',
    description='This packes provides everything to run a custom '
                'NI DAQ-task with CAMELS',
    author='Johannes Lehmeyer / Alexander Fuchs',
    author_email='johannes.lehmeyer@fau.de',
    packages=find_packages(),
    install_requires=[]
)