# Simple Sweep

The Simple Sweep step is a convenient way to create a sweep for a single channel (so changing the value of one channel) while reading any number of other channels for each setpoint of the sweep channel.

## Defining the Sweep

First select the channel you want to sweep (change). Then like in the For Loop, define the loop-type. Then define the list of values you want. Typically by giving start and stop (and min /max) values. Lastly select the channels you want to read for each value of the sweep channel.

## Plots and Fits

You can define plots that should be created while the simple sweep is running. To do this add a plot on the **right** side, as these plots belong to the simple sweep. Here you can also add fitting to your data.

You can use results from these fits as variables in your protocol. For this make sure that the fitting parameters are displayed for the function that you selected.

The entire script can use and also plot the results of fits if you define a plot on the **left** side of the window. This plot *belongs* to the entire protocol run.

In the end it can look something like this:
![GUI of the simple sweep step with example parameters](images/image-3.png)
