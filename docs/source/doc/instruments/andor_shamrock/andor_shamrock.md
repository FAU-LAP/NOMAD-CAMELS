# Andor Shamrock 500
This page is about the driver for [Andor Shamrock Spectrometer](https://andor.oxinst.com/products/kymera-and-shamrock-spectrographs/shamrock-500i)

## Installation
Install the instrument using the _Manage Instruments_ button of NOMAD-CAMELS.\
The PyPI package can be found on [PyPI](https://pypi.org/project/nomad-camels-driver-andor-shamrock-500/) and can be installed via 

```powershell
pip install nomad-camels-driver-andor-shamrock-500
```

The driver uses [pylablib](https://pylablib.readthedocs.io/en/latest/devices/AndorShamrock.html) for the communication.\
During the setup of the instrument in NOMAD CAMELS, the user needs to provide the path to the dll files provided by Andor through [Andor Solis](https://andor.oxinst.com/products/solis-software/) or the [Andor SDK](https://andor.oxinst.com/products/software-development-kit/software-development-kit).


## Features
The driver currently provides as channels:
- `spectrum` the count values of the recorded spectrum
- `wavelength` the wavelengths corresponding to `spectrum`

Supported as configuration:
- `set_grating_number` select the grating of the used grating turret
- `center_wavelength` set the center of the wavelengths to the given value
- `input_port` "direct" or "side", depending on where the signal comes from, if no flip is installed, it does not change anything
- `output_port` "direct" or "side", the port of the used camera, if no flip is installed, it does not change anything
- `camera` to use the spectrometer in NOMAD CAMELS, one has to connect to a supported camera, that can be read when taking a spectrum
- `input_slit_size` the size of the input slit, if installed
- `output_slit_size` the size of the output slit, if installed
- `horizontal_cam_flip` whether to flip the camera data horizontally (e.g. if the camera is turned upside down because of spatial restraints)