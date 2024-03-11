# Keithley 2000 - Digital Multimeter (DMM)
This page is about the driver for the [Keithley 2000 Series](https://www.tek.com/en/products/keithley/digital-multimeter/keithley-2000-series-6-digit-multimeter-scanning)

## Installation
Install the instrument using the _Manage Instruments_ button of NOMAD-CAMELS.\
The PyPI package can be found on [PyPI](https://pypi.org/project/nomad-camels-driver-keithley-2000/) and can be installed via 

```powershell
pip install nomad-camels-driver-keithley-2000
```

## Features
The driver currently provides as channels:
- `V_DC` measure DC voltage
- `V_AC` measure AC voltage
- `I_DC` measure DC current
- `I_AC` measure AC current
- `resistance` measure 2-wire resistance value
- `resistance_4_wire` measure 4-wire resistance value

Further, as configuration can be applied:
- `NPLC` the number of power line cycles as integration time for measurements