# Loops

## For Loop

This protocol step allows you to define a loop that will be iterated over. You can then add other steps into the loop by right-clicking and selecting `Add Into`. You can also drag and drop other steps into the loop.

The Loop Step will create (or get) a list of values and iterate over this list and run any step that is inside this loop for each iteration.

There are three main types of loops that you select with the `Loop-type` drop down menu:

1. **Start-Stop-Type:** This loop is either `start-stop`, `start-mix-max-stop` or `start-max-min-stop`. Creates a list that behaves accoridng to its name.
2. **Value-List:** You can manually enter values in a list that will be iterated over.
3. **Text-File:** Select a text file that contains a list of values as a simple column of numbers to iterate over them.

You can access the value of the loop by using the variable `<For_Loop_name>_Value`. The name is taken why the value you entered into the `name` field of the step. 

You can also access the number of the current iteration (so 0 for the first iteration, 1 for the second and so on) with `<For_Loop_name>_Count`. This allows you to keep track of the number of iterations performed. 

If one of the _Start-Stop_ types is selected, the sweep mode can be selected:
- _Linear_ means all steps have the same distance
- _Logarithmic_ means that the steps are on a logarithmic axis (e.g. from 1 to 100 in 3 steps gives `1, 10, 100`).
- _Exponential_ is the inverse of _logarithmic_
- _1/x_ selects the steps equidistant on a 1/x axis



## Simple Sweep

The Simple Sweep step is a convenient way to create a sweep for a single channel (so changing the value of one channel) while reading any number of other channels for each setpoint of the sweep channel.

### Defining the Sweep

The sweep is defined as for the [For Loop](#for-loop).

The _Data Output_ field is currently deprecated.

### Channels to set and read
The sweep's values will be set in the selected _Sweep Channel_. For each iteration the channels selected as _Read Channels_ will be read and saved.

### Plots and Fits

You can define plots that should be created while the simple sweep is running. To do this add a plot on the **right** side, as these plots belong to the simple sweep. Here you can also add fitting to your data.

You can use results from these fits as variables in your protocol. For this make sure that the fitting parameters are displayed for the function that you selected.

The entire script can use and also plot the results of fits if you define a plot on the **left** side of the window. This plot *belongs* to the entire protocol run.

In the end it may look like this:
![GUI of the simple sweep step with example parameters](images/image-3.png)


## ND Sweep
The ND sweep is a generalization of the [Simple Sweep](#simple-sweep).
It represents several loops, for example if both directions of an x-y stage are scanned.

The readings are the same for all loops.

In the tabs defining one single loop, the sweep values and the associated channel are defined. Additionally, after setting any channel, a wait time can be added.

The logic of the sweeps loops are as follows:
- outer loop
    - "middle" loop
        - inner loop

i.e. for each "middle" loop value the complete inner loop is run and for each outer loop value the complete "middle" loop.

## While Loop
The while loop allows to iterate as long as a given condition is True.
This condition can contain anything, including variables and channels, and works like [conditions in python](https://www.learnpython.org/en/Conditions). This is similar to the [If step](step_If.md#if-step) or [waiting for a condition](step_Wait.md#wait-for-condition).

```{note}
If you use variables or channels in the condition make sure to update / read them inside the loop!
```

A use case could also be to run an infinite loop with a variable `loop_running` as condition. Then, when using the _allow for live resetting of variables_, the experimentator can stop the loop by changing the value of the variable when desired.

The expected number of iterations is only used for the progress bar of CAMELS.

```{note}
Please note that the progress bar will almost certainly not be correct if your protocol contains a while loop.
```