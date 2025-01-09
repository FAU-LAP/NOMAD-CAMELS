# Run Subprotocol
This step allows to run another CAMELS protocol inside this protocol.
The protocol is selected by the `.cprot` file that CAMELS creates.

```{note}
When running the main protocol, the sub protocol is re-built as well, i.e. changes made in CAMELS are adopted.
```

**Variables In** allows to execute the protocol with changing variables. An example use case for this is a [For Loop](step_For_Loop.md#for-loop---protocol-step) containing the _Run Subprotocol_ where a variable of the subprotocol changes with each iteration.

**Variables Out** lets you take a variable from the subprotocol and write it to a variable name for the main protocol. For example, when the subprotocol does a small calculation, these variables 