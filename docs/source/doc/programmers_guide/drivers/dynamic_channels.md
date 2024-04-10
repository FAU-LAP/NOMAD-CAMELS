# How to Create a Driver with Dynamically Changing Channels

This guide should show you how to write an instrument driver where the number and type of available Channels is defined and modifiable at run time.

```{Tip}
This is especially useful if you want to write drivers where you know that the individual instrument might have, for example, a varying number of channels, where every channel has the same functionality.
Or for instruments with a very large number of (very similar) channels, where you programmatically want to create the available set and read channels at runtime. 
```

## Create the Core Structure

As always it is easiest to simply create the core structure and boilerplate code using the _Driver Builder_ under _Tools_ in the _CAMELS_ GUI. As an example we will create a mock instrument called _test_dynamic_.

## Modify the `*.py` File

In the `<driver_name>.py` file you must change the following things:

1. Set `ophyd_device=None` in the `super.init()` of `subclass`
2. Set `ophyd_class_name="make_ophyd_instance"` in the `super.init()` of the subclass
3. Add any instrument configuration settings. We will simply add a combobox (drop down menu) to vary the number of channels. This should demonstrate how the dynamic channel generation works. So we add 
   
   ```python
   self.settings["channel_numbers"] = "3"  # default number of channels should be 3
   ``` 
   below the `__init__` of `subclass` and then add

   ```python
   comboBoxes = {"channel_numbers": ["1", "2", "3", "4", "5"]}
   ``` 
   
   to the `subclass_config` class after `__init__`.

   You can define anything to be passed to the class (in `.py` file) and then define what should happen with the value you passed to the class to create read and set channels dynamically (in `ophyd.py` file).
