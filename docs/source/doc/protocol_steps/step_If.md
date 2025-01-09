# If step
This step allows for conditional branching of the protocol.

The condition can contain anything, including variables and channels, and works like [conditions in python](https://www.learnpython.org/en/Conditions). This is similar to the [While Loop](step_While_Loop.md#while-loop) or [waiting for a condition](step_Wait.md#wait-for-condition).

A grayed sub-step will appear in the protocol, called "If_Sub". The steps to be executed when the condition is true go here. When `Use Else` is selected, analogously an "Else_Sub" will appear to be executed when the condition is false.

In between the "If_Sub" and "Else_Sub", or without "else", an arbitrary number of "Elif" cases can be inserted. They may check for other conditions, allowing for simple branching on several conditions without nesting many If-steps.

When "End protocol if condition is true" is selected, the protocol will stop **after** the execution of the steps in "If_Sub". However, "If_Sub" may also be empty in this case.