# While Loop
The while loop allows to iterate as long as a given condition is True.
This condition can contain anything and works like [conditions in python](https://www.learnpython.org/en/Conditions).

```note
If you use variables or channels in the condition make sure to update / read them inside the loop!
```

A use case could also be to run an infinite loop with a variable `loop_running` as condition. Then, when using the _allow for live resetting of variables_, the experimentator can stop the loop by changing the value of the variable when desired.

The expected number of iterations is only used for the progress bar of CAMELS.

```note
Please note that the progress bar will almost certainly not be correct if your protocol contains a while loop.
```