4. Add an import statement to the top where you import the `make_ophyd_class` defined in the `device_name_ophyd.py` file like this 
   
   ```python
   from .test_dynamic_ophyd import make_ophyd_class
   ```

   The `make_ophyd_class` takes any arguments and then creates read and write channels depending on what you define in the `ophyd.py` file. How to modify the `device_name_ophyd.py` file is explained [below](#modify-the-ophydpy-file) in more detail.
5. We want to create the ophyd class with the number of channels we select from the drop down menu. Add the following two methods to the subclass:
   
   ```python
    def update_driver(self):
        if (
            not "channel_numbers" in self.settings
            or not self.settings["channel_numbers"]
        ):
            return
        # make_ophyd_class is a function that returns a class with components that are generated at runtime
        # here we pass the channel_numbers to the make_ophyd_class which creates the class
        self.ophyd_class = make_ophyd_class(self.settings["channel_numbers"])
        # now we create an instance of the class
        # name="test" prevents the instrument driver from actually trying to connect directly to the physical instrument
        self.ophyd_instance = self.ophyd_class(
            channel_numbers=self.settings["channel_numbers"], name="test"
        )
        config, passive_config = get_configs_from_ophyd(self.ophyd_instance)
        for key, value in config.items():
            if key not in self.config:
                self.config[key] = value
        for key, value in passive_config.items():
            if key not in self.passive_config:
                self.passive_config[key] = value

    def get_channels(self):
        self.update_driver()
        return super().get_channels()
   ```

   These methods update the driver and make sure all teh channels are available. `self.ophyd_class` and `self.ophyd_instance` actually create the instrument instance, depending on the 
6. Define this function at the end of the file. It does not belong to any class
   
   ```python
    def get_configs_from_ophyd(ophyd_instance):
        config = {}
        passive_config = {}
        for comp in ophyd_instance.walk_components():
            name = comp.item.attr
            dev_class = comp.item.cls
            if name in ophyd_instance.configuration_attrs:
                if device_class.check_output(dev_class):
                    config.update({f"{name}": 0})
                else:
                    passive_config.update({f"{name}": 0})
        return config, passive_config
   ```

The final `.py` looks like this 

```python
from .test_dynamic_ophyd import Test_Dynamic
from .test_dynamic_ophyd import make_ophyd_class

from nomad_camels.main_classes import device_class


class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(
            name="test_dynamic",
            virtual=False,
            tags=[],
            directory="test_dynamic",
            ophyd_device=None,
            ophyd_class_name="make_ophyd_instance",
            **kwargs,
        )
        self.settings["channel_numbers"] = "3"  # default number of channels should be 3

    def update_driver(self):
        if (
            not "channel_numbers" in self.settings
            or not self.settings["channel_numbers"]
        ):
            return
        # make_ophyd_class is a function that returns a class with components that are generated at runtime
        # here we pass the channel_numbers to the make_ophyd_class which creates the class
        self.ophyd_class = make_ophyd_class(self.settings["channel_numbers"])
        # now we create an instance of the class
        # name="test" prevents the instrument driver from actually trying to connect directly to the physical instrument
        self.ophyd_instance = self.ophyd_class(
            channel_numbers=self.settings["channel_numbers"], name="test"
        )
        config, passive_config = get_configs_from_ophyd(self.ophyd_instance)
        for key, value in config.items():
            if key not in self.config:
                self.config[key] = value
        for key, value in passive_config.items():
            if key not in self.passive_config:
                self.passive_config[key] = value

    def get_channels(self):
        self.update_driver()
        return super().get_channels()


class subclass_config(device_class.Simple_Config):
    def __init__(
        self,
        parent=None,
        data="",
        settings_dict=None,
        config_dict=None,
        additional_info=None,
    ):
        comboBoxes = {"channel_numbers": ["1", "2", "3", "4", "5"]}
        super().__init__(
            parent,
            "test_dynamic",
            data,
            settings_dict,
            config_dict,
            additional_info,
            comboBoxes=comboBoxes,
        )
        self.load_settings()
    



def get_configs_from_ophyd(ophyd_instance):
    config = {}
    passive_config = {}
    for comp in ophyd_instance.walk_components():
        name = comp.item.attr
        dev_class = comp.item.cls
        if name in ophyd_instance.configuration_attrs:
            if device_class.check_output(dev_class):
                config.update({f"{name}": 0})
            else:
                passive_config.update({f"{name}": 0})
    return config, passive_config
```

## Modify the `*ophyd.py` File

In the `*ophyd.py` file we must define the `make_ophyd_class` and `make_ophyd_instance` functions.

### 1. Define  `make_ophyd_class`
We will start by adding the function that defines and creates the class first:

```python
def make_ophyd_class(channel_number):
    signal_dictionary = {}
    for channel in range(1, int(channel_number) + 1):
        # For each channel add read_power function
        signal_dictionary[f"read_power_channel_{channel}"] = Cpt(
            Custom_Function_SignalRO,
            name=f"read_power_channel_{channel}",
            metadata={"units": "", "description": ""},
            read_function=read_function_generator(channel),
        )

    return type(
        f"Test_Dynamic_total_channels_{channel_number}",
        (Test_Dynamic,),
        {**signal_dictionary},
    )
```

### 2. Define `read_function_generator`
As we want to create read and write channels for each instrument channel, we iterate over all the available channels. Here you would add your own code and add the desired components to the `signal_dictionary`. We are using `CustomFunctionSignalsRO` as we only want to be able to read these channels.

```{Attention}
The `read_function=read_function_generator(channel)` line is very important as this is where we define what exactly is done when we call the _read channel_ in CAMELS.
```

As we want to dynamically create these read_functions as they most likely are slightly different for each channel (this depends on the exact instrument) we will use a closure to create many instances of slightly different functions.

For this add the definition of the `read_function_generator` anywhere in the ophyd file. You can add it into the `make_ophyd_class` if you like:

```python
def make_ophyd_class(channel_number):
    def read_function_generator(channel):
        def read_function(_self_instance):
            """
            This function returns a lambda function that reads the power of the specified channel.
            the read_function is added to the signal as a read_function.
            The _self_instance will later be resolved to the parent of the instance of the
            Ibeam_smart class that the signal belongs to.

            Parameters:
            _self_instance (object): The parent instance.

            Returns:
            function: A lambda function that reads the power channel.

            """
            return lambda: _self_instance.parent.read_power_channel(channel)

        return read_function

    signal_dictionary = {}
    for channel in range(1, int(channel_number) + 1):
```

It makes sense to add the `_self_instance` argument as this allows you to access all the methods of the parent class (so here the `Test_Dynamic` class) later on. The signals can handel functions that have the `_self_instance` argument and then pass the correct `self` to the function.

### 3. Define `make_ophyd_instance`
Now we define the function that creates an instance of the class we just defined. 

```python
def make_ophyd_instance(
    prefix="",
    *args,
    name,
    kind=None,
    read_attrs=None,
    configuration_attrs=None,
    parent=None,
    # These are the arguments you want to pass to the ophyd class
    # These are the settings you defined in the .py file
    # We will pass the number of channels we selected in the drop down and are defined in the .py file
    channel_numbers="",
    **kwargs,
):
    ophyd_class = make_ophyd_class(channel_numbers)
    return ophyd_class(
        prefix,
        *args,
        name=name,
        kind=kind,
        read_attrs=read_attrs,
        configuration_attrs=configuration_attrs,
        parent=parent,
        # These are the arguments you want to pass to the ophyd class
        # These are the settings you defined in the .py file
        # We will pass the number of channels we selected in the drop down and are defined in the .py file
        channel_numbers=channel_numbers,
        **kwargs,
    )
```

The instance we return here is the class we return with `make_ophyd_class`. 

```python
    ...
    return type(
        f"Test_Dynamic_total_channels_{channel_number}",
        (Test_Dynamic,), # This is the class that was automatically created by the driver_builder
        {**signal_dictionary},
    )
```

See [above](#1-define-make_ophyd_class) for more details.

### 4. Define the Device Class
The _driver builder_ automatically created the default Device class depending on the name you gave in the driver builder. For us this class is called `Test_Dynamic`. 

```python
class Test_Dynamic(Device):
    channel_numbers = Cpt(
        Custom_Function_Signal,
        name="channel_numbers",
        kind="config",
        metadata={"units": "None", "description": "number of channels selected by the user in the GUI"},
    )
    def __init__(
        self,
        prefix="",
        *,
        name,
        kind=None,
        read_attrs=None,
        configuration_attrs=None,
        parent=None,
        # This is what you need to add:
        channel_number="",
        **kwargs,
    ):
        super().__init__(
            prefix=prefix,
            name=name,
            kind=kind,
            read_attrs=read_attrs,
            configuration_attrs=configuration_attrs,
            parent=parent,
            **kwargs,
        )
```

### 5. Adding functions to the parent class

In the `read_function_generator` we defined that there must be a method of the parent class called `read_power_channel` as you can see here:

```python
def read_function_generator(channel):
...
    return lambda: _self_instance.parent.read_power_channel(channel)
...
```

We must now add this function to the parent class (the `Test_Dynamic` class)

```python
class Test_Dynamic(Device):
    def __init__(
        self,
        prefix="",
        *,
        name,
        kind=None,
        read_attrs=None,
        configuration_attrs=None,
        parent=None,
        # These are the settings you defined in the ophyd class
        channel_numbers="",
        **kwargs,
    ):
        super().__init__(
            prefix=prefix,
            name=name,
            kind=kind,
            read_attrs=read_attrs,
            configuration_attrs=configuration_attrs,
            parent=parent,
            **kwargs,
        )
        self.channel_numbers = channel_numbers

        # if name is test then all the code after the return is skipped
        # this is useful if you perform actual connections to instruments, that should not run when first defining the instrument in the GUI
        if name == "test":
            return

    # This function is called by the read_function_generator
    def read_power_channel(self, channel):
        return f"Power of channel {channel} is {channel**2}"
```

### 7. Final `ophyd.py` File

The final file looks like this

```python
from ophyd import Component as Cpt

from nomad_camels.bluesky_handling.custom_function_signal import (
    Custom_Function_Signal,
    Custom_Function_SignalRO,
)
from ophyd import Device


def make_ophyd_instance(
    prefix="",
    *args,
    name,
    kind=None,
    read_attrs=None,
    configuration_attrs=None,
    parent=None,
    # These are the arguments you want to pass to the ophyd class
    # These are the settings you defined in the .py file
    # We will pass the number of channels we selected in the drop down and are defined in the .py file
    channel_numbers="",
    **kwargs,
):
    ophyd_class = make_ophyd_class(channel_numbers)
    return ophyd_class(
        prefix,
        *args,
        name=name,
        kind=kind,
        read_attrs=read_attrs,
        configuration_attrs=configuration_attrs,
        parent=parent,
        # These are the arguments you want to pass to the ophyd class
        # These are the settings you defined in the .py file
        # We will pass the number of channels we selected in the drop down and are defined in the .py file
        channel_numbers=channel_numbers,
        **kwargs,
    )


def make_ophyd_class(channel_number):
    def read_function_generator(channel):
        def read_function(_self_instance):
            """
            This function returns a lambda function that reads the power of the specified channel.
            the read_function is added to the signal as a read_function.
            The _self_instance will later be resolved to the parent of the instance of the
            Ibeam_smart class that the signal belongs to.

            Parameters:
            _self_instance (object): The parent instance.

            Returns:
            function: A lambda function that reads the power channel.

            """
            return lambda: _self_instance.parent.read_power_channel(channel)

        return read_function

    signal_dictionary = {}
    for channel in range(1, int(channel_number) + 1):
        # For each channel add read_power function
        signal_dictionary[f"read_power_channel_{channel}"] = Cpt(
            Custom_Function_SignalRO,
            name=f"read_power_channel_{channel}",
            metadata={"units": "", "description": ""},
            read_function=read_function_generator(channel),
        )

    return type(
        f"Test_Dynamic_total_channels_{channel_number}",
        (Test_Dynamic,),
        {**signal_dictionary},
    )


class Test_Dynamic(Device):
    def __init__(
        self,
        prefix="",
        *,
        name,
        kind=None,
        read_attrs=None,
        configuration_attrs=None,
        parent=None,
        # These are the settings you defined in the ophyd class
        channel_numbers="",
        **kwargs,
    ):
        super().__init__(
            prefix=prefix,
            name=name,
            kind=kind,
            read_attrs=read_attrs,
            configuration_attrs=configuration_attrs,
            parent=parent,
            **kwargs,
        )
        self.channel_numbers = channel_numbers

        # if name is test then all the code after the return is skipped
        # this is useful if you perform actual connections to instruments, that should not run when first defining the instrument in the GUI
        if name == "test":
            return
    
    # This function is called by the read_function_generator
    def read_power_channel(self, channel):
        return f"Power of channel {channel} is {channel**2}"

```