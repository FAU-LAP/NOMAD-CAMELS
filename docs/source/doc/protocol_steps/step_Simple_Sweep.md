# Simple Sweep

The Simple Sweep step is a convenient way to create a sweep for a single channel (so changing the value of one channel) while reading any number of other channels for each setpoint of the sweep channel.

## Defining the Sweep

The sweep is defined as for the [For Loop](step_For_Loop.md#for-loop---protocol-step).

The _Data Output_ field is currently deprecated.

## Channels to set and read
The sweep's values will be set in the selected _Sweep Channel_. For each iteration the channels selected as _Read Channels_ will be read and saved.

## Plots and Fits

You can define plots that should be created while the simple sweep is running. To do this add a plot on the **right** side, as these plots belong to the simple sweep. Here you can also add fitting to your data.

You can use results from these fits as variables in your protocol. For this make sure that the fitting parameters are displayed for the function that you selected.

The entire script can use and also plot the results of fits if you define a plot on the **left** side of the window. This plot *belongs* to the entire protocol run.

In the end it may look like this:
![GUI of the simple sweep step with example parameters](images/image-3.png)
