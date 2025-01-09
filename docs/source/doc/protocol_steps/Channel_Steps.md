# Read Channels

This protocol step allows you to read data from all the instruments you have installed and also created instances of.

The name of each channel that you can read is something like `<instrument_name>_<parameter>` where parameter is a physical entity like `voltage`, `current`, `camera`. The available channels you can read are defined in the drivers for each instrument. Signals that you can set as well as read-only signals (called *SignalsRO*) create readable channels.

If you are using a SweepMe! instrument you can read everything that is in `self.variables` depending on the `SweepMode` selected.

Simply mark the checkbox to read the desired channels.
![Image of the Read Channels protocol step.](images/image.png)


## Trigger Channels

Some instruments with long acquisition times may provide splitted functions for triggering the reading process and the actual readout. To make use of this, in the _Read Channels_ step, one needs to select _Split trigger and read_.

In this case, the _Trigger Channels_ step can select the corresponding _Read Channels_. In between those two steps, any other steps can be executed.

# Set Channels

This protocol step allows you to set channels of the instruments you have installed and also created instances of.

The name of each channel that you can set is `<instrument_name>_set_<parameter>` where `<parameter>` is some thing like `voltage`, `current`, `camera_exposure_time`. The available channels you can set are defined in the drivers. Signals create readable channels.

If you are using a SweepMe! instrument you can only set channels if the instrument has a `SweepMode`. Depending on the mode selected in the *Instrument Manager* you will have the corresponding *Set Channel*.



Mark the checkbox to set the desired channels. Then enter the value that you want to set to the instrument into the value field. This value can either be a number, a Python expression that is evaluated at runtime or variables. This means you can set channels using complex python code. So something like `np.mean([1,2,3,4,5,6])` will evaluate to `3.5`. The available functions can be found by right clicking and looking at the `Insert Function` option. When CAMELS understands your expression the value field should turn green. If not is it red and will most likely not work. For very complex commands the red color might not be correct and it can work at runtime. 

You can also set channels to the value of variables that you defined before. You can do this in the bottom left of the window. Simply right-click and enter `Insert Variable`. Again you can apply any Python code to the variable and treat it as if it was a number.

Example of setting channels:

![Image of the GUI when using Set Channel showing possible settings of the value field.](images/image-2.png)

Here are the available functions you can use:

![Available functions you can use to set channels](images/image-1.png)
