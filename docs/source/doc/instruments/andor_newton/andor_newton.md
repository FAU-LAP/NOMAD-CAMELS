# Andor Newton CCD
This page is about the driver for [Andor Newton CCD Cameras](https://andor.oxinst.com/products/newton-ccd-and-emccd-cameras/newton-920)

## Installation
Install the instrument using the _Manage Instruments_ button of NOMAD-CAMELS.\
The PyPI package can be found on [PyPI](https://pypi.org/project/nomad-camels-driver-andor-newton/) and can be installed via 

```powershell
pip install nomad-camels-driver-andor-newton
```

The driver uses [pylablib](https://pylablib.readthedocs.io/en/latest/devices/Andor.html#cameras-andor-sdk2) for the communication, so that other cameras might work with the driver as well (not tested!).\
During the setup of the instrument in NOMAD CAMELS, the user needs to provide the path to the dll files provided by Andor through [Andor Solis](https://andor.oxinst.com/products/solis-software/) or the [Andor SDK](https://andor.oxinst.com/products/software-development-kit/software-development-kit).


## Features
The driver currently provides as channels:
- `read_camera` read the data from the camera using the defined settings

As configuration may be read:
- `get_temperature` read the current detector temperature
- `temperature_status` whether the cooling has reached the desired temperature

Further settings that are supported:
- `set_temperature` the desired temperature for the CCD
- `shutter_mode` controls the camera's shutterpossible values are "auto", "open" and "closed"
- `exposure_time` the exposure time for a single reading
- `readout_mode` how to interpret the data, "FVB - full vertical binning", "multi track" or "image"
- `preamp_gain` the preamplification gain
- `horizontal_binning` the number of bins to combine horizontally
- `hs_speed` the horizontal shift speed in microseconds / shift
- `vs_speed` the vertical shift speed in MHz
- `multi_tracks` the track start and end values for multi track mode
- `shutter_ttl_open` whether the shutter is open for TTL signal "low" or "high"