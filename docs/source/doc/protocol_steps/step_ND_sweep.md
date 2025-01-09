# ND Sweep
The ND sweep is a generalization of the [Simple Sweep](step_Simple_Sweep.md#simple-sweep).
It represents several loops, for example if both directions of an x-y stage are scanned.

The readings are the same for all loops.

In the tabs defining one single loop, the sweep values and the associated channel are defined. Additionally, after setting any channel, a wait time can be added.

The logic of the sweeps loops are as follows:
- outer loop
    - "middle" loop
        - inner loop

i.e. for each "middle" loop value the complete inner loop is run and for each outer loop value the complete "middle" loop.
