# Local Instrument Drivers
You can create and use local instrument drivers by creating this kind of folder structure

```
nomad_camels_driver_<parent_driver_name> (contains the actual device communication files)
└─> <parent_driver_name>.py
└─> <parent_driver_name>_ophyd.py
```
and giving the path to the parent folder in the CAMELS settings.

CAMELS then searches the given path for folder starting with `nomad_camels_driver_` and extracts the device name from the text following this.\
For more details on how the .py and ophyd.py files should look like you can go to the code examples in [Section 1.2.](python_files)

## File Templates
You can find templates for a new instrument driver [here](https://github.com/FAU-LAP/CAMELS_drivers/tree/main/empty_instrument_driver).

---

### Advanced Driver Information

**Regarding the `*.py` file.**

It should include a class `subclass` which inherits from `main_classes.device_class.Device`.
The arguments here should be set in the __init__ by the subclass (following) the documentation of the Device class.
For most devices, nothing further should be necessary in this class.

The `subclass_config`, inheriting from `main_classes.device_class.Device_Config` should provide the necessary configuration for the device and put this information into the device's `config`, `settings` and `ioc_settings` attributes.

**Regarding the `*ophyd.py` file.**

This should include a class (meaningfully named) inheriting from `ophyd.Device`.
Here you may set all the components the device has. \
Components that are created with kind='normal' (or not specified) will appear as channels inside CAMELS. Channels can be set and read and are the main way CAMELS communicates with devices during measurements. \
Components with kind='config' should be part of the configuration-widget.
