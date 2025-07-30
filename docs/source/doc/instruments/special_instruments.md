# Special Instrument Drivers

This page gives an overview over some special instruments drivers, either because they are not directly connected to an actual instrument, or because they can be used generically for a multitude of similar instruments.


## Generic Drivers
These drivers either handle a communication protocol or are able to communicate with a multitude of similar instruments.

### EPICS
The driver allows you to interface with any of your EPICS PVs. For more information see the up to date driver's page on [PyPI](https://pypi.org/project/nomad-camels-driver-epics-instrument/).

### OPC UA
As with EPICS you can connect to any OPC UA variables in your environment. See the up to date driver's page on [PyPI](https://pypi.org/project/nomad-camels-driver-opc-ua-instrument/) for more information.

### NI DAQ
The driver enables you to interface with National Instruments DAQ. More can be found on [PyPI](https://pypi.org/project/nomad-camels-driver-ni-daq/).

### openCV
Allows to control any camera if it is possible with [openCV](https://pypi.org/project/opencv-python/). More information on the driver's page on [PyPI](https://pypi.org/project/nomad-camels-driver-openCV-instrument/).

### Cam-Control PyLabLib
This uses the cam control software of [PyLabLib](https://pylablib-cam-control.readthedocs.io/en/latest/). An in-depth explanation of this driver can be found [here](./cam_control_pylablib/cam_control_pylablib.md).


## Virtual Instruments
These instruments instead of communicating themselves take on calculations using other instruments' channels.

### PID Controller
Implements a PID controller in CAMELS. It comes with its own manual control and can be used in protocols. It may use 1 channel as output and 1 as input and allows for arbitrary calculations for conversion between reading and output. Find more on its page on [PyPI](https://pypi.org/project/nomad-camels-driver-PID/).

### Derived Channels
The driver allows you to create additional channels in CAMELS that are calculated from an arbitrary number of other channels and use them in your protocols. More information can be found on [PyPI](https://pypi.org/project/nomad-camels-driver-derived-channels/).

