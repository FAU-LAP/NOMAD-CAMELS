# Read Channels

This protocol step allows you to read data from all the instruments you have installed and also created instances of.

The name of each channel that you can read is always `<instrument_name>_read_<parameter>` where parameter is some thing like `voltage`, `current`, `camera`. The available channels you can read are defined in the drivers for each instrument. Signals as well as SignalsRO (Read Only) create readable channels. 

If you are using a SweepMe! instrument you can read everything that is in `self.variables` depending on the `SweepMode`  selected.

Simply mark the checkbox to read the desired channels.
![Image of the Read Channels protocol step.](images/image.png)
