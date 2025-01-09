# Wait

Wait has several options:

### Simple wait
In this case, you can define a number of seconds for which CAMELS should wait before continuing the execution of the protocol. The number can also be an expression that calculates the amount of time using variables or channel values.

### Wait with progress bar
Here the same applies as for the [Simple wait](#simple-wait). When this step is executed in the protocol, a progress bar appears until the waiting is done.

If `skipable` is selected, the window with the progress bar will have a "Skip" button, that cancels the waiting when clicked and the execution of the protocol continues.

### Wait for condition
Here, a condition can be defined, and CAMELS will wait **until** this condition resolves to true. This condition can contain anything, including variables and channels, and works like [conditions in python](https://www.learnpython.org/en/Conditions). This is similar to the [If step](step_If.md#if-step) or the [While Loop](step_While_Loop.md#while-loop).

To evaluate the condition, channels may be selected to be read.
The field `read every` defines how often the selected channels are read and the condition is re-evaluated.

```{note}
Only if you select the channels to be read, they will update in the condition. Make sure to read all channels you use in the condition!
```