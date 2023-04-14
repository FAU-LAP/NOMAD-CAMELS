from setuptools import setup, find_packages

setup(
    name='camels_driver_PID',
    version='1.0',
    description='This packes provides everything to run a PID Controller with'
                'CAMELS',
    author='Johannes Lehmeyer / Alexander Fuchs',
    author_email='johannes.lehmeyer@fau.de',
    packages=find_packages(),
    install_requires=['simple-pid>=1.0.1']
)