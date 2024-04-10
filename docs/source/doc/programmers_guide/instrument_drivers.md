# Create New Instrument Drivers

Do you want to use CAMELS but can not find existing drivers for the instruments you have in your lab?\
You can simply create your own drivers for CAMELS. We provide you with automatic builders and guides to help you create them.

```{tip}
Follow our [step-by-step tutorial](drivers/drivers_tutorial.md) to learn the basics on how to create your own instrument driver.  
```

Or you can read the pages below to directly [start writing](drivers/writing_drivers.md) your own driver.

```{tip}
If you have instrument communication already implemented using **EPICS** you can [create drivers for EPICS](drivers/EPICS_drivers.md) very easily. 
```

```{toctree}
:maxdepth: 2

Tutorial: Creating your own Instrument Driver <drivers/drivers_tutorial>
How to Write New Drivers <drivers/writing_drivers.md>
How to Modify Existing Drivers <drivers/modifying_drivers.md>
How to Share Your Drivers with Others <drivers/pypi_drivers.md>
Create Driver with Dynamically Changing Channels <drivers/dynamic_channels.md>
EPICS Instrument Drivers <drivers/EPICS_drivers.md>
```
