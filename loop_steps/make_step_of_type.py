from main_classes.loop_step import Loop_Step, Loop_Step_Container, Loop_Step_Config
from loop_steps import for_while_loops, read_channels, set_channels

from utility import variables_handling

step_type_config = {'Default': [Loop_Step, Loop_Step_Config],
                    'Container': [Loop_Step_Container, Loop_Step_Config],
                    'For Loop': [for_while_loops.For_Loop_Step, for_while_loops.For_Loop_Step_Config],
                    'Read Channels': [read_channels.Read_Channels, read_channels.Read_Channels_Config],
                    'Set Channels': [set_channels.Set_Channels, set_channels.Set_Channels_Config],
                    'While Loop': [for_while_loops.While_Loop_Step, for_while_loops.While_Loop_Step_Config]}

def get_device_steps():
    device_steps = {}
    for devname, device in sorted(variables_handling.devices.items(), key=lambda x: x[0].lower()):
        device_steps.update(device.get_special_steps())
    return device_steps


def make_step(step_type, step_info=None, children=None):
    dev_steps = get_device_steps()
    if step_type in step_type_config:
        if step_info is None:
            name = step_type.replace(' ', '_')
        else:
            name = step_info['name']
        return step_type_config[step_type][0](name=name, step_info=step_info, children=children)
    elif step_type in dev_steps:
        if step_info is None:
            name = step_type.replace(' ', '_')
        else:
            name = step_info['name']
        return dev_steps[step_type][0](name=name, step_info=step_info, children=children)
    return Loop_Step(name='fail')

def get_config(step:Loop_Step):
    """Returns the Loop_Step_Config belonging to the given step."""
    step_type = step.step_type
    dev_steps = get_device_steps()
    if step_type in step_type_config:
        return step_type_config[step_type][1](loop_step=step)
    elif step_type in dev_steps:
        return dev_steps[step_type][1](loop_step=step)
    raise Exception('Loop Step configuration is not defined!')

