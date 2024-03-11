# Agilent 34401A - Digital Multimeter (DMM)
This page is about the driver for the [34401A Digital Multimeter by Agilent/Keysight](https://www.keysight.com/de/de/product/34401A/digital-multimeter-6-digit.html)

## Installation
Install the instrument using the _Manage Instruments_ button of NOMAD-CAMELS.\
The PyPI package can be found on [PyPI](https://pypi.org/project/nomad-camels-driver-agilent-34401a/) and can be installed via 

```powershell
pip install nomad-camels-driver-agilent-34401a
```

## Features
The driver currently provides as channels:
- DC measurement of voltage and current
- AC measurement of voltage and current
- two or four wire measurements of a resistance
- reading the error message from the instrument