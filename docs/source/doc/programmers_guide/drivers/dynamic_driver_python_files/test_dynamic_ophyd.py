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
    
    def put_function_generator(channel):
        def put_power_function(_self_instance, value):
            """
            This function returns a lambda function that sets the power of the specified channel.
            the put_function is added to the signal as a put_function.
            The _self_instance will later be resolved to the parent of the instance of the
            Ibeam_smart class that the signal belongs to.

            Parameters:
            _self_instance (object): The parent instance.
            value (float): The power to set the channel to.

            Returns:
            function: A lambda function that sets the power channel.

            """
            # It is important to pass the value to the lambda function!
            return lambda: _self_instance.parent.put_power_channel(channel, value)

        return put_power_function

    signal_dictionary = {}
    for channel in range(1, int(channel_number) + 1):
        # For each channel add read_power function
        signal_dictionary[f"read_power_channel_{channel}"] = Cpt(
            Custom_Function_SignalRO,
            name=f"read_power_channel_{channel}",
            metadata={"units": "", "description": f"Read power of channel {channel} which is the square of {channel}"},
            read_function=read_function_generator(channel),
        )
        # For each channel add a set power function
        signal_dictionary[f"put_power_channel_{channel}"] = Cpt(
            Custom_Function_Signal,
            name=f"put_power_channel_{channel}",
            metadata={"units": "", "description": f"Sets the power of channel {channel} to the value provided in the GUI."},
            put_function=put_function_generator(channel),
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
    
    def put_power_channel(self, channel, value):
        return f"Power of channel {channel} is set to {value}"
