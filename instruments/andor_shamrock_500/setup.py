from setuptools import setup, find_packages

setup(
    name='camels_driver_andor_shamrock_500',
    version='1.0',
    description='This packes provides everything to run the spectrometer Andor Shamrock 500',
    author='Johannes Lehmeyer / Alexander Fuchs',
    author_email='alexander.d.fuchs@fau.de',
    packages=find_packages(),
    install_requires=['camels_support_visa_signal @ git+https://github.com/FAU-LAP/CAMELS.git@new_device_management#subdirectory=instruments/Support/visa_signal']
)