# For Loop - Protocol Step

This protocol step allows you to define a loop that will be iterated over. You can then add other steps into the loop by right-clicking and selecting `Add Into`. You can also drag and drop other steps into the loop.

The Loop Step will create (or get) a list of values and iterate over this list and run any step that is inside this loop for each iteration.

There are three main types of loops that you select with the `Loop-type` drop down menu:

1. **Start-Stop-Type:** This loop is either `start-stop`, `start-mix-max-stop` or `start-max-min-stop`. Creates a list that behaves accoridng to its name.
2. **Value-List:** You can manually enter values in a list that will be iterated over.
3. **Text-File:** Select a text file that contains a list of values as a simple column of numbers to iterate over them.

You can access the value of the loop by using the variable `<For_Loop_name>_Value`. The name is taken why the value you entered into the `name` field of the step. 

You can also access the number of the current iteration (so 0 for the first iteration, 1 for the second and so on) with `<For_Loop_name>_Count`. This allows you to keep track of the number of iterations performed. 