from setuptools import setup, find_packages
from pkg_resources import parse_requirements

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='CAMELS_control',
    version='0.1',
    description='This is the main package to run CAMELS',
    author='Johannes Lehmeyer / Alexander Fuchs',
    author_email='johannes.lehmeyer@fau.de',
    packages=find_packages(),
    package_data={
        'CAMELS': ['graphics/*']
    },
    install_requires=requirements
)