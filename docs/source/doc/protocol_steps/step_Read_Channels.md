# Read Channels - Protocol Step

This protocol step allows you to read data from all the instruments you have installed and also created instances of.

The name of each channel that you can read is something like `<instrument_name>_<parameter>` where parameter is a physical entity like `voltage`, `current`, `camera`. The available channels you can read are defined in the drivers for each instrument. Signals that you can set as well as read-only signals (called *SignalsRO*) create readable channels.

If you are using a SweepMe! instrument you can read everything that is in `self.variables` depending on the `SweepMode` selected.

Simply mark the checkbox to read the desired channels.
![Image of the Read Channels protocol step.](images/image.png)


## Trigger Channels

Some instruments with long acquisition times may provide splitted functions for triggering the reading process and the actual readout. To make use of this, in the _Read Channels_ step, one needs to select _Split trigger and read_.

In this case, the _Trigger Channels_ step can select the corresponding _Read Channels_. In between those two steps, any other steps can be executed.