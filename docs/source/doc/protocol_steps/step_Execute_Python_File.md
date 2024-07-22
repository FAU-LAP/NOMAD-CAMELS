# Execute Python File

This step allows you to execute (run) any Python file on your system. For this simply give the step the path to the file.

You can pass values to the Python script as well as save its results in variables so that you can continue to work with the returned data.

## Basic Function

This step basically calls something like

```python
subprocess.run(['python_exe_path', 'python_file_path', 'key=value', 'key2=value2', ...])
```

## The Python Environment

The Python file can be run using three different Python environment types. As CAMELS can not know which packages your script might need you have the possibility to define exactly which environment it should use:

1. **CAMELS Python**: This uses the same environment that is running CAMELS itself. This should be fine in many cases where you do not require unusual or very specific packages. You can find a list of the installed packages on our [GitHub](https://github.com/FAU-LAP/NOMAD-CAMELS/blob/main/requirements.txt).
2. **Existing Python Environment**: If you need very specific packages or very specific versions for your script to work you can also give the path to the `python.exe` of an already existing environment. The script will then be run using this python.exe. 
3. **Specific Packages**: If you only need a small number of very specific packages with specific versions you can use this option. Here you can define the package number and its version. The environment will be built at run time in a temp folder. It will then execute your script with this environment and then delete the environment again.
   ```{attention}
   Only do this if you really need this and don't do this very often, as this is quite slow!
   ```

## Passing Values

You can pass values to the Python file to be executed. These are the `key=value` pairs you can see in the command [above](#basic-function). 
To do this, add variables/keys and their value using the green button and then entering the desired values.

You can leave the value field empty. CAMELS will then try and find the variable name you gave in the current name space. 

```{note}
This means you can use channel or variable names here if you leave the value field empty!
```

If you give it a value it will pass the key value pair to the file.

To then use the key-value pairs in your script you can do something like

```python
# Parse the arguments into a dictionary assuming they are in key=value format
arguments = sys.argv[1:]
arguments_dict = {}
for arg in arguments:
    key, value = map(str.strip, arg.split("=", 1))
    arguments_dict[key] = value
```

and then use the `arguments_dict` to use the passed variables in any way you like.


## Returning Results

CAMELS can also read the results returned by your Python script. For this your script must `print()` the results, as CAMELS gets its results from the `stdout` of `subprocess.run`
It is recommended to do something like

```python
data = {
    "results": result
}
# Serialize the dictionary to a JSON formatted string
json_data = json.dumps(data)
# Print the JSON string and make sure it is passed to CAMELS
print(json_data)
sys.stdout.flush()
```

CAMELS will then match the returned dictionary with the names of the values you defined that will be returned by the file. CAMELS looks for the beginning of a curly brace `{` and matches after it until the end of the closing brace; it can handle one level of nested dictionaries.

To be able to use the returned variable and its contents in the rest of the protocol it might make sense to define the variable in the left of the window, so you can easily add it to the following steps if you use the value to perform further steps.

An example of a `Execute Python Script` step can be seen here.
![Example Image showing hwo to use the Execute Python Script step.](images/image-4.png)
This passes `exponent=2` and what ever value the `Keithley_2000_read_voltage` channel had above to the script.
It expects a single returned result that will be accessible using the varaible name `results`.

