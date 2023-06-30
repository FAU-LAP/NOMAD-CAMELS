# EPICS instrument-drivers
To make new NOMAD-CAMELS drivers for your EPICS environment it is easiest to use the EPICS-driver-builder that you can find in NOMAD-CAMELS under "Tools".

## How to use the builder
You can use the driver-builder as follows:
- __Instrument Name:__ This will be the `<instrument_driver_name>` of your instrument in NOMAD-CAMELS.
- __Input Channels:__ These are the PV-names that are later listed as read-only channels in NOMAD-CAMELS
- __Output Channels:__ List the PV-names you want to use as writable channels
- __Config Channels - Read Only:__ These PVs are for configuration that usually needs to be read only once. An example could be the identity of a measurement instrument.
- __Config Channels:__ These are the PVs that will configure the instrument in the beginning of the measurement. Here, you also need to give a datatype for the PV (float, string or bool), which will be used to generate the UI in the instrument configuration.

When you click on "Build Driver", a folder named `nomad_camels_driver_<instrument_driver_name>` should appear in the specified path (either you are asked when the build is done, or it is your local driver path, specified in the program's settings).  
The folder should contain two files `<instrument_driver_name>.py` and `<instrument_driver_name>_ophyd.py`.

The resulting PV-names will in the end be `<instrument_name>:<PV-name>` where:
- `<instrument_name>` is the name you give your instrument in the config inside NOMAD-CAMELS --> manage instruments
- `<PV-name>` is the the name you give the PVs in the builder. You can also see them in the `<instrument_driver_name>_ophyd.py`-file.
> &#9888; There are two things you need to pay attention to:
> - The `<instrument_driver_name>` you use in the builder must __NOT__ be equal to the name of your instrument later.
> - The `<PV-name>` should not mirror any python builtin function. If your EPICS environment uses such a name, you can edit the file (see [Troubleshooting](epics_driver_builder_troubleshooting))

(epics_driver_builder_troubleshooting)=
## Troubleshooting
If a PV in your EPICS environment is e.g. called `test:set`, you might want to mirror it in your driver:
```python
set = Cpt(EpicsSignal, "set") # This does not work!
```
Since `set` is a builtin function, this will not work. Instead you can break the convention of bluesky / ophyd that the components and PVs should have the same name and change the variable name like this:
```python
setter = Cpt(EpicsSignal, "set") # This works
```
