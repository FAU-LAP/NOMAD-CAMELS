What you need to implement a new device:

The directory should be named like the device.


`device`.py

This should include a class `subclass` which inherits from `main_classes.device_class.Device`.
The Arguments here should be set in the __init__ by the subclass (following) the documentation of the Device class.
For most devices, nothing further should be necessary in this class.
In the attribute `files`, you should list all files, needed for an IOC to support this device. These should be in the same directory.

The `subclass_config`, inheriting from `main_classes.device_class.Device_Config`.
It should provide the necessary configuration for the device and put this information into the device's `config`, `settings` and `ioc_settings` attributes.



`device`_ophyd.py
This should include a class (meaningfully named) inheriting from `ophyd.Device`.
Here you may set all the components the device has. Those with a kind='normal' (or not specified) will appear as channels inside CAMELS. Those with kind='config' should be part of the configuration-Widget.

