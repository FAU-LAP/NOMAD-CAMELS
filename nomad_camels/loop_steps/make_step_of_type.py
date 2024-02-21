"""This module provides a way to produce all possible protocol steps from the UI"""

from nomad_camels.main_classes.loop_step import Loop_Step
from nomad_camels.loop_steps import (
    for_while_loops,
    read_channels,
    set_channels,
    wait_loop_step,
    if_step,
    prompt_loop_step,
    run_subprotocol,
    simple_sweep,
    gradient_descent,
    change_device_config,
    nd_sweep,
    set_variables,
    set_value_popup,
    export_data,
    call_function,
)

from nomad_camels.utility import variables_handling

step_type_config = {
    "Call Function": [call_function.Call_Function, call_function.Call_Function_Config],
    "Change Device Config": [
        change_device_config.Change_DeviceConf,
        change_device_config.Change_DeviceConf_Config,
    ],
    # 'Export Data': [export_data.Export_Data_Step,
    #                 export_data.Export_Data_Step_Config],
    "For Loop": [for_while_loops.For_Loop_Step, for_while_loops.For_Loop_Step_Config],
    "Gradient Descent": [
        gradient_descent.Gradient_Descent_Step,
        gradient_descent.Gradient_Descent_Config,
    ],
    "If": [if_step.If_Loop_Step, if_step.If_Step_Config],
    "ND Sweep": [nd_sweep.ND_Sweep, nd_sweep.ND_Sweep_Config],
    "Prompt": [
        prompt_loop_step.Prompt_Loop_Step,
        prompt_loop_step.Prompt_Loop_Step_Config,
    ],
    "Read Channels": [read_channels.Read_Channels, read_channels.Read_Channels_Config],
    "Run Subprotocol": [
        run_subprotocol.Run_Subprotocol,
        run_subprotocol.Run_Subprotocol_Config,
    ],
    "Set Channels": [set_channels.Set_Channels, set_channels.Set_Channels_Config],
    "Set Value Popup": [
        set_value_popup.Set_Value_Popup,
        set_value_popup.Set_Value_Popup_Config,
    ],
    "Set Variables": [set_variables.Set_Variables, set_variables.Set_Variables_Config],
    "Simple Sweep": [simple_sweep.Simple_Sweep, simple_sweep.Simple_Sweep_Config],
    "Trigger Channels": [
        read_channels.Trigger_Channels_Step,
        read_channels.Trigger_Channels_Config,
    ],
    "While Loop": [
        for_while_loops.While_Loop_Step,
        for_while_loops.While_Loop_Step_Config,
    ],
    "Wait": [wait_loop_step.Wait_Loop_Step, wait_loop_step.Wait_Loop_Step_Config],
}

non_addables = {
    "If_Sub": [if_step.If_Sub_Step, if_step.Sub_Step_Config],
    "Elif_Sub": [if_step.Elif_Sub_Step, if_step.Sub_Step_Config],
    "Else_Sub": [if_step.Else_Sub_Step, if_step.Sub_Step_Config],
}


def get_device_steps():
    """Goes through all the devices and checks, whether they provide
    their own types of loop-steps.

    Returns
    -------
    device_steps
        dictionary of the possible steps provided by the devices
    """
    device_steps = {}
    for devname, device in sorted(
        variables_handling.devices.items(), key=lambda x: x[0].lower()
    ):
        device_steps.update(device.get_special_steps())
    return device_steps


def make_step(step_type, step_info=None, children=None, protocol=None):
    """Checks whether the given `step_type` is supported, if yes, then a
    step of that type with the given info and children will be created.
    If there is no step_info, a new step is made.

    Parameters
    ----------
    step_type : str
        A string representing the type of the step. Should correspond to one of
        the keys of `step_type_config` or a device specific step.
    step_info : dict, None
        (Default value = None)
        The information for the step's configuration
    children : list[Loop_Step], None
        (Default value = None)
        The produced step's children. Handed over to it's constructor.
    protocol : Measurement_Protocol
        (Default value = None)
        The protocol, in which the step should be.

    Returns
    -------
    step
        The produced step.
    """
    dev_steps = get_device_steps()
    if step_type in step_type_config:
        if step_info is None:
            name = step_type.replace(" ", "_")
        else:
            name = step_info["name"]
        return step_type_config[step_type][0](
            name=name, step_info=step_info, children=children, protocol=protocol
        )
    elif step_type in dev_steps:
        if step_info is None:
            name = step_type.replace(" ", "_")
        else:
            name = step_info["name"]
        return dev_steps[step_type][0](
            name=name, step_info=step_info, children=children, protocol=protocol
        )
    elif step_type in non_addables:
        if step_info is None:
            name = step_type.replace(" ", "_")
        else:
            name = step_info["name"]
        return non_addables[step_type][0](
            name=name, step_info=step_info, children=children, protocol=protocol
        )
    return Loop_Step(name="fail")


def get_config(step: Loop_Step):
    """Returns the Loop_Step_Config belonging to the given step.

    Parameters
    ----------
    step : Loop_Step
        The step for which the config-widget should be opened.

    Returns
    -------
    step_config
        The Loop_Step_Config corresponding to the given `step`.
    """
    step_type = step.step_type
    dev_steps = get_device_steps()
    if step_type in step_type_config:
        return step_type_config[step_type][1](loop_step=step)
    elif step_type in dev_steps:
        return dev_steps[step_type][1](loop_step=step)
    elif step_type in non_addables:
        return non_addables[step_type][1](loop_step=step)
    raise Exception("Loop Step configuration is not defined!")
