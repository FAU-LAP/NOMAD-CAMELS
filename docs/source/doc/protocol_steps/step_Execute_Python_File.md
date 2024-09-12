# Execute Python File - Protocol Step

This step allows you to execute (run) any Python file on your system. To do this, enter the path to the file in the protocol step.

You can pass arguments to the Python script and save its results in variables so that you can continue to work with the returned data.

## Basic Functionality

This step calls something like

```python
subprocess.run(['python_exe_path', 'python_file_path', 'key=value', 'key2=value2', ...])
```

allowing you to execute a Python file with arbitrary arguments passed to it.

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
    "results": result,
    "results2": result2,
    ...
}
# Serialize the dictionary to a JSON formatted string
json_data = json.dumps(data)
# Print the JSON string and make sure it is passed to CAMELS
print("###Start Data") # Required so that CAMELS knows where to find the returned data!
print(json_data)
print("###End Data") # Required so that CAMELS knows where to find the returned data!
sys.stdout.flush()
```

where the keys of the returned dictionary match the variable names defined in the "Values returned by the Python file" table.

```{important}
You **MUST** print the `###Start Data` and `###End Data` strings so that CAMELS knows where to find the returned dictionary. This prevents other prints from your script from disturbing the data extraction later on.
``` 

CAMELS will then match the returned dictionary with the names of the values you defined that will be returned by the file and saves them to your data file.

Every key of the returned data dictionary is added to the Python namespace. This means you can access this variable the same way you would any other variable. You can use it for example to set an instrument channel to this value.

```{important}
You do not need to define the returned variable names. But if you do not, the returned value is not saved to the final data file! 

You can still access **ALL** the variables that are returned by the Python script in following protocol steps. In the example above you could still use `results2` as the variable for a *Set Channel* after the Python script execution. 
``` 

An example of a `Execute Python Script` step can be seen here.
![Example Image showing hwo to use the Execute Python Script step.](images/image-6.png)
This passes `factor=3` and what ever value the `Keithley_2000_read_voltage` channel read above to the script.
It expects a single returned result that will be saved and is accessible using the variable name `results`.

### Returning Arrays

Your Python file can also return arrays. Unfortunately numpy arrays can not be serialized with JSON, this means you must first convert your array to a list. This can be easily done using the `.tolist()` method. So something like

```python
array = np.arange(10)
data = {
    "results": array.tolist(),
}
# Serialize the dictionary to a JSON formatted string
json_data = json.dumps(data)
print("###Start Data")
print(json_data)
print("###End Data")
sys.stdout.flush()
```

will work. The returned array is now a list, so you must consider this if you want to perform further interactions with the variable. So something like `results.mean()` will not work!

For multidimensional arrays you can use:

```python
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)

a = np.array([[1, 2, 3], [4, 5, 6]])
print(a.shape)
json_dump = json.dumps({'a': a, 'aa': [2, (2, 3, 4), a], 'bb': [2]}, 
                       cls=NumpyEncoder)
print(json_dump)

--> Output:
(2, 3)
{"a": [[1, 2, 3], [4, 5, 6]], "aa": [2, [2, 3, 4], [[1, 2, 3], [4, 5, 6]]], "bb": [2]}
```

```{note}
Anything that can be serialized with JSON can be returned by your Python file.
```
